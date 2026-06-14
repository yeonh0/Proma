use tauri::State;

use crate::models::schedule::{CreateScheduleRequest, Schedule, UpdateScheduleRequest};
use crate::repository::schedule as repo;
use crate::AppState;

#[tauri::command]
pub fn schedule_create(state: State<AppState>, req: CreateScheduleRequest) -> Result<Schedule, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::create(db.connection(), &req).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn schedule_list(state: State<AppState>) -> Result<Vec<Schedule>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::list(db.connection()).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn schedule_get(state: State<AppState>, id: i64) -> Result<Option<Schedule>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::get(db.connection(), id).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn schedule_update(state: State<AppState>, id: i64, req: UpdateScheduleRequest) -> Result<Schedule, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::update(db.connection(), id, &req).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn schedule_delete(state: State<AppState>, id: i64) -> Result<bool, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::delete(db.connection(), id).map_err(|e| e.to_string())
}
