-- V003: ai_results result_type에 'draft_reply' 추가
-- SQLite는 CHECK 제약 변경을 위해 테이블 재생성 방식 사용

CREATE TABLE ai_results_new (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT    NOT NULL
                    CHECK (source_type IN ('email', 'project', 'task')),
    source_id   INTEGER NOT NULL,
    result_type TEXT    NOT NULL
                    CHECK (result_type IN (
                        'summary', 'keywords', 'action_items',
                        'project_candidates', 'classification',
                        'draft_reply'
                    )),
    model_name  TEXT    NOT NULL,
    prompt      TEXT,
    result      TEXT    NOT NULL,
    is_applied  INTEGER NOT NULL DEFAULT 0
                    CHECK (is_applied IN (0, 1)),
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

INSERT INTO ai_results_new SELECT * FROM ai_results;
DROP TABLE ai_results;
ALTER TABLE ai_results_new RENAME TO ai_results;

CREATE INDEX IF NOT EXISTS idx_ai_results_source  ON ai_results(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_ai_results_applied ON ai_results(is_applied);
