mod commands;
mod db;
mod models;
mod repository;
mod services;

use std::path::PathBuf;
use std::sync::Mutex;
use tauri::Manager;

pub struct AppState {
    pub db: Mutex<db::DatabaseManager>,
    pub app_data_dir: PathBuf,
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .setup(|app| {
            let app_data_dir = app.path().app_data_dir()?;
            let db_path = app_data_dir.join("data.db");

            let mut db = db::DatabaseManager::new(&db_path)?;
            db.run_migrations()?;

            app.manage(AppState {
                db: Mutex::new(db),
                app_data_dir,
            });

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            greet,
            commands::project::project_create,
            commands::project::project_list,
            commands::project::project_get,
            commands::project::project_update,
            commands::project::project_delete,
            commands::task::task_create,
            commands::task::task_list,
            commands::task::task_list_all,
            commands::task::task_get,
            commands::task::task_update,
            commands::task::task_delete,
            commands::schedule::schedule_create,
            commands::schedule::schedule_list,
            commands::schedule::schedule_get,
            commands::schedule::schedule_update,
            commands::schedule::schedule_delete,
            commands::email::email_import,
            commands::email::email_list,
            commands::email::email_get,
            commands::email::email_delete,
            commands::email::email_delete_all,
            commands::email::email_link_project,
            commands::email::email_unlink_project,
            commands::email::email_list_project_ids,
            commands::settings::settings_get,
            commands::settings::settings_set,
            commands::settings::settings_get_all,
            commands::ai::email_analyze,
            commands::ai::email_list_ai_results,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
