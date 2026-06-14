mod commands;
mod db;
mod models;
mod repository;
mod services;

use std::sync::Mutex;
use tauri::Manager;

pub struct AppState {
    pub db: Mutex<db::DatabaseManager>,
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            let db_path = app
                .path()
                .app_data_dir()?
                .join("data.db");

            let mut db = db::DatabaseManager::new(&db_path)?;
            db.run_migrations()?;

            app.manage(AppState {
                db: Mutex::new(db),
            });

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            greet,
            commands::project::project_create,
            commands::project::project_list,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
