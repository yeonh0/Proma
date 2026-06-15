use tauri::State;

use crate::models::ai_result::AiResult;
use crate::repository::{ai_result as ai_repo, email as email_repo, settings as settings_repo};
use crate::services::ai::{AiProviderFactory, LlmRequest};
use crate::AppState;

#[tauri::command]
pub async fn email_analyze(
    state: State<'_, AppState>,
    email_id: i64,
    analysis_type: String,
) -> Result<AiResult, String> {
    let (result_type, system_prompt) = match analysis_type.as_str() {
        "summary" => (
            "summary",
            "이메일 내용을 핵심만 3-5문장으로 요약하라. 반드시 한국어로 답하라.",
        ),
        "classification" => (
            "classification",
            "이메일의 종류를 분류하라. (업무 요청 / 정보 공유 / 뉴스레터 / 알림 / 기타) 중 하나를 선택하고 한 줄 이유를 한국어로 답하라.",
        ),
        "draft_reply" => (
            "draft_reply",
            "이 이메일에 대한 짧고 전문적인 한국어 답장 초안을 작성하라. 수신인 이름은 [이름] 형태로 표시하라.",
        ),
        _ => return Err(format!("알 수 없는 분석 유형: {analysis_type}")),
    };

    // DB 조회 — MutexGuard를 await 이전에 drop
    let (body, settings, model_name) = {
        let db = state.db.lock().map_err(|e| e.to_string())?;
        let conn = db.connection();

        let email = email_repo::get(conn, email_id)
            .map_err(|e| e.to_string())?
            .ok_or_else(|| format!("이메일 #{email_id}을 찾을 수 없습니다"))?;

        let body = email
            .body_text
            .filter(|s| !s.trim().is_empty())
            .ok_or_else(|| "이메일 본문이 없어 AI 분석을 수행할 수 없습니다".to_string())?;

        let settings = settings_repo::get_all(conn).map_err(|e| e.to_string())?;

        let model_name = match settings.ai_provider.as_str() {
            "internal" => "internal".to_string(),
            _ => format!("ollama/{}", settings.ollama_model),
        };

        (body, settings, model_name)
    }; // MutexGuard 여기서 drop

    // AI HTTP 호출 — blocking reqwest를 spawn_blocking으로 격리
    let system_prompt_owned = system_prompt.to_string();
    let body_for_ai = body.clone();
    let analysis_type_clone = analysis_type.clone();

    let response_content = tokio::task::spawn_blocking(move || {
        let provider = AiProviderFactory::from_settings(
            &settings.ai_provider,
            &settings.ollama_base_url,
            &settings.ollama_model,
            &settings.internal_api_url,
        );

        let llm_req = LlmRequest {
            system_prompt: system_prompt_owned,
            user_prompt: body_for_ai,
            temperature: 0.7,
        };

        let result = match analysis_type_clone.as_str() {
            "summary" => provider.summarize(llm_req),
            "classification" => provider.classify(llm_req),
            "draft_reply" => provider.draft_reply(llm_req),
            _ => unreachable!(),
        };

        result.map(|r| r.content).map_err(|e| e.to_string())
    })
    .await
    .map_err(|e| e.to_string())??;

    // 결과 저장 — 새로 MutexGuard 획득
    let db = state.db.lock().map_err(|e| e.to_string())?;
    let params = ai_repo::CreateAiResultParams {
        source_type: "email",
        source_id: email_id,
        result_type,
        model_name: &model_name,
        prompt: Some(&body),
        result: &response_content,
    };

    ai_repo::create(db.connection(), &params).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn email_list_ai_results(
    state: State<AppState>,
    email_id: i64,
) -> Result<Vec<AiResult>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    ai_repo::list_by_source(db.connection(), "email", email_id).map_err(|e| e.to_string())
}
