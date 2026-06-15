-- V002 롤백: AI 제공자 설정 제거

DELETE FROM settings WHERE key IN ('ai_provider', 'internal_api_url');
