use rusqlite::{params, Connection};

use crate::models::task::{CreateTaskRequest, Task, UpdateTaskRequest};

const SELECT_COLS: &str =
    "id, project_id, title, description, status, priority, due_date, completed_at, created_at, updated_at";

fn map_row(row: &rusqlite::Row) -> rusqlite::Result<Task> {
    Ok(Task {
        id: row.get(0)?,
        project_id: row.get(1)?,
        title: row.get(2)?,
        description: row.get(3)?,
        status: row.get(4)?,
        priority: row.get(5)?,
        due_date: row.get(6)?,
        completed_at: row.get(7)?,
        created_at: row.get(8)?,
        updated_at: row.get(9)?,
    })
}

pub fn create(conn: &Connection, req: &CreateTaskRequest) -> rusqlite::Result<Task> {
    let status = req.status.as_deref().unwrap_or("todo");
    let priority = req.priority.as_deref().unwrap_or("medium");

    conn.execute(
        "INSERT INTO tasks (project_id, title, description, status, priority, due_date)
         VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
        params![req.project_id, req.title, req.description, status, priority, req.due_date],
    )?;

    let id = conn.last_insert_rowid();
    get(conn, id)?.ok_or(rusqlite::Error::QueryReturnedNoRows)
}

pub fn list_by_project(conn: &Connection, project_id: i64) -> rusqlite::Result<Vec<Task>> {
    let sql = format!(
        "SELECT {SELECT_COLS} FROM tasks WHERE project_id = ?1 ORDER BY created_at ASC"
    );
    let mut stmt = conn.prepare(&sql)?;
    let rows = stmt.query_map([project_id], map_row)?;
    rows.collect()
}

pub fn list_all(conn: &Connection) -> rusqlite::Result<Vec<Task>> {
    let sql = format!(
        "SELECT {SELECT_COLS} FROM tasks
         ORDER BY due_date ASC NULLS LAST, created_at ASC"
    );
    let mut stmt = conn.prepare(&sql)?;
    let rows = stmt.query_map([], map_row)?;
    rows.collect()
}

pub fn get(conn: &Connection, id: i64) -> rusqlite::Result<Option<Task>> {
    let sql = format!("SELECT {SELECT_COLS} FROM tasks WHERE id = ?1");
    let mut stmt = conn.prepare(&sql)?;
    let mut rows = stmt.query_map([id], map_row)?;
    rows.next().transpose()
}

pub fn update(conn: &Connection, id: i64, req: &UpdateTaskRequest) -> rusqlite::Result<Task> {
    let affected = conn.execute(
        "UPDATE tasks SET
             title        = ?1,
             description  = ?2,
             status       = ?3,
             priority     = ?4,
             due_date     = ?5,
             completed_at = ?6,
             updated_at   = datetime('now', 'localtime')
         WHERE id = ?7",
        params![
            req.title, req.description, req.status, req.priority,
            req.due_date, req.completed_at, id,
        ],
    )?;

    if affected == 0 {
        return Err(rusqlite::Error::QueryReturnedNoRows);
    }
    get(conn, id)?.ok_or(rusqlite::Error::QueryReturnedNoRows)
}

pub fn delete(conn: &Connection, id: i64) -> rusqlite::Result<bool> {
    let affected = conn.execute("DELETE FROM tasks WHERE id = ?1", [id])?;
    Ok(affected > 0)
}
