use tauri::State;

use crate::models::settings::AppSettings;
use crate::repository::settings as repo;
use crate::AppState;

#[tauri::command]
pub fn settings_get(state: State<AppState>, key: String) -> Result<Option<String>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::get(db.connection(), &key).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn settings_set(state: State<AppState>, key: String, value: String) -> Result<(), String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::set(db.connection(), &key, &value).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn settings_get_all(state: State<AppState>) -> Result<AppSettings, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::get_all(db.connection()).map_err(|e| e.to_string())
}
