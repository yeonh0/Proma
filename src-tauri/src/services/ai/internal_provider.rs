use reqwest::blocking::Client;
use serde::{Deserialize, Serialize};

use super::provider::{AiError, AiProvider, LlmRequest, LlmResponse};

#[derive(Serialize)]
struct InternalMessage {
    role: String,
    content: String,
}

#[derive(Serialize)]
struct InternalRequest {
    messages: Vec<InternalMessage>,
    temperature: f32,
}

#[derive(Deserialize)]
struct InternalChoiceMessage {
    content: String,
}

#[derive(Deserialize)]
struct InternalChoice {
    message: InternalChoiceMessage,
}

#[derive(Deserialize)]
struct InternalResponse {
    choices: Vec<InternalChoice>,
}

pub struct InternalProvider {
    api_url: String,
    client: Client,
}

impl InternalProvider {
    pub fn new(api_url: &str) -> Self {
        Self {
            api_url: api_url.to_string(),
            client: Client::new(),
        }
    }

    fn call(&self, req: LlmRequest) -> Result<LlmResponse, AiError> {
        let body = InternalRequest {
            messages: vec![
                InternalMessage { role: "system".to_string(), content: req.system_prompt },
                InternalMessage { role: "user".to_string(), content: req.user_prompt },
            ],
            temperature: req.temperature,
        };

        let response = self
            .client
            .post(&self.api_url)
            .json(&body)
            .send()
            .map_err(|e| AiError::Http(e.to_string()))?;

        let api_response: InternalResponse =
            response.json().map_err(|e| AiError::Parse(e.to_string()))?;

        let content = api_response
            .choices
            .into_iter()
            .next()
            .map(|c| c.message.content)
            .ok_or_else(|| AiError::InvalidResponse("응답에 선택지가 없습니다".to_string()))?;

        Ok(LlmResponse { content })
    }
}

impl AiProvider for InternalProvider {
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
