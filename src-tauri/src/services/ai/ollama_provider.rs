use serde::{Deserialize, Serialize};
use std::time::Duration;

use super::provider::{AiError, AiProvider, LlmRequest, LlmResponse};

#[derive(Serialize)]
struct OllamaMessage {
    role: String,
    content: String,
}

#[derive(Serialize)]
struct OllamaOptions {
    temperature: f32,
}

#[derive(Serialize)]
struct OllamaChatRequest {
    model: String,
    messages: Vec<OllamaMessage>,
    options: OllamaOptions,
    stream: bool,
}

#[derive(Deserialize)]
struct OllamaResponseMessage {
    content: String,
}

#[derive(Deserialize)]
struct OllamaChatResponse {
    message: OllamaResponseMessage,
}

pub struct OllamaProvider {
    base_url: String,
    model: String,
    agent: ureq::Agent,
}

impl OllamaProvider {
    pub fn new(base_url: &str, model: &str) -> Self {
        let agent = ureq::AgentBuilder::new()
            .timeout_read(Duration::from_secs(300))
            .timeout_connect(Duration::from_secs(10))
            .build();
        Self {
            base_url: base_url.trim_end_matches('/').to_string(),
            model: model.to_string(),
            agent,
        }
    }

    fn call(&self, req: LlmRequest) -> Result<LlmResponse, AiError> {
        let body = OllamaChatRequest {
            model: self.model.clone(),
            messages: vec![
                OllamaMessage { role: "system".to_string(), content: req.system_prompt },
                OllamaMessage { role: "user".to_string(), content: req.user_prompt },
            ],
            options: OllamaOptions { temperature: req.temperature },
            stream: false,
        };

        let response = self
            .agent
            .post(&format!("{}/api/chat", self.base_url))
            .send_json(&body)
            .map_err(|e| AiError::Http(e.to_string()))?;

        let chat_response: OllamaChatResponse =
            response.into_json().map_err(|e| AiError::Parse(e.to_string()))?;

        Ok(LlmResponse { content: chat_response.message.content })
    }
}

impl AiProvider for OllamaProvider {
    fn summarize(&self, req: LlmRequest) -> Result<LlmResponse, AiError> {
        self.call(req)
    }

    fn classify(&self, req: LlmRequest) -> Result<LlmResponse, AiError> {
        self.call(req)
    }

    fn draft_reply(&self, req: LlmRequest) -> Result<LlmResponse, AiError> {
        self.call(req)
    }
}
