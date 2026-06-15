-- V003 롤백: draft_reply 제거 (해당 행 삭제 후 테이블 재생성)

DELETE FROM ai_results WHERE result_type = 'draft_reply';

CREATE TABLE ai_results_v002 (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT    NOT NULL
                    CHECK (source_type IN ('email', 'project', 'task')),
    source_id   INTEGER NOT NULL,
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

INSERT INTO ai_results_v002 SELECT * FROM ai_results;
DROP TABLE ai_results;
ALTER TABLE ai_results_v002 RENAME TO ai_results;

CREATE INDEX IF NOT EXISTS idx_ai_results_source  ON ai_results(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_ai_results_applied ON ai_results(is_applied);
