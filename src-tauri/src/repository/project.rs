use rusqlite::{params, Connection};

use crate::models::project::{CreateProjectRequest, Project, UpdateProjectRequest};

const SELECT_COLS: &str =
    "id, parent_id, title, description, status, priority, start_date, due_date, completed_at, created_at, updated_at";

fn map_row(row: &rusqlite::Row) -> rusqlite::Result<Project> {
    Ok(Project {
        id: row.get(0)?,
        parent_id: row.get(1)?,
        title: row.get(2)?,
        description: row.get(3)?,
        status: row.get(4)?,
        priority: row.get(5)?,
        start_date: row.get(6)?,
        due_date: row.get(7)?,
        completed_at: row.get(8)?,
        created_at: row.get(9)?,
        updated_at: row.get(10)?,
    })
}

pub fn create(conn: &Connection, req: &CreateProjectRequest) -> rusqlite::Result<Project> {
    let status = req.status.as_deref().unwrap_or("active");
    let priority = req.priority.as_deref().unwrap_or("medium");

    conn.execute(
        "INSERT INTO projects (parent_id, title, description, status, priority, start_date, due_date)
         VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
        params![
            req.parent_id,
            req.title,
            req.description,
            status,
            priority,
            req.start_date,
            req.due_date,
        ],
    )?;

    let id = conn.last_insert_rowid();
    get(conn, id)?.ok_or(rusqlite::Error::QueryReturnedNoRows)
}

pub fn list(conn: &Connection) -> rusqlite::Result<Vec<Project>> {
    let sql = format!(
        "SELECT {SELECT_COLS} FROM projects ORDER BY created_at DESC"
    );
    let mut stmt = conn.prepare(&sql)?;
    let rows = stmt.query_map([], map_row)?;
    rows.collect()
}

pub fn get(conn: &Connection, id: i64) -> rusqlite::Result<Option<Project>> {
    let sql = format!("SELECT {SELECT_COLS} FROM projects WHERE id = ?1");
    let mut stmt = conn.prepare(&sql)?;
    let mut rows = stmt.query_map([id], map_row)?;
    rows.next().transpose()
}

pub fn update(conn: &Connection, id: i64, req: &UpdateProjectRequest) -> rusqlite::Result<Project> {
    let affected = conn.execute(
        "UPDATE projects SET
             parent_id    = ?1,
             title        = ?2,
             description  = ?3,
             status       = ?4,
             priority     = ?5,
             start_date   = ?6,
             due_date     = ?7,
             completed_at = ?8,
             updated_at   = datetime('now', 'localtime')
         WHERE id = ?9",
        params![
            req.parent_id,
            req.title,
            req.description,
            req.status,
            req.priority,
            req.start_date,
            req.due_date,
            req.completed_at,
            id,
        ],
    )?;

    if affected == 0 {
        return Err(rusqlite::Error::QueryReturnedNoRows);
    }
    get(conn, id)?.ok_or(rusqlite::Error::QueryReturnedNoRows)
}

pub fn delete(conn: &Connection, id: i64) -> rusqlite::Result<bool> {
    let affected = conn.execute("DELETE FROM projects WHERE id = ?1", [id])?;
    Ok(affected > 0)
}

