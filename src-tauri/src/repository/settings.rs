use rusqlite::{params, Connection};

use crate::models::settings::AppSettings;

pub fn get(conn: &Connection, key: &str) -> rusqlite::Result<Option<String>> {
    let mut stmt = conn.prepare("SELECT value FROM settings WHERE key = ?1")?;
    let mut rows = stmt.query_map([key], |row| row.get(0))?;
    rows.next().transpose()
}

pub fn set(conn: &Connection, key: &str, value: &str) -> rusqlite::Result<()> {
    conn.execute(
        "INSERT INTO settings (key, value, updated_at)
         VALUES (?1, ?2, datetime('now', 'localtime'))
         ON CONFLICT(key) DO UPDATE SET
             value      = excluded.value,
             updated_at = excluded.updated_at",
        params![key, value],
    )?;
    Ok(())
}

pub fn get_all(conn: &Connection) -> rusqlite::Result<AppSettings> {
    fn get_or(conn: &Connection, key: &str, default: &str) -> rusqlite::Result<String> {
        Ok(get(conn, key)?.unwrap_or_else(|| default.to_string()))
    }

    Ok(AppSettings {
        ollama_base_url:    get_or(conn, "ollama_base_url",    "http://localhost:11434")?,
        ollama_model:       get_or(conn, "ollama_model",       "llama3")?,
        app_language:       get_or(conn, "app_language",       "ko")?,
        email_storage_path: get_or(conn, "email_storage_path", "")?,
        ai_provider:        get_or(conn, "ai_provider",        "ollama")?,
        internal_api_url:   get_or(conn, "internal_api_url",   "http://localhost:8080/api/ai")?,
    })
}
