pub mod migration;

use std::path::Path;

pub struct DatabaseManager {
    conn: rusqlite::Connection,
}

#[derive(Debug)]
pub enum DbError {
    Sqlite(rusqlite::Error),
    Io(std::io::Error),
}

impl From<rusqlite::Error> for DbError {
    fn from(e: rusqlite::Error) -> Self {
        DbError::Sqlite(e)
    }
}

impl From<std::io::Error> for DbError {
    fn from(e: std::io::Error) -> Self {
        DbError::Io(e)
    }
}

impl std::fmt::Display for DbError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DbError::Sqlite(e) => write!(f, "SQLite 오류: {}", e),
            DbError::Io(e) => write!(f, "IO 오류: {}", e),
        }
    }
}

impl std::error::Error for DbError {}

impl DatabaseManager {
    pub fn new(path: &Path) -> Result<Self, DbError> {
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent)?;
        }

        let conn = rusqlite::Connection::open(path)?;

        conn.execute_batch(
            "PRAGMA foreign_keys = ON;
             PRAGMA journal_mode = WAL;
             PRAGMA synchronous = NORMAL;",
        )?;

        Ok(Self { conn })
    }

    pub fn run_migrations(&mut self) -> Result<(), rusqlite::Error> {
        migration::MigrationRunner::run(&mut self.conn)
    }

    pub fn connection(&self) -> &rusqlite::Connection {
        &self.conn
    }

    pub fn connection_mut(&mut self) -> &mut rusqlite::Connection {
        &mut self.conn
    }
}
