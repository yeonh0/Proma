use rusqlite::{params, Connection};

use crate::models::ai_result::AiResult;

pub struct CreateAiResultParams<'a> {
    pub source_type: &'a str,
    pub source_id: i64,
    pub result_type: &'a str,
    pub model_name: &'a str,
    pub prompt: Option<&'a str>,
    pub result: &'a str,
}

const SELECT_COLS: &str =
    "id, source_type, source_id, result_type, model_name, prompt, result, is_applied, created_at";

fn map_row(row: &rusqlite::Row) -> rusqlite::Result<AiResult> {
    Ok(AiResult {
        id: row.get(0)?,
        source_type: row.get(1)?,
        source_id: row.get(2)?,
        result_type: row.get(3)?,
        model_name: row.get(4)?,
        prompt: row.get(5)?,
        result: row.get(6)?,
        is_applied: row.get::<_, i64>(7)? != 0,
        created_at: row.get(8)?,
    })
}

pub fn create(conn: &Connection, p: &CreateAiResultParams) -> rusqlite::Result<AiResult> {
    conn.execute(
        "INSERT INTO ai_results (source_type, source_id, result_type, model_name, prompt, result)
         VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
        params![p.source_type, p.source_id, p.result_type, p.model_name, p.prompt, p.result],
    )?;
    let id = conn.last_insert_rowid();
    let sql = format!("SELECT {SELECT_COLS} FROM ai_results WHERE id = ?1");
    let mut stmt = conn.prepare(&sql)?;
    let mut rows = stmt.query_map([id], map_row)?;
    rows.next().transpose()?.ok_or(rusqlite::Error::QueryReturnedNoRows)
}

pub fn list_by_source(
    conn: &Connection,
    source_type: &str,
    source_id: i64,
) -> rusqlite::Result<Vec<AiResult>> {
    let sql = format!(
        "SELECT {SELECT_COLS} FROM ai_results
         WHERE source_type = ?1 AND source_id = ?2
         ORDER BY created_at DESC"
    );
    let mut stmt = conn.prepare(&sql)?;
    let rows = stmt.query_map(params![source_type, source_id], map_row)?;
    rows.collect()
}
