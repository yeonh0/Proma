# Proma

**프로젝트 관리 + 이메일 분석 데스크탑 앱**

로컬 AI(Ollama) 또는 내부망 AI 서비스와 연동하여 이메일을 분석하고, 프로젝트·일정·Task를 통합 관리하는 Windows 데스크탑 애플리케이션입니다. 모든 데이터는 로컬 SQLite에 저장됩니다.

---

## 주요 기능

### ✅ Phase 1 — 프로젝트 관리
- 프로젝트 CRUD (상태: active / paused / completed / archived, 우선순위: low / medium / high)
- Task CRUD — 상태 클릭으로 순환 전환 (todo → in_progress → done)
- 프로젝트 상세 화면 (개요 탭 / Task 탭)

### ✅ Phase 2 — 일정 관리
- 일정 CRUD (소요시간, 반복 여부, RRULE 지원)
- 프로젝트 연결 드롭다운
- 월별 캘린더 뷰 + 목록 뷰 탭 전환

### ✅ Phase 3 — 이메일 임포트 및 관리
- `.eml` 파일 다중 선택 임포트 (Tauri dialog)
- 헤더·본문(plain/HTML)·첨부파일 파싱 (`mailparse`)
- 첨부파일 로컬 저장 (`%APPDATA%\...\attachments\`)
- 중복 임포트 방지 (Message-ID 기준)
- 이메일 ↔ 프로젝트 수동 연결/해제

### ✅ Phase 4 — AI 분석
- 이메일 요약 / 분류 / 답장 초안 생성
- AI 제공자 선택: **Ollama(로컬)** 또는 **내부망 AI 서비스(SSE 스트리밍)**
- 설정 화면 — AI 제공자 / URL / 요청 헤더 / Workspace ID 설정
- AI 결과 DB 저장 및 이메일 상세 화면에서 조회

### ✅ Phase 5 — 대시보드
- 프로젝트·Task·일정·메일 통계 카드
- 미완료 Task 섹션 (진행 중 우선 정렬, 최대 7개)
- 이번 주 일정 / 활성 프로젝트 / 최근 메일

### 🔲 Phase 6 — 안정화
- 토스트 알림 / 로딩 처리 / 입력 유효성 검사 / DB 백업

---

## 기술 스택

| 계층 | 기술 |
|------|------|
| Frontend | React 19 + TypeScript + Vite |
| 라우팅 | React Router v7 (MemoryRouter) |
| Backend | Rust + Tauri v2 |
| 데이터베이스 | SQLite (`rusqlite` 0.32, bundled) |
| 이메일 파싱 | `mailparse` 0.15 |
| 파일 다이얼로그 | `tauri-plugin-dialog` v2 |
| HTTP 클라이언트 | `ureq` 2 (동기 / Tokio 독립) |
| AI — Ollama | HTTP POST `/api/chat` (로컬, qwen3·llama3 등) |
| AI — 내부망 | HTTP POST + SSE 스트리밍 (`llm_result.answer` 누적) |
| 폰트 | NanumSquare (jsDelivr CDN) |
| 빌드/배포 | GitHub Actions (Windows NSIS/MSI 자동 빌드) |

---

## 아키텍처

```
┌─────────────────────────────────────────────┐
│         React + TypeScript (SPA)            │
│   features / pages / shared                 │
└──────────────────┬──────────────────────────┘
                   │ Tauri IPC (invoke, camelCase)
┌──────────────────▼──────────────────────────┐
│         Rust (Tauri v2)                     │
│  commands → repository → services           │
└──────┬───────────────────┬──────────────────┘
       │                   │
┌──────▼──────┐   ┌────────▼───────────────────────┐
│   SQLite    │   │   AI Provider (ureq)            │
│  data.db    │   │   Ollama (localhost:11434)      │
└─────────────┘   │   내부망 AI (SSE 스트리밍)       │
                  └────────────────────────────────┘
```

### 데이터 저장 위치

```
%APPDATA%\com.claudeproj.app\
├── data.db              # SQLite 메인 DB
└── attachments\
    └── {email_id}\      # 첨부파일 저장
```

---

## 프로젝트 구조

```
proma/
├── .github/workflows/
│   └── build-windows.yml   # GitHub Actions 수동 빌드 (NSIS/MSI 생성)
├── src/                        # React 프론트엔드
│   ├── features/               # 도메인별 기능 모듈
│   │   ├── project/
│   │   ├── task/
│   │   ├── schedule/
│   │   ├── email/
│   │   ├── ai/                 # AI 분석 API + 타입
│   │   └── settings/           # 설정 API + 타입
│   ├── pages/                  # 라우트별 페이지 컴포넌트
│   ├── layouts/                # AppLayout (사이드바 + Outlet)
│   └── shared/
│       ├── lib/
│       │   ├── tauri.ts        # invokeCommand<T>() 래퍼
│       │   └── dialog.ts       # openEmlFileDialog()
│       └── types/index.ts      # Status, Priority, TaskStatus
│
├── src-tauri/                  # Rust 백엔드
│   ├── src/
│   │   ├── commands/           # IPC 커맨드 핸들러
│   │   ├── models/             # Serde 직렬화 구조체
│   │   ├── repository/         # SQL 쿼리 레이어
│   │   ├── services/
│   │   │   ├── ai/             # AiProvider 트레이트 + Ollama/Internal 구현
│   │   │   └── eml_parser/
│   │   ├── db/                 # DatabaseManager + MigrationRunner
│   │   └── lib.rs              # AppState, invoke_handler 등록
│   ├── migrations/
│   │   ├── V001_initial_schema.sql
│   │   ├── V002_add_ai_settings.sql
│   │   └── V003_add_draft_reply.sql
│   └── Cargo.toml
│
└── test-data/                  # 통합 테스트 데이터
    ├── eml/                    # 샘플 EML 108개
    ├── projects.json
    ├── schedules.json
    └── expected-ai-results.json
```

---

## DB 스키마 (주요 테이블)

| 테이블 | 설명 |
|--------|------|
| `projects` | 프로젝트 (self-referencing `parent_id`, depth ≤ 2) |
| `tasks` | Task — `project_id` FK, ON DELETE CASCADE |
| `schedules` | 일정 — `project_id` FK (nullable), ON DELETE SET NULL |
| `emails` | 임포트된 이메일 |
| `email_attachments` | 첨부파일 메타데이터 |
| `email_project_mappings` | 이메일 ↔ 프로젝트 다대다 (mapped_by: user / ai) |
| `ai_results` | AI 분석 결과 (source_type + source_id, result_type: summary/classification/draft_reply) |
| `settings` | KV 설정 스토어 (ai_provider, ollama_*, internal_*) |
| `schema_migrations` | 마이그레이션 이력 |

Migration SQL은 컴파일 타임에 바이너리에 임베딩되며, 앱 시작 시 자동 적용됩니다.

---

## 시작하기

### 필수 환경

- [Rust](https://rustup.rs/) (stable)
- [Node.js](https://nodejs.org/) 18+
- [Tauri v2 사전 요구사항](https://v2.tauri.app/ko/start/prerequisites/) (Windows: WebView2, Build Tools)

### 설치 및 실행

```bash
git clone https://github.com/yeonh0/Proma.git
cd Proma
npm install
npm run tauri dev
```

### 빌드

```bash
npm run tauri build
# 결과: src-tauri/target/release/bundle/nsis/*.exe
```

#### GitHub Actions로 자동 빌드 (폐쇄망 배포용)

1. GitHub → **Actions** 탭 → **Windows 빌드** → **Run workflow**
2. 빌드 완료 후 Artifacts에서 `proma-windows` 다운로드
3. 압축 해제 후 설치파일 실행

---

## AI 설정

앱 설정 화면에서 AI 제공자를 선택합니다.

### Ollama (로컬)
```bash
ollama pull qwen3:8b   # 또는 원하는 모델
ollama serve           # 기본 포트: 11434
```
설정: `http://localhost:11434` / 모델명 입력

### 내부망 AI 서비스
- API URL: 내부망 엔드포인트
- Workspace ID: 페이로드에 포함될 workspace_id
- 요청 헤더: 브라우저 DevTools에서 복사한 헤더 붙여넣기 (`Key: Value` 형식)

---

## 개발 규칙

- **Migration**: `src-tauri/migrations/V{NNN}_*.sql` 추가 후 `db/migration.rs`의 `MIGRATIONS` 배열에 수동 등록
- **IPC 커맨드**: `commands/` → `lib.rs`의 `invoke_handler![]`에 등록
- **IPC 파라미터**: Rust `snake_case` → TypeScript `camelCase` 자동 변환 (Tauri v2)
- **Frontend**: `features/{domain}/` 단위로 `types.ts` / `api.ts` / `index.ts` 구성

---

## 로드맵

| Phase | 내용 | 상태 |
|-------|------|------|
| 0 | 설계 및 기반 준비 | ✅ 완료 |
| 1 | 프로젝트 · Task 관리 | ✅ 완료 |
| 2 | 일정 관리 + 캘린더 뷰 | ✅ 완료 |
| 3 | 이메일 임포트 및 관리 | ✅ 완료 |
| 4 | AI 분석 (Ollama + 내부망 AI) | ✅ 완료 |
| 5 | 대시보드 및 통합 | ✅ 완료 |
| 6 | 안정화 및 마무리 | 🔲 예정 |

---

## 라이선스

MIT
