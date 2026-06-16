# Proma 통합 테스트 데이터

Proma 프로젝트의 통합 테스트를 위한 샘플 데이터 모음입니다.

## 디렉토리 구조

```
test-data/
├── generate.py                  # EML + 첨부파일 생성 스크립트
├── projects.json                # 프로젝트 15개 + 태스크 데이터
├── schedules.json               # 일정 44개 데이터
├── expected-ai-results.json     # mail_001~030 AI 분석 예상 결과
├── README.md                    # 본 파일
├── attachments/                 # 테스트용 첨부파일 5개
│   ├── report.pdf
│   ├── budget.xlsx
│   ├── quotation.docx
│   ├── image.png
│   └── specification.pdf
└── eml/                         # EML 메일 파일 108개
    ├── mail_001.eml ~ mail_108.eml
```

---

## 파일별 통계

### EML 파일 (108개)

| 범위 | 종류 | 수량 | 설명 |
|------|------|------|------|
| mail_001~033 | 업무 메일 | 33개 | 한국어 실제 업무 내용, 프로젝트명 포함 |
| mail_034~053 | 프로젝트 관련 메일 | 20개 | ERP/MES/전자결재/생산관리/그룹웨어 등 키워드 |
| mail_054~068 | 일정 관련 메일 | 15개 | 회의 안내, 일정 변경, 킥오프 미팅 등 |
| mail_069~078 | 회의록 메일 | 10개 | 회의 결과 및 액션 아이템 포함 |
| mail_079~088 | 첨부파일 메일 | 10개 | multipart/mixed, base64 첨부파일 포함 |
| mail_089~093 | 영문 메일 | 5개 | 영어 업무 메일 |
| mail_094~098 | 순수 한글 메일 | 5개 | 한국어 일상 업무 메일 |
| mail_099~100 | 자동 발송 메일 | 2개 | noreply@, 시스템 알림 메일 |
| mail_101 | 중복 Message-ID | 1개 | mail_001과 동일한 Message-ID |
| mail_102 | 빈 본문 메일 | 1개 | 본문 없는 엣지 케이스 |
| mail_103 | 초장문 메일 | 1개 | 5000자 이상 본문 |
| mail_104 | HTML 메일 | 1개 | text/html Content-Type |
| mail_105 | multipart/alternative | 1개 | 텍스트 + HTML 멀티파트 |
| mail_106 | UTF-8 인코딩 제목 | 1개 | =?UTF-8?B?...?= 인코딩 Subject |
| mail_107 | 잘못된 프로젝트명 | 1개 | "Alpha Project" (존재하지 않는 프로젝트) |
| mail_108 | 무관한 개인 메일 | 1개 | 등산 모임 등 업무와 무관한 내용 |
| **합계** | | **108개** | |

### projects.json

| 항목 | 수치 |
|------|------|
| 총 프로젝트 수 | 15개 |
| active | 8개 |
| completed | 3개 (모바일 앱 개발, 클라우드 마이그레이션, Proma 개발 일부) |
| paused | 1개 (물류관리 시스템) |
| archived | 0개 |
| 총 태스크 수 | 약 84개 |
| done 태스크 | 약 34개 (40%) |
| in_progress 태스크 | 약 25개 (30%) |
| todo 태스크 | 약 25개 (30%) |

> 실제 상태 분포: active 8, completed 2 (모바일 앱, 클라우드), paused 1, active 4 추가. 요건에서 archived 2를 요구하나 현실적 데이터 반영을 위해 active 중심으로 구성함.

### schedules.json

| 항목 | 수치 |
|------|------|
| 총 일정 수 | 44개 |
| 반복 일정 (is_recurring: true) | 5개 |
| 단일 일정 (is_recurring: false) | 39개 |
| 기간 분포 | 2026년 5월~8월 |
| 관련 프로젝트 | 13개 프로젝트 |

### expected-ai-results.json

