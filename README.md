# proma

**프로젝트 관리 + 이메일 분석 데스크탑 앱**

로컬 AI(Ollama)와 연동하여 이메일을 분석하고, 프로젝트·일정·Task를 통합 관리하는 Windows 데스크탑 애플리케이션입니다. 외부 서버 없이 모든 데이터와 AI 추론을 로컬에서 완결합니다.

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

### 🔲 Phase 4 — AI 분석 (Ollama 연동)
- 이메일 요약 / 키워드 / 액션 아이템 추출
- AI 프로젝트 후보 제안 (사용자 확인 후에만 적용)
- 설정 화면 — Ollama URL / 모델 설정

### 🔲 Phase 5 — 대시보드
- 프로젝트 현황 / 오늘 일정 / 마감 임박 Task / 미확인 AI 결과 위젯

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
| AI | Ollama (localhost:11434) — Phase 4 예정 |

---

## 아키텍처

```
┌─────────────────────────────────────────────┐
│         React + TypeScript (SPA)            │
│   features / pages / shared                 │
└──────────────────┬──────────────────────────┘
                   │ Tauri IPC (invoke)
┌──────────────────▼──────────────────────────┐
│         Rust (Tauri v2)                     │
│  commands → repository → services           │
└──────┬───────────────────────┬──────────────┘
       │                       │
┌──────▼──────┐     ┌──────────▼──────────────┐
│   SQLite    │     │   Ollama (localhost)     │
│  data.db    │     │   port 11434  (Phase 4) │
└─────────────┘     └─────────────────────────┘
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
├── src/                        # React 프론트엔드
│   ├── features/               # 도메인별 기능 모듈
│   │   ├── project/            # 프로젝트 목록·상세·모달
│   │   ├── task/               # Task 목록·상태 전환
│   │   ├── schedule/           # 일정 목록·캘린더·모달
│   │   └── email/              # 이메일 목록
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
│   │   ├── services/           # 비즈니스 로직 (eml_parser, ollama_client)
│   │   ├── db/                 # DatabaseManager + MigrationRunner
│   │   └── lib.rs              # AppState, invoke_handler 등록
│   ├── migrations/
│   │   └── V001_initial_schema.sql   # 전체 스키마 (include_str! 임베딩)
│   └── Cargo.toml
│
└── docs/
    ├── architecture.md
    ├── database.md
    ├── roadmap.md
    └── ui-flow.md
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
| `ai_results` | AI 분석 결과 (polymorphic source_type + source_id) |
| `settings` | KV 설정 스토어 (Ollama URL/모델 등) |
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
# 저장소 클론
git clone https://github.com/<username>/proma.git
cd proma

# 의존성 설치
npm install

# 개발 서버 + Tauri 앱 실행
npm run tauri dev
```

### 빌드

```bash
npm run tauri build
```

빌드 결과물은 `src-tauri/target/release/bundle/` 에 생성됩니다.

---

## AI 기능 사용 (Phase 4 이후)

[Ollama](https://ollama.com/)를 설치하고 원하는 모델을 Pull합니다.

```bash
ollama pull llama3
ollama serve    # 기본 포트: 11434
```

앱 설정 화면에서 Ollama URL과 모델명을 지정하면 이메일 분석 기능이 활성화됩니다.

---

## 개발 규칙

- **Migration**: `src-tauri/migrations/V{NNN}_*.sql` 추가 후 `db/migration.rs`의 `MIGRATIONS` 배열에 수동 등록
- **IPC 커맨드**: `commands/` → `lib.rs`의 `invoke_handler![]`에 등록
- **Frontend**: `features/{domain}/` 단위로 `types.ts` / `api.ts` / `index.ts` 구성

---

## 로드맵

| Phase | 내용 | 상태 |
|-------|------|------|
| 0 | 설계 및 기반 준비 | ✅ 완료 |
| 1 | 프로젝트 · Task 관리 | ✅ 완료 |
| 2 | 일정 관리 + 캘린더 뷰 | ✅ 완료 |
| 3 | 이메일 임포트 및 관리 | ✅ 완료 |
| 4 | AI 분석 (Ollama 연동) | 🔲 예정 |
| 5 | 대시보드 및 통합 | 🔲 예정 |
| 6 | 안정화 및 마무리 | 🔲 예정 |

---

## 라이선스

MIT
