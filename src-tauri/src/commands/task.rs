use tauri::State;

use crate::models::task::{CreateTaskRequest, Task, UpdateTaskRequest};
use crate::repository::task as repo;
use crate::AppState;

#[tauri::command]
pub fn task_create(state: State<AppState>, req: CreateTaskRequest) -> Result<Task, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::create(db.connection(), &req).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn task_list(state: State<AppState>, project_id: i64) -> Result<Vec<Task>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::list_by_project(db.connection(), project_id).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn task_get(state: State<AppState>, id: i64) -> Result<Option<Task>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::get(db.connection(), id).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn task_update(state: State<AppState>, id: i64, req: UpdateTaskRequest) -> Result<Task, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::update(db.connection(), id, &req).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn task_delete(state: State<AppState>, id: i64) -> Result<bool, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::delete(db.connection(), id).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn task_list_all(state: State<AppState>) -> Result<Vec<Task>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::list_all(db.connection()).map_err(|e| e.to_string())
}