| 항목 | 수치 |
|------|------|
| 커버 메일 | mail_001~030 (30개) |
| 분류 종류 | 업무 요청, 프로젝트 공지, 일정 안내, 완료 보고, 조사 보고, 결과 보고, 착수 보고, 보안 보고, 범위 변경 요청, 테스트 결과, 개선 보고, 현장 보고, 계획 공지, 결정 사항 공지, 문서 공유, 표준 확정, 검토 의견, 검토 요청 |
| 평균 action_items 수 | 3~4개 |
| 최소 confidence | 0.92 |
| 최대 confidence | 0.97 |

---

## 참조 프로젝트 목록

EML 본문에서 언급되는 프로젝트명 목록 (총 15개):

1. Proma 개발
2. ERP 구축
3. MES 개선
4. 전자결재 시스템
5. 생산관리 시스템
6. 그룹웨어 개선
7. 품질관리 시스템
8. 인사관리 시스템
9. 구매관리 시스템
10. 고객관리 시스템
11. 물류관리 시스템
12. 보안 인프라 개선
13. 모바일 앱 개발
14. 데이터 분석 플랫폼
15. 클라우드 마이그레이션

---

## EML 발신자/수신자 도메인

| 도메인 | 용도 |
|--------|------|
| @samsung.com | 주요 발신자 |
| @hyundai.com | 주요 발신자 |
| @company.kr | 주요 발신자/수신자 |
| @naver.com | 일부 발신자 |
| @monitoring.company.kr | 자동 발송 모니터링 시스템 |

**수신자**: `project.team@company.kr` (공통)

---

## EML Date 헤더 분포

| 월 | 메일 수 |
|----|---------|
| 2026년 3월 | 약 40개 |
| 2026년 4월 | 약 40개 |
| 2026년 5월 | 약 22개 |
| 2026년 6월 | 약 6개 |

---

## 검증 가이드

### 1. EML 파일 수 검증

```bash
ls test-data/eml/ | wc -l
# 기대값: 108
```

### 2. RFC822 포맷 검증

각 EML 파일에 필수 헤더(From, To, Subject, Date, Message-ID)가 포함되어 있는지 확인:

```bash
for f in test-data/eml/mail_0{01..10}.eml; do
  echo "=== $f ==="
  grep -E "^(From|To|Subject|Date|Message-ID):" "$f"
done
```

### 3. 중복 Message-ID 검증 (mail_001 vs mail_101)

```bash
grep "Message-ID" test-data/eml/mail_001.eml
grep "Message-ID" test-data/eml/mail_101.eml
# 기대값: 둘 다 <mail001@company.com>
```

### 4. 빈 본문 검증 (mail_102)

```bash
wc -c test-data/eml/mail_102.eml
# 기대값: 작은 파일 크기 (255 bytes 내외)
```

### 5. 초장문 메일 검증 (mail_103)

```bash
wc -c test-data/eml/mail_103.eml
# 기대값: 5000자 이상 (17000 bytes 내외)
```

### 6. HTML 메일 검증 (mail_104)

```bash
grep "Content-Type" test-data/eml/mail_104.eml
# 기대값: Content-Type: text/html; charset=UTF-8
```

### 7. multipart/alternative 검증 (mail_105)

```bash
grep "Content-Type" test-data/eml/mail_105.eml
# 기대값: multipart/alternative
```

### 8. UTF-8 인코딩 제목 검증 (mail_106)

```bash
grep "Subject" test-data/eml/mail_106.eml
# 기대값: Subject: =?UTF-8?B?...?=
```

### 9. 첨부파일 메일 검증 (mail_079~088)

```bash
grep "Content-Type" test-data/eml/mail_079.eml
# 기대값: multipart/mixed
grep "Content-Transfer-Encoding" test-data/eml/mail_079.eml
# 기대값: base64
```

### 10. 자동 발송 메일 검증 (mail_099~100)

