# 데이터베이스 설계

## 개요

- DBMS: SQLite (내장, 단일 파일)
- 저장 위치: `%APPDATA%\com.claudeproj.app\data.db`
- ORM: 미사용 — rusqlite 직접 쿼리 (명시적 SQL 관리)
- 모든 스키마 변경은 Migration을 통해서만 수행

---

## 설계 변경 이력

| 버전 | 변경 내용 |
|------|---------|
| v1.0 | 초기 설계 (projects, tasks, schedules, emails, ai_results, settings) |
| v1.1 | projects.parent_id 추가 (세부 프로젝트 계층). emails.project_id 제거 → email_project_mappings 분리. tags 시스템 추가. |

---

## ERD (Entity Relationship)

```
projects ──(parent_id 자기참조)──► projects (세부 프로젝트, depth ≤ 2)
    │
    ├──────────────────── tasks
    │                       (project_id FK)
    │
    └──────────────────── schedules
                            (project_id FK, nullable)


emails ──────────────────── email_attachments
    │                          (email_id FK)
    │
    └── email_project_mappings ──► projects
           (email_id FK)            (project_id FK)
           mapped_by: 'user'|'ai'
           is_confirmed: 0|1


tags ──── project_tags  ──► projects
     ├─── email_tags    ──► emails
     └─── schedule_tags ──► schedules


ai_results (polymorphic — FK 제약 없음, 앱 레벨에서 무결성 관리)
    source_type: 'email' | 'project' | 'task'
    source_id:   emails.id | projects.id | tasks.id

settings          (독립 KV 스토어)
schema_migrations (마이그레이션 이력)
```

---

## 테이블 스키마

### projects

```sql
CREATE TABLE projects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id   INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    -- NULL: 최상위 프로젝트 / NOT NULL: 세부 프로젝트
    -- 앱 레벨에서 depth ≤ 2 강제 (세부 프로젝트의 자식 생성 금지)
    title       TEXT    NOT NULL,
    description TEXT,
    status      TEXT    NOT NULL DEFAULT 'active',
    -- 'active' | 'paused' | 'completed' | 'archived'
    priority    TEXT    NOT NULL DEFAULT 'medium',
    -- 'low' | 'medium' | 'high'
    start_date  TEXT,               -- ISO 8601 (YYYY-MM-DD)
    due_date    TEXT,
    completed_at TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

> **계층 정책**: `parent_id IS NULL` = 최상위 프로젝트, `parent_id IS NOT NULL` = 세부 프로젝트.
> 세부 프로젝트에 하위 프로젝트 생성 시도 시 앱 레벨에서 차단.

### tasks

```sql
CREATE TABLE tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id  INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    -- 최상위 또는 세부 프로젝트 모두 참조 가능
    title       TEXT    NOT NULL,
    description TEXT,
    status      TEXT    NOT NULL DEFAULT 'todo',
    -- 'todo' | 'in_progress' | 'done'
    priority    TEXT    NOT NULL DEFAULT 'medium',
    -- 'low' | 'medium' | 'high'
    due_date    TEXT,
    completed_at TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

### schedules

