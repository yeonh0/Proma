-- V001: 초기 스키마
-- settings 테이블 및 기본값 삽입
-- 업무 테이블(projects, tasks, emails 등)은 Task 0-8에서 추가 예정

CREATE TABLE IF NOT EXISTS settings (
    key        TEXT PRIMARY KEY,
    value      TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

INSERT OR IGNORE INTO settings (key, value) VALUES
    ('ollama_base_url',    'http://localhost:11434'),
    ('ollama_model',       'llama3'),
    ('app_language',       'ko'),
    ('email_storage_path', '');
