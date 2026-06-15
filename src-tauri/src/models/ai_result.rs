use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct AiResult {
    pub id: i64,
    pub source_type: String,
    pub source_id: i64,
    pub result_type: String,
    pub model_name: String,
    pub prompt: Option<String>,
    pub result: String,
    pub is_applied: bool,
    pub created_at: String,
}
