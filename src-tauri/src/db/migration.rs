pub struct Migration {
    pub version: u32,
    pub description: &'static str,
    pub up: &'static str,
    #[allow(dead_code)] // 롤백 기능은 Phase 6에서 구현
    pub down: Option<&'static str>,
}

pub const MIGRATIONS: &[Migration] = &[
    Migration {
        version: 1,
        description: "initial_schema",
        up: include_str!("../../migrations/V001_initial_schema.sql"),
        down: Some(include_str!(
            "../../migrations/V001_initial_schema.rollback.sql"
        )),
    },
    Migration {
        version: 2,
        description: "add_ai_settings",
        up: include_str!("../../migrations/V002_add_ai_settings.sql"),
        down: Some(include_str!(
            "../../migrations/V002_add_ai_settings.rollback.sql"
        )),
    },
    Migration {
        version: 3,
        description: "add_draft_reply",
        up: include_str!("../../migrations/V003_add_draft_reply.sql"),
        down: Some(include_str!(
            "../../migrations/V003_add_draft_reply.rollback.sql"
        )),
    },
];

pub struct MigrationRunner;

impl MigrationRunner {
    pub fn run(conn: &mut rusqlite::Connection) -> Result<(), rusqlite::Error> {
        run_migrations(conn, MIGRATIONS)
    }
}

fn ensure_migrations_table(conn: &rusqlite::Connection) -> Result<(), rusqlite::Error> {
    conn.execute_batch(
        "CREATE TABLE IF NOT EXISTS schema_migrations (
            version     INTEGER PRIMARY KEY,
            description TEXT    NOT NULL,
            applied_at  TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        );",
    )
}

fn get_max_applied_version(conn: &rusqlite::Connection) -> Result<u32, rusqlite::Error> {
    conn.query_row(
        "SELECT COALESCE(MAX(version), 0) FROM schema_migrations",
        [],
        |row| row.get(0),
    )
}

fn run_migrations(
    conn: &mut rusqlite::Connection,
    migrations: &[Migration],
) -> Result<(), rusqlite::Error> {
    // schema_migrations 테이블은 Migration 외부에서 생성
    // — Migration 실패 후 재시작 시 이력을 읽을 수 있어야 하므로
    ensure_migrations_table(conn)?;

    // MAX(version) 방식: 단일 사용자 앱에서 버전 갭 발생 불가 → 단순성 우선
    let max_version = get_max_applied_version(conn)?;

    for migration in migrations.iter().filter(|m| m.version > max_version) {
        let tx = conn.transaction()?;
        // 실패 시 tx가 drop → 자동 rollback, schema_migrations 기록 없음
        tx.execute_batch(migration.up)?;
        tx.execute(
            "INSERT INTO schema_migrations (version, description) VALUES (?1, ?2)",
            rusqlite::params![migration.version, migration.description],
        )?;
        tx.commit()?;
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use rusqlite::Connection;

    fn in_memory_conn() -> Connection {
        let conn = Connection::open_in_memory().unwrap();
        conn.execute_batch("PRAGMA foreign_keys = ON;").unwrap();
        conn
    }

    // 시나리오 1: 빈 DB → Migration 실행 → schema_migrations 테이블 생성
    #[test]
    fn test_creates_schema_migrations_table() {
        let mut conn = in_memory_conn();
        MigrationRunner::run(&mut conn).unwrap();

        let exists: bool = conn
            .query_row(
                "SELECT COUNT(*) > 0 FROM sqlite_master \
                 WHERE type='table' AND name='schema_migrations'",
                [],
                |row| row.get(0),
            )
            .unwrap();

        assert!(exists, "schema_migrations 테이블이 생성되어야 함");
    }

    // 시나리오 2: V001 적용 → schema_migrations 기록 + 테이블 생성 확인
    #[test]
    fn test_applies_v001_and_records() {
        let mut conn = in_memory_conn();
        MigrationRunner::run(&mut conn).unwrap();

        let (version, description): (u32, String) = conn
            .query_row(
                "SELECT version, description FROM schema_migrations WHERE version = 1",
                [],
                |row| Ok((row.get(0)?, row.get(1)?)),
            )
            .unwrap();

        assert_eq!(version, 1);
        assert_eq!(description, "initial_schema");

        // V001 SQL 실행 결과 검증 (settings 테이블 생성 여부)
        let table_exists: bool = conn
            .query_row(
                "SELECT COUNT(*) > 0 FROM sqlite_master \
                 WHERE type='table' AND name='settings'",
                [],
                |row| row.get(0),
            )
            .unwrap();

        assert!(table_exists, "V001 실행으로 settings 테이블이 생성되어야 함");
    }

    // 시나리오 3: 앱 재시작 시 V001 재적용 없음 (멱등성)
    #[test]
    fn test_idempotent_on_second_run() {
        let mut conn = in_memory_conn();
        MigrationRunner::run(&mut conn).unwrap();
        MigrationRunner::run(&mut conn).unwrap();

        let count: i64 = conn
            .query_row(
                "SELECT COUNT(*) FROM schema_migrations",
                [],
                |row| row.get(0),
            )
            .unwrap();

        assert_eq!(
            count as usize,
            MIGRATIONS.len(),
            "Migration이 중복 적용되지 않아야 함"
        );
    }

    // 시나리오 4: 잘못된 SQL → 트랜잭션 롤백 → schema_migrations 기록 없음
    #[test]
    fn test_failed_migration_rolls_back() {
        const BAD: Migration = Migration {
            version: 999,
            description: "bad",
            up: "THIS IS NOT VALID SQL;",
            down: None,
        };

        let mut conn = in_memory_conn();
        ensure_migrations_table(&conn).unwrap();

        let result = run_migrations(&mut conn, &[BAD]);
        assert!(result.is_err(), "잘못된 SQL은 에러를 반환해야 함");

        let count: i64 = conn
            .query_row(
                "SELECT COUNT(*) FROM schema_migrations WHERE version = 999",
                [],
                |row| row.get(0),
            )
            .unwrap();

        assert_eq!(count, 0, "실패한 Migration은 schema_migrations에 기록되지 않아야 함");
    }
}
