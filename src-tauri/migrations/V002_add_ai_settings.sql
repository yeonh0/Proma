-- V002: AI 제공자 설정 추가
-- ai_provider: 사용할 AI 제공자 ('ollama' | 'internal')
-- internal_api_url: 사내 AI 서버 엔드포인트 (InternalProvider 전용)

INSERT OR IGNORE INTO settings (key, value) VALUES
    ('ai_provider',      'ollama'),
    ('internal_api_url', 'http://localhost:8080/api/ai');