```sql
CREATE TABLE schedules (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id       INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    -- 최상위 또는 세부 프로젝트(parent_id 있는) 모두 연결 가능
    -- 세부 프로젝트 연결로 간트차트 2계층 표현 충분 → task_id 미추가 (설계 결정 참조)
    title            TEXT    NOT NULL,
    description      TEXT,
    scheduled_at     TEXT    NOT NULL,  -- ISO 8601 datetime
    duration_minutes INTEGER,
    is_recurring     INTEGER NOT NULL DEFAULT 0,  -- 0 | 1
    recurrence_rule  TEXT,
    -- 'daily' | 'weekly' | 'monthly' | null
    created_at       TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at       TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

### emails

```sql
CREATE TABLE emails (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    -- project_id 제거: 이메일-프로젝트 관계는 email_project_mappings로 관리
    message_id  TEXT    UNIQUE,         -- 이메일 Message-ID 헤더
    subject     TEXT,
    sender      TEXT,                   -- "이름 <email@addr>"
    recipients  TEXT,                   -- JSON 배열: ["a@b.com", ...]
    cc          TEXT,                   -- JSON 배열
    body_text   TEXT,                   -- plain text 본문
    body_html   TEXT,                   -- HTML 본문 (렌더링 시 XSS 주의 — sanitize 필수)
    sent_at     TEXT,                   -- 발신 일시
    imported_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    file_path   TEXT,                   -- 원본 .eml 파일 경로 (참조용)
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

### email_project_mappings

```sql
CREATE TABLE email_project_mappings (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id     INTEGER NOT NULL REFERENCES emails(id)   ON DELETE CASCADE,
    project_id   INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    mapped_by    TEXT    NOT NULL DEFAULT 'user',
    -- 'user': 사용자 직접 연결 / 'ai': AI 추천
    is_confirmed INTEGER NOT NULL DEFAULT 1,
    -- 'user' 직접 연결: 1 (즉시 확정)
    -- 'ai' 추천: 0 (사용자 확인 대기) → 확인 후 1
    confidence   REAL,
    -- AI 추천 시 신뢰도 (0.0 ~ 1.0), 수동 연결 시 NULL
    created_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    UNIQUE(email_id, project_id)
);
```

> **AI 프로젝트 매핑 흐름**:
> AI 분석 결과로 여러 프로젝트 후보가 `is_confirmed=0`으로 저장됨.
> 사용자가 후보를 확인하고 선택하면 `is_confirmed=1` 업데이트.
> 거부한 후보는 레코드 삭제 또는 별도 `rejected=1` 플래그 처리.

### email_attachments

```sql
CREATE TABLE email_attachments (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id     INTEGER NOT NULL REFERENCES emails(id) ON DELETE CASCADE,
    filename     TEXT    NOT NULL,
    content_type TEXT,
    size_bytes   INTEGER,
    file_path    TEXT,   -- 추출 저장 경로
    created_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

### tags

```sql
CREATE TABLE tags (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL UNIQUE,
    color      TEXT,               -- HEX 코드 (예: '#FF5733')
    created_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

### project_tags

```sql
CREATE TABLE project_tags (
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    tag_id     INTEGER NOT NULL REFERENCES tags(id)     ON DELETE CASCADE,
    PRIMARY KEY (project_id, tag_id)
);
```

### email_tags

```sql
CREATE TABLE email_tags (
    email_id   INTEGER NOT NULL REFERENCES emails(id) ON DELETE CASCADE,
    tag_id     INTEGER NOT NULL REFERENCES tags(id)   ON DELETE CASCADE,
    PRIMARY KEY (email_id, tag_id)
);
```

### schedule_tags

```sql
CREATE TABLE schedule_tags (
    schedule_id INTEGER NOT NULL REFERENCES schedules(id) ON DELETE CASCADE,
    tag_id      INTEGER NOT NULL REFERENCES tags(id)      ON DELETE CASCADE,
    PRIMARY KEY (schedule_id, tag_id)
);
```

### ai_results

```sql
CREATE TABLE ai_results (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT    NOT NULL,
    -- 'email' | 'project' | 'task'
    source_id   INTEGER NOT NULL,
    -- polymorphic: emails.id | projects.id | tasks.id
    -- DB 레벨 FK 제약 불가 → 앱 레벨에서 소스 삭제 시 관련 ai_results 함께 삭제
    result_type TEXT    NOT NULL,
    -- 'summary' | 'keywords' | 'action_items' | 'project_candidates' | 'classification'
    model_name  TEXT    NOT NULL,   -- 사용된 Ollama 모델명
    prompt      TEXT,               -- 사용된 프롬프트 (감사 목적)
    result      TEXT    NOT NULL,   -- JSON 또는 plain text
    is_applied  INTEGER NOT NULL DEFAULT 0,  -- 0: 미확인, 1: 사용자 확인 완료
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

> **프로젝트 후보 AI 결과**: `result_type='project_candidates'`로 저장.
> result는 `[{"project_id": 1, "confidence": 0.87}, ...]` 형식 JSON.
> 사용자 확인 후 `email_project_mappings`에 이관, `is_applied=1` 처리.

### settings

```sql
CREATE TABLE settings (
    key        TEXT PRIMARY KEY,
    value      TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 초기 기본값
INSERT INTO settings (key, value) VALUES
    ('ollama_base_url',    'http://localhost:11434'),
    ('ollama_model',       'llama3'),
    ('app_language',       'ko'),
    ('email_storage_path', '');
```

### schema_migrations

```sql
CREATE TABLE schema_migrations (
    version     INTEGER PRIMARY KEY,
    description TEXT    NOT NULL,
    applied_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

---

## 설계 결정 기록

### schedules.task_id 미추가 결정

검토 후 추가하지 않기로 결정. 근거:

| | 내용 |
|-|------|
| **미추가 근거** | `projects.parent_id` 도입으로 `schedules.project_id`가 세부 프로젝트(자식 project)를 직접 참조 가능 → task 수준 없이도 간트차트 2계층 구현 가능 |
| | `tasks`는 체크리스트 성격의 최하위 항목 → 독립 일정을 갖기보다 프로젝트 일정 내에 포함되는 단위 |
| | `project_id + task_id` 동시 보유 시 두 FK 간 일관성 강제 복잡도 발생 |
| **향후 방침** | 간트차트 구현 시 task 수준 연결이 실제로 필요하다고 판단되면 별도 Migration으로 추가 |

### ai_results polymorphic 패턴

`(source_type, source_id)` 조합으로 다형성 참조 구현. DB 레벨 FK 제약 불가.
단일 사용자 앱에서 허용 범위이나, 소스 레코드 삭제 시 앱 레벨에서 고아 레코드 cleanup 필수.

---

## Migration 전략

### 파일 명명 규칙

```
src-tauri/src/db/migrations/
├── V001_initial_schema.sql
├── V001_initial_schema.rollback.sql
├── V002_xxx.sql
├── V002_xxx.rollback.sql
└── ...
```

### 적용 방식

앱 시작 시 자동으로 `schema_migrations` 테이블을 확인하여
미적용 Migration을 버전 순서대로 실행한다.

```
앱 시작
  │
  ▼
schema_migrations 테이블 존재 여부 확인 (없으면 생성)
  │
  ▼
migrations/ 폴더에서 V*.sql 파일 목록 로드
  │
  ▼
applied_versions = SELECT version FROM schema_migrations
  │
  ▼
미적용 버전을 오름차순으로 트랜잭션 단위 실행
  │
  ▼
각 실행 후 schema_migrations에 기록
```

### Migration 작성 원칙

1. 각 Migration은 트랜잭션 단위로 실행
2. 실패 시 전체 롤백
3. `ALTER TABLE`은 SQLite 제약으로 컬럼 추가만 지원 — 구조 변경 시 테이블 재생성 패턴 사용
4. Rollback 스크립트는 항상 쌍으로 작성
5. 데이터 변경(INSERT/UPDATE)을 포함하는 Migration은 별도 버전으로 분리

### SQLite 제약 사항

- `ALTER TABLE`: 컬럼 추가(`ADD COLUMN`)만 지원
- 컬럼 삭제/변경 필요 시: 새 테이블 생성 → 데이터 복사 → 기존 삭제 → 이름 변경
- `FOREIGN KEY`는 pragma로 활성화 필요: `PRAGMA foreign_keys = ON;`
- 재귀 쿼리: `WITH RECURSIVE` 지원 (프로젝트 계층 조회에 활용)

---

## 인덱스 계획

```sql
-- 프로젝트 목록 / 계층 조회
CREATE INDEX idx_projects_parent_id ON projects(parent_id);
CREATE INDEX idx_projects_status    ON projects(status);
CREATE INDEX idx_projects_due_date  ON projects(due_date);

-- Task 조회
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_status     ON tasks(status);

-- 일정 조회
CREATE INDEX idx_schedules_scheduled_at ON schedules(scheduled_at);
CREATE INDEX idx_schedules_project_id   ON schedules(project_id);

-- 이메일 검색 (B-Tree 인덱스, MVP 단계)
CREATE INDEX idx_emails_sent_at ON emails(sent_at);
CREATE INDEX idx_emails_sender  ON emails(sender);
CREATE INDEX idx_emails_subject ON emails(subject);  -- v1.1 추가

-- 이메일-프로젝트 매핑 조회
CREATE INDEX idx_epm_email_id     ON email_project_mappings(email_id);
CREATE INDEX idx_epm_project_id   ON email_project_mappings(project_id);
CREATE INDEX idx_epm_confirmed    ON email_project_mappings(is_confirmed);

-- AI 결과 조회
CREATE INDEX idx_ai_results_source  ON ai_results(source_type, source_id);
CREATE INDEX idx_ai_results_applied ON ai_results(is_applied);
```

### 향후 계획 — 이메일 FTS5 전문 검색

이메일 수천 건 이상 누적 시 LIKE 검색 성능 한계. Phase 5 완료 후 도입 검토.

```sql
-- Phase 5 Migration 예약 (구현 전 별도 검토 필요)
-- CREATE VIRTUAL TABLE emails_fts USING fts5(
--     subject, sender, body_text,
--     content=emails,
--     content_rowid=id
-- );
-- CREATE TRIGGER emails_fts_insert AFTER INSERT ON emails BEGIN
--     INSERT INTO emails_fts(rowid, subject, sender, body_text)
--     VALUES (new.id, new.subject, new.sender, new.body_text);
-- END;
```
