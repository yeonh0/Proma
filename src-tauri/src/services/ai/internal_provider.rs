use serde::{Deserialize, Serialize};
use std::time::Duration;

use super::provider::{AiError, AiProvider, LlmRequest, LlmResponse};

#[derive(Serialize)]
struct InternalPayload {
    agent_key: String,
    is_stream: String,
    query: String,
    workspace_id: String,
}

#[derive(Deserialize)]
struct SseChunk {
    llm_result: Option<LlmResult>,
}

#[derive(Deserialize)]
struct LlmResult {
    answer: Option<String>,
}

pub struct InternalProvider {
    api_url: String,
    token: String,
    workspace_id: String,
    agent: ureq::Agent,
}

impl InternalProvider {
    pub fn new(api_url: &str, token: &str, workspace_id: &str) -> Self {
        let agent = ureq::AgentBuilder::new()
            .timeout_read(Duration::from_secs(300))
            .timeout_connect(Duration::from_secs(10))
            .build();
        Self {
            api_url: api_url.to_string(),
            token: token.to_string(),
            workspace_id: workspace_id.to_string(),
            agent,
        }
    }

    fn call(&self, req: LlmRequest) -> Result<LlmResponse, AiError> {
        let query = format!("{}\n\n{}", req.system_prompt, req.user_prompt);

        let payload = InternalPayload {
            agent_key: "free_GPT_OSS".to_string(),
            is_stream: "true".to_string(),
            query,
            workspace_id: self.workspace_id.clone(),
        };

        let response = self
            .agent
            .post(&self.api_url)
            .set("Content-Type", "application/json")
            .set("Authorization", &format!("Bearer {}", self.token))
            .send_json(&payload)
            .map_err(|e| AiError::Http(e.to_string()))?;

        let body = response.into_string().map_err(|e| AiError::Parse(e.to_string()))?;

        Self::parse_sse(&body)
    }

    fn parse_sse(body: &str) -> Result<LlmResponse, AiError> {
        let mut full_answer = String::new();

        for line in body.lines() {
            if let Some(json_str) = line.strip_prefix("data:") {
                let json_str = json_str.trim();
                if json_str.is_empty() || json_str == "[DONE]" {
                    continue;
                }
                if let Ok(chunk) = serde_json::from_str::<SseChunk>(json_str) {
                    if let Some(answer) = chunk.llm_result.and_then(|r| r.answer) {
                        full_answer.push_str(&answer);
                    }
                }
            }
        }

        if full_answer.is_empty() {
            Err(AiError::InvalidResponse("응답에서 텍스트를 추출할 수 없습니다".to_string()))
        } else {
            Ok(LlmResponse { content: full_answer })
        }
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
