use tauri::State;

use crate::models::project::{CreateProjectRequest, Project};
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
