-- V001: 초기 스키마 (전체 업무 테이블)
-- schema_migrations 테이블은 MigrationRunner가 별도 관리 (이 파일에서 제외)
-- 테이블 생성 순서: FK 참조 대상 → 참조 테이블 순

-- ─────────────────────────────────────────────
-- 앱 설정
-- ─────────────────────────────────────────────

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

-- ─────────────────────────────────────────────
-- 프로젝트
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS projects (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id    INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    -- NULL: 최상위 프로젝트 / NOT NULL: 세부 프로젝트 (depth ≤ 2, 앱 레벨 강제)
    title        TEXT    NOT NULL,
    description  TEXT,
    status       TEXT    NOT NULL DEFAULT 'active'
                     CHECK (status IN ('active', 'paused', 'completed', 'archived')),
    priority     TEXT    NOT NULL DEFAULT 'medium'
                     CHECK (priority IN ('low', 'medium', 'high')),
    start_date   TEXT,
    due_date     TEXT,
    completed_at TEXT,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ─────────────────────────────────────────────
-- Task
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS tasks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id   INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title        TEXT    NOT NULL,
    description  TEXT,
    status       TEXT    NOT NULL DEFAULT 'todo'
                     CHECK (status IN ('todo', 'in_progress', 'done')),
    priority     TEXT    NOT NULL DEFAULT 'medium'
                     CHECK (priority IN ('low', 'medium', 'high')),
    due_date     TEXT,
    completed_at TEXT,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ─────────────────────────────────────────────
-- 일정
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS schedules (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id       INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    title            TEXT    NOT NULL,
    description      TEXT,
    scheduled_at     TEXT    NOT NULL,
    duration_minutes INTEGER,
    is_recurring     INTEGER NOT NULL DEFAULT 0
                         CHECK (is_recurring IN (0, 1)),
    recurrence_rule  TEXT
                         CHECK (recurrence_rule IS NULL
                                OR recurrence_rule IN ('daily', 'weekly', 'monthly')),
    created_at       TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at       TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ─────────────────────────────────────────────
-- 태그 (공통)
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS tags (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL UNIQUE,
    color      TEXT,
    created_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS project_tags (
    project_id INTEGER NOT NULL REFERENCES projects(id)  ON DELETE CASCADE,
    tag_id     INTEGER NOT NULL REFERENCES tags(id)      ON DELETE CASCADE,
    PRIMARY KEY (project_id, tag_id)
);

CREATE TABLE IF NOT EXISTS schedule_tags (
    schedule_id INTEGER NOT NULL REFERENCES schedules(id) ON DELETE CASCADE,
    tag_id      INTEGER NOT NULL REFERENCES tags(id)      ON DELETE CASCADE,
    PRIMARY KEY (schedule_id, tag_id)
);

-- ─────────────────────────────────────────────
-- 이메일
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS emails (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id  TEXT    UNIQUE,
    subject     TEXT,
    sender      TEXT,
    recipients  TEXT,       -- JSON 배열
    cc          TEXT,       -- JSON 배열
    body_text   TEXT,
    body_html   TEXT,       -- 렌더링 시 XSS sanitize 필수
    sent_at     TEXT,
    imported_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    file_path   TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS email_attachments (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id     INTEGER NOT NULL REFERENCES emails(id) ON DELETE CASCADE,
    filename     TEXT    NOT NULL,
    content_type TEXT,
    size_bytes   INTEGER,
    file_path    TEXT,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS email_project_mappings (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id     INTEGER NOT NULL REFERENCES emails(id)   ON DELETE CASCADE,
    project_id   INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    mapped_by    TEXT    NOT NULL DEFAULT 'user'
                     CHECK (mapped_by IN ('user', 'ai')),
    is_confirmed INTEGER NOT NULL DEFAULT 1
                     CHECK (is_confirmed IN (0, 1)),
    confidence   REAL
                     CHECK (confidence IS NULL
                            OR (confidence >= 0.0 AND confidence <= 1.0)),
    created_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    UNIQUE (email_id, project_id)
);

CREATE TABLE IF NOT EXISTS email_tags (
    email_id   INTEGER NOT NULL REFERENCES emails(id) ON DELETE CASCADE,
    tag_id     INTEGER NOT NULL REFERENCES tags(id)   ON DELETE CASCADE,
    PRIMARY KEY (email_id, tag_id)
);

-- ─────────────────────────────────────────────
-- AI 결과 (polymorphic)
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ai_results (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT    NOT NULL
                    CHECK (source_type IN ('email', 'project', 'task')),
    source_id   INTEGER NOT NULL,
    -- FK 제약 불가 (polymorphic) — 소스 삭제 시 앱 레벨에서 고아 레코드 정리
    result_type TEXT    NOT NULL
                    CHECK (result_type IN (
                        'summary', 'keywords', 'action_items',
                        'project_candidates', 'classification'
                    )),
    model_name  TEXT    NOT NULL,
    prompt      TEXT,
    result      TEXT    NOT NULL,
    is_applied  INTEGER NOT NULL DEFAULT 0
                    CHECK (is_applied IN (0, 1)),
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ─────────────────────────────────────────────
-- 인덱스
-- ─────────────────────────────────────────────

-- projects
CREATE INDEX IF NOT EXISTS idx_projects_parent_id ON projects(parent_id);
CREATE INDEX IF NOT EXISTS idx_projects_status    ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_due_date  ON projects(due_date);

-- tasks
CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status     ON tasks(status);

-- schedules
CREATE INDEX IF NOT EXISTS idx_schedules_scheduled_at ON schedules(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_schedules_project_id   ON schedules(project_id);

-- emails
CREATE INDEX IF NOT EXISTS idx_emails_sent_at ON emails(sent_at);
CREATE INDEX IF NOT EXISTS idx_emails_sender  ON emails(sender);
CREATE INDEX IF NOT EXISTS idx_emails_subject ON emails(subject);

-- email_project_mappings
CREATE INDEX IF NOT EXISTS idx_epm_email_id   ON email_project_mappings(email_id);
CREATE INDEX IF NOT EXISTS idx_epm_project_id ON email_project_mappings(project_id);
CREATE INDEX IF NOT EXISTS idx_epm_confirmed  ON email_project_mappings(is_confirmed);

-- ai_results
CREATE INDEX IF NOT EXISTS idx_ai_results_source  ON ai_results(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_ai_results_applied ON ai_results(is_applied);
