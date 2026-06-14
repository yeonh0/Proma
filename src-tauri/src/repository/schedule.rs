use rusqlite::{params, Connection};

use crate::models::schedule::{CreateScheduleRequest, Schedule, UpdateScheduleRequest};

const SELECT_COLS: &str =
    "id, project_id, title, description, scheduled_at, duration_minutes, is_recurring, recurrence_rule, created_at, updated_at";

fn map_row(row: &rusqlite::Row) -> rusqlite::Result<Schedule> {
    Ok(Schedule {
        id: row.get(0)?,
        project_id: row.get(1)?,
        title: row.get(2)?,
        description: row.get(3)?,
        scheduled_at: row.get(4)?,
        duration_minutes: row.get(5)?,
        is_recurring: row.get(6)?,
        recurrence_rule: row.get(7)?,
        created_at: row.get(8)?,
        updated_at: row.get(9)?,
    })
}

pub fn create(conn: &Connection, req: &CreateScheduleRequest) -> rusqlite::Result<Schedule> {
    let is_recurring = req.is_recurring.unwrap_or(false);
    conn.execute(
        "INSERT INTO schedules
             (project_id, title, description, scheduled_at, duration_minutes, is_recurring, recurrence_rule)
         VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
        params![
            req.project_id, req.title, req.description, req.scheduled_at,
            req.duration_minutes, is_recurring, req.recurrence_rule,
        ],
    )?;
    let id = conn.last_insert_rowid();
    get(conn, id)?.ok_or(rusqlite::Error::QueryReturnedNoRows)
}

pub fn list(conn: &Connection) -> rusqlite::Result<Vec<Schedule>> {
    let sql = format!("SELECT {SELECT_COLS} FROM schedules ORDER BY scheduled_at ASC");
    let mut stmt = conn.prepare(&sql)?;
    let rows = stmt.query_map([], map_row)?;
    rows.collect()
}

pub fn get(conn: &Connection, id: i64) -> rusqlite::Result<Option<Schedule>> {
    let sql = format!("SELECT {SELECT_COLS} FROM schedules WHERE id = ?1");
    let mut stmt = conn.prepare(&sql)?;
    let mut rows = stmt.query_map([id], map_row)?;
    rows.next().transpose()
}

pub fn update(conn: &Connection, id: i64, req: &UpdateScheduleRequest) -> rusqlite::Result<Schedule> {
    let affected = conn.execute(
        "UPDATE schedules SET
             project_id       = ?1,
             title            = ?2,
             description      = ?3,
             scheduled_at     = ?4,
             duration_minutes = ?5,
             is_recurring     = ?6,
             recurrence_rule  = ?7,
             updated_at       = datetime('now', 'localtime')
         WHERE id = ?8",
        params![
            req.project_id, req.title, req.description, req.scheduled_at,
            req.duration_minutes, req.is_recurring, req.recurrence_rule, id,
        ],
    )?;
    if affected == 0 {
        return Err(rusqlite::Error::QueryReturnedNoRows);
    }
    get(conn, id)?.ok_or(rusqlite::Error::QueryReturnedNoRows)
}

pub fn delete(conn: &Connection, id: i64) -> rusqlite::Result<bool> {
    let affected = conn.execute("DELETE FROM schedules WHERE id = ?1", [id])?;
    Ok(affected > 0)
}
