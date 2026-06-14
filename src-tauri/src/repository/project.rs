use rusqlite::{params, Connection};

use crate::models::project::{CreateProjectRequest, Project};

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
    find_by_id(conn, id)?.ok_or(rusqlite::Error::QueryReturnedNoRows)
}

pub fn list(conn: &Connection) -> rusqlite::Result<Vec<Project>> {
    let sql = format!(
        "SELECT {SELECT_COLS} FROM projects ORDER BY created_at DESC"
    );
    let mut stmt = conn.prepare(&sql)?;
    let rows = stmt.query_map([], map_row)?;
    rows.collect()
}

fn find_by_id(conn: &Connection, id: i64) -> rusqlite::Result<Option<Project>> {
    let sql = format!(
        "SELECT {SELECT_COLS} FROM projects WHERE id = ?1"
    );
    let mut stmt = conn.prepare(&sql)?;
    let mut rows = stmt.query_map([id], map_row)?;
    rows.next().transpose()
}
