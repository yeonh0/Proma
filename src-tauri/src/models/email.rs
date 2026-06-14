use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Email {
    pub id: i64,
    pub message_id: Option<String>,
    pub subject: Option<String>,
    pub sender: Option<String>,
    pub recipients: Option<String>,
    pub cc: Option<String>,
    pub body_text: Option<String>,
    pub body_html: Option<String>,
    pub sent_at: Option<String>,
    pub imported_at: String,
    pub file_path: Option<String>,
    pub created_at: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct EmailAttachment {
    pub id: i64,
    pub email_id: i64,
    pub filename: String,
    pub content_type: Option<String>,
    pub size_bytes: Option<i64>,
    pub file_path: Option<String>,
    pub created_at: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct EmailProjectMapping {
    pub id: i64,
    pub email_id: i64,
    pub project_id: i64,
    pub mapped_by: String,
    pub is_confirmed: bool,
    pub confidence: Option<f64>,
    pub created_at: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct EmailWithMeta {
    pub email: Email,
    pub attachments: Vec<EmailAttachment>,
    pub project_ids: Vec<i64>,
}
