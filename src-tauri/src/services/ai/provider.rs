use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug, Serialize, Deserialize)]
pub struct LlmRequest {
    pub system_prompt: String,
    pub user_prompt: String,
    pub temperature: f32,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct LlmResponse {
    pub content: String,
}

#[derive(Debug)]
pub enum AiError {
    Http(String),
    Parse(String),
    InvalidResponse(String),
}

impl fmt::Display for AiError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AiError::Http(e) => write!(f, "HTTP 오류: {e}"),
            AiError::Parse(e) => write!(f, "파싱 오류: {e}"),
            AiError::InvalidResponse(e) => write!(f, "응답 형식 오류: {e}"),
        }
    }
}

impl std::error::Error for AiError {}

pub trait AiProvider: Send + Sync {
    fn summarize(&self, req: LlmRequest) -> Result<LlmResponse, AiError>;
    fn classify(&self, req: LlmRequest) -> Result<LlmResponse, AiError>;
    fn draft_reply(&self, req: LlmRequest) -> Result<LlmResponse, AiError>;
}
