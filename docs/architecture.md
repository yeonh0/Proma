# 시스템 아키텍처

## 개요

폐쇄망 Windows 환경에서 동작하는 단일 사용자용 데스크탑 애플리케이션.
외부 네트워크 통신 없이 모든 데이터와 AI 처리를 로컬에서 완결한다.

---

## 레이어 구조

```
┌─────────────────────────────────────────────┐
│           Presentation Layer                │
│         React + TypeScript (SPA)            │
│   컴포넌트 / 페이지 / 상태관리 (Zustand)    │
└──────────────────┬──────────────────────────┘
                   │ Tauri IPC (invoke / event)
┌──────────────────▼──────────────────────────┐
│           Application Layer                 │
│              Rust (Tauri)                   │
│    Command Handlers / Business Logic        │
└──────┬───────────────────────┬──────────────┘
       │                       │
┌──────▼──────┐     ┌──────────▼──────────────┐
│  Data Layer │     │       AI Layer          │
│   SQLite    │     │  Ollama HTTP (localhost)│
│  (rusqlite) │     │     port 11434          │
└─────────────┘     └─────────────────────────┘
```

---

## 기술 스택 상세

| 계층 | 기술 | 역할 |
|------|------|------|
| Frontend | React 18 + TypeScript | UI 렌더링 |
| 상태관리 | Zustand | 클라이언트 상태 |
| 라우팅 | React Router v6 | 화면 전환 |
| Backend | Rust + Tauri v2 | IPC 명령 처리, 비즈니스 로직 |
| DB | SQLite (rusqlite) | 영속 데이터 저장 |
| AI | Ollama (로컬) | LLM 추론 (폐쇄망) |
| 이메일 파싱 | mail-parser (Rust crate) | .eml 파싱 |

---

## 디렉토리 구조

```
claudeProj/
├── src/                            # React 프론트엔드
│   ├── features/                   # 도메인별 기능 모듈
│   │   ├── project/
│   │   │   ├── components/         # 프로젝트 UI 컴포넌트
│   │   │   └── index.ts
│   │   ├── email/
│   │   │   ├── components/
│   │   │   └── index.ts
│   │   ├── schedule/
│   │   │   ├── components/
│   │   │   └── index.ts
│   │   └── ai/
│   │       ├── components/
│   │       └── index.ts
│   ├── shared/                     # 공유 리소스
│   │   ├── components/             # 공통 UI 컴포넌트
│   │   ├── hooks/                  # 공통 커스텀 훅
│   │   ├── lib/
│   │   │   └── tauri.ts            # IPC invoke 래퍼
│   │   └── types/
│   │       └── index.ts            # 공통 타입 (Status, Priority 등)
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
│
├── src-tauri/                      # Rust 백엔드
│   ├── migrations/                 # SQL 마이그레이션 파일 (include_str! 임베딩)
│   │   ├── V001_initial_schema.sql
│   │   └── V001_initial_schema.rollback.sql
│   ├── src/
│   │   ├── main.rs                 # 진입점
│   │   ├── lib.rs                  # 모듈 선언, Tauri 빌더, AppState
│   │   ├── db/                     # DB 초기화 및 Migration 엔진
│   │   │   ├── mod.rs              # DatabaseManager, DbError
│   │   │   └── migration.rs        # Migration struct, MIGRATIONS 배열, MigrationRunner
│   │   ├── commands/               # Tauri IPC 커맨드
│   │   │   ├── mod.rs
│   │   │   ├── project.rs
│   │   │   ├── task.rs
│   │   │   ├── schedule.rs
│   │   │   ├── email.rs
│   │   │   └── ai.rs
│   │   ├── models/                 # 도메인 모델 (struct + serde)
│   │   │   ├── mod.rs
│   │   │   ├── project.rs
│   │   │   ├── email.rs
│   │   │   └── ai_result.rs
│   │   ├── repository/             # DB 접근 계층 (rusqlite)
│   │   │   ├── mod.rs
│   │   │   ├── project.rs
│   │   │   ├── email.rs
│   │   │   └── ai_result.rs
│   │   └── services/               # 비즈니스 로직
│   │       ├── mod.rs
│   │       ├── email_parser.rs     # .eml 파싱
│   │       └── ollama_client.rs    # Ollama HTTP 클라이언트
│   ├── Cargo.toml
│   └── tauri.conf.json
│
├── docs/
│   ├── architecture.md             # 이 문서
│   ├── database.md
│   ├── ui-flow.md
│   ├── roadmap.md
│   └── tasks/
│       └── completed/
│
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## IPC 설계 원칙

- 모든 프론트엔드 → 백엔드 통신은 Tauri `invoke()` 사용
- 커맨드명 규칙: `{domain}_{action}` (예: `project_create`, `email_import`)
- 에러는 Rust `Result<T, String>` → 프론트엔드 `Promise<T>` 로 전달
- 대용량 데이터(이메일 본문 등)는 페이지네이션 적용

---

## 데이터 흐름 — 이메일 AI 분석

### 흐름 1: 내용 분석 (요약 / 키워드 / 액션 아이템)

```
사용자: .eml 파일 선택
    │
    ▼
