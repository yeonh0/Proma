use tauri::State;

use crate::models::email::{Email, EmailProjectMapping, EmailWithMeta};
use crate::repository::email as repo;
use crate::services::email_parser;
use crate::AppState;

#[tauri::command]
pub fn email_import(state: State<AppState>, file_path: String) -> Result<Email, String> {
    let raw = std::fs::read(&file_path).map_err(|e| format!("파일 읽기 오류: {e}"))?;
    let parsed = email_parser::parse_eml(&raw)?;

    let app_data_dir = state.app_data_dir.clone();
    let db = state.db.lock().map_err(|e| e.to_string())?;
    let conn = db.connection();

    // 중복 체크 (message_id 기준)
    if let Some(mid) = &parsed.message_id {
        if let Ok(Some(existing)) = repo::get_by_message_id(conn, mid) {
            return Ok(existing);
        }
    }

    let recipients_json = serde_json::to_string(&parsed.recipients).ok();
    let cc_json = if parsed.cc.is_empty() {
        None
    } else {
        serde_json::to_string(&parsed.cc).ok()
    };

    let params = repo::CreateEmailParams {
        message_id: parsed.message_id.as_deref(),
        subject: parsed.subject.as_deref(),
        sender: parsed.sender.as_deref(),
        recipients_json: recipients_json.as_deref(),
        cc_json: cc_json.as_deref(),
        body_text: parsed.body_text.as_deref(),
        body_html: parsed.body_html.as_deref(),
        sent_at: parsed.sent_at.as_deref(),
        file_path: Some(&file_path),
    };

    let email = repo::create(conn, &params).map_err(|e| e.to_string())?;

    // 첨부파일 저장
    let saved = email_parser::save_attachments(email.id, &parsed.attachments, &app_data_dir);
    for (filename, content_type, size_bytes) in saved {
        let att_path = app_data_dir
            .join("attachments")
            .join(email.id.to_string())
            .join(&filename)
            .to_string_lossy()
            .to_string();
        let _ = repo::create_attachment(conn, email.id, &filename, &content_type, size_bytes, &att_path);
    }

    Ok(email)
}

#[tauri::command]
pub fn email_list(state: State<AppState>) -> Result<Vec<Email>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::list(db.connection()).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn email_get(state: State<AppState>, id: i64) -> Result<Option<EmailWithMeta>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    let conn = db.connection();
    let Some(email) = repo::get(conn, id).map_err(|e| e.to_string())? else {
        return Ok(None);
    };
    let attachments = repo::list_attachments(conn, id).map_err(|e| e.to_string())?;
    let project_ids = repo::list_project_ids(conn, id).map_err(|e| e.to_string())?;
    Ok(Some(EmailWithMeta { email, attachments, project_ids }))
}

#[tauri::command]
pub fn email_delete(state: State<AppState>, id: i64) -> Result<bool, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::delete(db.connection(), id).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn email_link_project(state: State<AppState>, email_id: i64, project_id: i64) -> Result<EmailProjectMapping, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::link_project(db.connection(), email_id, project_id).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn email_unlink_project(state: State<AppState>, email_id: i64, project_id: i64) -> Result<bool, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::unlink_project(db.connection(), email_id, project_id).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn email_list_project_ids(state: State<AppState>, email_id: i64) -> Result<Vec<i64>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    repo::list_project_ids(db.connection(), email_id).map_err(|e| e.to_string())
}
