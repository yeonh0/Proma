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
    workspace_id: String,
    headers: Vec<(String, String)>,
    agent: ureq::Agent,
}

impl InternalProvider {
    pub fn new(api_url: &str, raw_headers: &str, workspace_id: &str) -> Self {
        let agent = ureq::AgentBuilder::new()
            .timeout_read(Duration::from_secs(300))
            .timeout_connect(Duration::from_secs(10))
            .build();
        Self {
            api_url: api_url.to_string(),
            workspace_id: workspace_id.to_string(),
            headers: Self::parse_headers(raw_headers),
            agent,
        }
    }

    /// "Key: Value" 형식과 Python 교대 줄(홀수=키, 짝수=값) 형식 모두 지원.
    /// DevTools General 섹션 메타데이터(Request URL, Status Code 등)는 키에 공백이 있어
    /// 유효한 HTTP 헤더가 아니므로 자동으로 제외한다.
    fn parse_headers(raw: &str) -> Vec<(String, String)> {
        let lines: Vec<&str> = raw.trim().lines().map(str::trim).filter(|l| !l.is_empty()).collect();
        if lines.is_empty() {
            return vec![];
        }

        let pairs: Vec<(String, String)> = if lines[0].contains(':') {
            // "Key: Value" 형식
            lines
                .iter()
                .filter_map(|line| {
                    let idx = line.find(':')?;
                    let key = line[..idx].trim().to_string();
                    let value = line[idx + 1..].trim().to_string();
                    if key.is_empty() { None } else { Some((key, value)) }
                })
                .collect()
        } else {
            // Python raw_headers 교대 줄 형식 (짝수=키, 홀수=값)
            lines
                .chunks(2)
                .filter_map(|chunk| {
                    if chunk.len() == 2 {
                        Some((chunk[0].to_string(), chunk[1].to_string()))
                    } else {
                        None
                    }
                })
                .collect()
        };

        // 키에 공백이 있는 항목은 HTTP 헤더가 아닌 DevTools 메타데이터이므로 제외
        pairs.into_iter().filter(|(key, _)| !key.contains(' ')).collect()
    }

    fn call(&self, req: LlmRequest) -> Result<LlmResponse, AiError> {
        let query = format!("{}\n\n{}", req.system_prompt, req.user_prompt);

        let payload = InternalPayload {
            agent_key: "free_GPT_OSS".to_string(),
            is_stream: "true".to_string(),
            query,
            workspace_id: self.workspace_id.clone(),
        };

        let mut ureq_req = self.agent.post(&self.api_url);
        for (key, value) in &self.headers {
            ureq_req = ureq_req.set(key, value);
        }

        let response = ureq_req
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
