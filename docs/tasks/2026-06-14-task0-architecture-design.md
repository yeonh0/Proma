# Task 0 — 아키텍처 설계 및 문서화

## 목적

코드 구현 시작 전, 전체 시스템 설계를 확정하고 문서화한다.
이후 모든 구현 작업은 이 설계를 기준으로 진행한다.

## 구현 범위

코드 생성 없음. 문서 생성만 수행.

## 작업 목록

| # | 내용 | 출력물 | 상태 |
|---|------|--------|------|
| 0-1 | 시스템 아키텍처 설계 | `docs/architecture.md` | ✅ |
| 0-2 | DB 스키마 설계 | `docs/database.md` | ✅ |
| 0-3 | UI 화면 흐름 설계 | `docs/ui-flow.md` | ✅ |
| 0-4 | Phase별 로드맵 작성 | `docs/roadmap.md` | ✅ |

## 완료 조건

- [x] 4개 문서 모두 생성됨
- [x] 시스템 레이어 구조 확정
- [x] 디렉토리 구조 확정
- [x] SQLite 테이블 스키마 초안 확정
- [x] Migration 전략 확정
- [x] 화면 구조 및 전환 흐름 확정
- [x] Phase별 로드맵 확정

## 설계 결정 사항

### 기술 선택

| 항목 | 선택 | 이유 |
|------|------|------|
| 상태관리 | Zustand | 단일 사용자 앱, Redux는 과함 |
| DB 접근 | rusqlite 직접 쿼리 | ORM보다 Migration 제어가 명확함 |
| 이메일 파싱 | mail-parser crate | Rust 생태계, 폐쇄망 호환 |
| 라우팅 | React Router v6 | Tauri SPA 표준 |

### 핵심 정책 결정

- AI 결과: `is_applied = false` 로 저장 후 사용자 확인 시에만 `true` 전환
- DB 날짜: SQLite TEXT 타입, `datetime('now', 'localtime')` 사용
- IPC 커맨드명: `{domain}_{action}` 형식 통일
- 데이터 저장 위치: `%APPDATA%\com.claudeproj.app\`

## 예상 영향 범위

없음 (설계 단계)

## 다음 Task

Task 0-5: Tauri 프로젝트 초기화
- `npm create tauri-app` 실행
- 기본 설정 구성
- `docs/tasks/2026-06-14-task0-tauri-init.md` 작성