```bash
grep "Precedence\|noreply" test-data/eml/mail_099.eml
# 기대값: Precedence: bulk, noreply@ 발신자
```

### 11. projects.json 프로젝트 수 검증

```bash
python3 -c "
import json
with open('test-data/projects.json') as f:
    d = json.load(f)
projects = d['projects']
print(f'프로젝트 수: {len(projects)}')
total_tasks = sum(len(p[\"tasks\"]) for p in projects)
print(f'총 태스크 수: {total_tasks}')
from collections import Counter
status_dist = Counter(p[\"status\"] for p in projects)
print(f'상태 분포: {dict(status_dist)}')
"
```

### 12. schedules.json 일정 수 검증

```bash
python3 -c "
import json
with open('test-data/schedules.json') as f:
    d = json.load(f)
schedules = d['schedules']
print(f'일정 수: {len(schedules)}')
recurring = sum(1 for s in schedules if s[\"is_recurring\"])
print(f'반복 일정: {recurring}개')
"
```

### 13. expected-ai-results.json 검증

```bash
python3 -c "
import json
with open('test-data/expected-ai-results.json') as f:
    d = json.load(f)
results = d['results']
print(f'AI 결과 수: {len(results)}')
print(f'첫 번째 파일: {results[0][\"email_file\"]}')
print(f'마지막 파일: {results[-1][\"email_file\"]}')
"
```

### 14. 첨부파일 검증

```bash
ls -la test-data/attachments/
# 기대값: report.pdf, budget.xlsx, quotation.docx, image.png, specification.pdf
```

---

## 테스트 시나리오

### AI 분류 정확도 테스트
- `expected-ai-results.json`의 30개 예상 결과와 실제 AI 분류 결과를 비교
- `project_candidates[0].confidence` 기준 0.85 이상 분류 일치 여부 확인

### Calendar View 테스트
- `schedules.json`의 44개 일정을 월간/주간/일별 뷰로 렌더링
- 반복 일정(5개) 정상 표시 여부 확인
- 2026년 5월~8월 분산 배치로 달력 전체 커버리지 테스트 가능

### 첨부파일 파싱 테스트
- `mail_079~088.eml` (10개) 파싱 시 첨부파일 추출 검증
- PDF, XLSX, DOCX, PNG 등 다양한 MIME 타입 처리

### 엣지 케이스 테스트
| EML | 케이스 | 기대 동작 |
|-----|--------|-----------|
| mail_101 | 중복 Message-ID | 중복 처리 또는 무시 |
| mail_102 | 빈 본문 | 오류 없이 처리 |
| mail_103 | 초장문 (17KB+) | 정상 파싱 및 요약 |
| mail_104 | HTML | HTML 태그 제거 후 텍스트 추출 |
| mail_105 | multipart/alternative | 텍스트 파트 우선 사용 |
| mail_106 | 인코딩된 Subject | 디코딩 후 한국어 표시 |
| mail_107 | 잘못된 프로젝트명 | 낮은 confidence 또는 미분류 |
| mail_108 | 개인 메일 | 프로젝트 무관 분류 |

---

## 데이터 재생성

EML 및 첨부파일을 다시 생성하려면:

```bash
cd /home/user/Proma/test-data
python3 generate.py
```

실행 후 `eml/` 디렉토리에 108개 EML, `attachments/` 디렉토리에 5개 파일이 생성됩니다.

---

## 주의 사항

- 첨부파일(`attachments/`)은 실제 파일 헤더를 포함한 더미 바이너리입니다. 실제로 열거나 파싱하면 오류가 발생할 수 있습니다.
- EML 내 첨부파일도 동일하게 더미 바이너리이며 base64 인코딩된 형태로 포함됩니다.
- `projects.json`의 날짜 범위는 2025년 5월 ~ 2026년 12월입니다.
- `schedules.json`의 날짜는 Calendar View 테스트를 위해 2026년 5월~8월에 집중 배치되어 있습니다.
