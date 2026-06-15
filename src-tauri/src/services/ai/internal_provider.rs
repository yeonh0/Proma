use serde::{Deserialize, Serialize};
use std::time::Duration;

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
    agent: ureq::Agent,
}

impl InternalProvider {
    pub fn new(api_url: &str) -> Self {
        let agent = ureq::AgentBuilder::new()
            .timeout_read(Duration::from_secs(300))
            .timeout_connect(Duration::from_secs(10))
            .build();
        Self {
            api_url: api_url.to_string(),
            agent,
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
            .agent
            .post(&self.api_url)
            .send_json(&body)
            .map_err(|e| AiError::Http(e.to_string()))?;

        let api_response: InternalResponse =
            response.into_json().map_err(|e| AiError::Parse(e.to_string()))?;

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
