use tauri::State;

use crate::models::project::{CreateProjectRequest, Project, UpdateProjectRequest};
use crate::repository::project as repo;
use crate::AppState;

#[tauri::command]
pub fn project_create(state: State<AppState>, req: CreateProjectRequest) -> Result<Project, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::create(db.connection(), &req).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn project_list(state: State<AppState>) -> Result<Vec<Project>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::list(db.connection()).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn project_get(state: State<AppState>, id: i64) -> Result<Option<Project>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::get(db.connection(), id).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn project_update(
    state: State<AppState>,
    id: i64,
    req: UpdateProjectRequest,
) -> Result<Project, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::update(db.connection(), id, &req).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn project_delete(state: State<AppState>, id: i64) -> Result<bool, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::delete(db.connection(), id).map_err(|e| e.to_string())
}
