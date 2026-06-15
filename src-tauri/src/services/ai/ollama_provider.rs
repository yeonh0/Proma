use reqwest::blocking::Client;
use serde::{Deserialize, Serialize};

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
    client: Client,
}

impl OllamaProvider {
    pub fn new(base_url: &str, model: &str) -> Self {
        Self {
            base_url: base_url.trim_end_matches('/').to_string(),
            model: model.to_string(),
            client: Client::new(),
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
            .client
            .post(format!("{}/api/chat", self.base_url))
            .json(&body)
            .send()
            .map_err(|e| AiError::Http(e.to_string()))?;

        let chat_response: OllamaChatResponse =
            response.json().map_err(|e| AiError::Parse(e.to_string()))?;

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
