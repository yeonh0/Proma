use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct AppSettings {
    pub ollama_base_url: String,
    pub ollama_model: String,
    pub app_language: String,
    pub email_storage_path: String,
    pub ai_provider: String,
    pub internal_api_url: String,
}