Frontend: invoke('email_import', { path })
    │
    ▼
Rust: email_parser::parse_eml(path)
    │
    ▼
Rust: email_repo::save(parsed_email) → SQLite
    │
    ▼
사용자: "요약 요청" 버튼 클릭
    │
    ▼
Frontend: invoke('ai_analyze_email', { email_id, result_type: 'summary' })
    │
    ▼
Rust: ollama_client::request(prompt) → Ollama localhost:11434
    │
    ▼
Rust: ai_result_repo::save(result, is_applied=false) → SQLite
    │
    ▼
Frontend: 결과 표시 + [적용] [무시] 버튼
    │
    ├─ [적용] → invoke('ai_result_apply', { result_id })
    │               → ai_result_repo::mark_applied(result_id)
    └─ [무시] → 결과 숨김 (DB에 is_applied=0 보존)
```

### 흐름 2: AI 프로젝트 후보 제안 → 사용자 확정 → email_project_mappings 저장

```
사용자: "프로젝트 연결 추천" 버튼 클릭
    │
    ▼
Frontend: invoke('ai_suggest_projects', { email_id })
    │
    ▼
Rust: ollama_client::request(project_candidate_prompt) → Ollama localhost:11434
    │
    ▼
Rust: ai_result_repo::save(result_type='project_candidates', is_applied=false)
Rust: email_project_mappings에 후보 행 삽입 (mapped_by='ai', is_confirmed=0)
    │
    ▼
Frontend: 후보 프로젝트 목록 표시 (신뢰도 포함)
    │
    ├─ [확정] 클릭
    │       ▼
    │   Frontend: invoke('email_project_confirm', { email_id, project_id })
    │       ▼
    │   Rust: email_project_mappings → is_confirmed=1 업데이트
    │         ai_results             → is_applied=1 업데이트
    │
    └─ [제거] 클릭
            ▼
        Rust: email_project_mappings 해당 행 삭제
```

모든 AI 결과는 `is_applied = false`, 프로젝트 매핑 후보는 `is_confirmed = 0`으로 먼저 저장하고,
사용자가 명시적으로 확인한 후에만 반영한다. 자동 적용 금지.

---

## DB 초기화 흐름

앱 시작 시 `tauri::Builder::setup()` 콜백에서 DB 초기화가 이루어진다.

```
앱 시작
  │
  ▼
app.path().app_data_dir()
  → %APPDATA%\com.claudeproj.app\  (개발/배포 공통)
  │
  ▼
DatabaseManager::new("data.db")
  ├─ create_dir_all(parent) — 디렉토리 없으면 자동 생성
  ├─ Connection::open(path)  — data.db 파일 없으면 자동 생성
  └─ PRAGMA foreign_keys=ON / journal_mode=WAL / synchronous=NORMAL
  │
  ▼
MigrationRunner::run(&mut conn)
  ├─ schema_migrations 테이블 생성 (CREATE TABLE IF NOT EXISTS)
  ├─ SELECT COALESCE(MAX(version), 0) FROM schema_migrations
  └─ 미적용 Migration을 버전 오름차순으로 각각 독립 트랜잭션 실행
       실패 시 tx drop → 자동 rollback → schema_migrations 기록 없음
  │
  ▼
app.manage(AppState { db: Mutex<DatabaseManager> })
```

Migration SQL은 `include_str!()` 매크로로 컴파일 타임에 바이너리에 임베딩된다.
런타임 파일 탐색 없음 — 배포 환경에서 파일 경로 의존성 없음.

---

## 보안 및 데이터 정책

- 데이터는 OS 앱 데이터 디렉토리에 저장 (`%APPDATA%\com.claudeproj.app\`)
- 외부 네트워크 통신 없음 (Ollama는 localhost only)
- 파일 접근 권한은 Tauri allowlist로 최소 범위 제한
