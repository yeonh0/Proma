#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proma 통합 테스트 데이터 생성 스크립트
EML 108개 + 첨부파일 5개 생성
"""

import os
import base64
import struct
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EML_DIR = os.path.join(BASE_DIR, "eml")
ATT_DIR = os.path.join(BASE_DIR, "attachments")

os.makedirs(EML_DIR, exist_ok=True)
os.makedirs(ATT_DIR, exist_ok=True)

PROJECTS = [
    "Proma 개발", "ERP 구축", "MES 개선", "전자결재 시스템", "생산관리 시스템",
    "그룹웨어 개선", "품질관리 시스템", "인사관리 시스템", "구매관리 시스템",
    "고객관리 시스템", "물류관리 시스템", "보안 인프라 개선", "모바일 앱 개발",
    "데이터 분석 플랫폼", "클라우드 마이그레이션"
]

SENDERS = [
    ("김민준", "minjun.kim@samsung.com"),
    ("이서연", "seoyeon.lee@hyundai.com"),
    ("박지훈", "jihoon.park@company.kr"),
    ("최유진", "yujin.choi@naver.com"),
    ("정수빈", "subin.jung@samsung.com"),
    ("한승우", "seungwoo.han@hyundai.com"),
    ("오다은", "daeun.oh@company.kr"),
    ("임재원", "jaewon.im@samsung.com"),
    ("신예린", "yerin.shin@company.kr"),
    ("강태양", "taeyang.kang@hyundai.com"),
    ("윤하늘", "haneul.yoon@naver.com"),
    ("장소희", "sohee.jang@samsung.com"),
    ("홍길동", "gildong.hong@company.kr"),
    ("배수진", "sujin.bae@hyundai.com"),
    ("조민서", "minseo.jo@company.kr"),
]

RECIPIENT = ("프로젝트팀", "project.team@company.kr")

def make_date(month, day, hour=9):
    return f"{'Mon' if day%7==0 else 'Tue' if day%7==1 else 'Wed' if day%7==2 else 'Thu' if day%7==3 else 'Fri' if day%7==4 else 'Sat' if day%7==5 else 'Sun'}, {day:02d} {'Mar' if month==3 else 'Apr' if month==4 else 'May' if month==5 else 'Jun'} 2026 {hour:02d}:00:00 +0900"

def write_eml(filename, raw_content):
    path = os.path.join(EML_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(raw_content)

def simple_eml(mid, sender_name, sender_email, subject, body, date, extra_headers=""):
    return f"""From: {sender_name} <{sender_email}>
To: {RECIPIENT[0]} <{RECIPIENT[1]}>
Subject: {subject}
Date: {date}
Message-ID: <{mid}@company.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
{extra_headers}
{body}"""

# ── mail_001 ~ 033: 업무 메일 ─────────────────────────────────────────────
work_mails = [
    (1,  3,  1,  9, "ERP 구축 프로젝트 요구사항 검토 요청",
     "안녕하세요 김민준 차장입니다.\n\nERP 구축 프로젝트의 요구사항 분석 결과를 검토해 주시기 바랍니다.\n첨부된 요구사항 명세서를 확인하시고 의견을 이번 주 금요일까지 회신해 주세요.\n\n주요 검토 항목:\n1. 구매 모듈 연계 방식\n2. 재고 관리 실시간 동기화\n3. 기존 레거시 시스템 마이그레이션 방안\n\n감사합니다.", "ERP 구축", 0),
    (2,  3,  3, 10, "MES 개선 착수 보고 자료 공유",
     "안녕하세요.\n\nMES 개선 프로젝트 착수 보고 자료를 공유드립니다.\n다음 주 월요일 오전 10시에 킥오프 미팅이 예정되어 있습니다.\n자료를 미리 검토하시고 질문 사항 정리해 주시기 바랍니다.\n\n주요 개선 대상:\n- 실시간 생산 현황 모니터링\n- 불량률 자동 집계 기능\n- 설비 가동률 대시보드", "MES 개선", 1),
    (3,  3,  5, 14, "전자결재 시스템 UAT 일정 안내",
     "전자결재 시스템 사용자 인수 테스트(UAT) 일정을 안내드립니다.\n\n일정: 2026년 3월 20일(금) ~ 3월 27일(금)\n장소: 3층 교육실\n참여 부서: 총무팀, 인사팀, 재무팀\n\n각 부서별 테스트 시나리오는 별도 공유 예정입니다.\n문의 사항은 전산팀 박지훈(내선 1234)에게 연락 주세요.", "전자결재 시스템", 2),
    (4,  3,  8,  9, "생산관리 시스템 1차 개발 완료 보고",
     "생산관리 시스템 1차 개발이 완료되었습니다.\n\n완료 기능:\n- 생산 계획 등록/수정/삭제\n- 작업 지시서 자동 발행\n- 생산 실적 입력 화면\n\n미완료 기능 (2차 예정):\n- 원자재 자동 발주 연계\n- KPI 대시보드\n\n시연은 3월 15일 오후 2시로 예정되어 있습니다.", "생산관리 시스템", 3),
    (5,  3, 10, 11, "그룹웨어 개선 사용자 인터뷰 결과 보고",
     "지난주 실시한 그룹웨어 개선 사용자 인터뷰 결과를 보고드립니다.\n\n주요 불만 사항:\n1. 모바일 앱 속도 저하 (응답자 78%)\n2. 전자결재 연동 오류 (응답자 45%)\n3. 캘린더 공유 기능 미흡 (응답자 62%)\n\n개선 우선순위 재조정이 필요합니다.\n다음 주 기획 회의에서 논의하겠습니다.", "그룹웨어 개선", 4),
    (6,  3, 12,  9, "품질관리 시스템 검수 기준 협의 요청",
     "안녕하세요.\n\n품질관리 시스템 개발을 위한 검수 기준 협의가 필요합니다.\n현재 각 공장별로 상이한 기준을 적용하고 있어 통합 기준 수립이 시급합니다.\n\n협의 필요 사항:\n- 불량 판정 기준 통일\n- 샘플링 방식 표준화\n- 이력 보관 기간 설정\n\n3월 20일까지 의견 주시면 감사하겠습니다.", "품질관리 시스템", 5),
    (7,  3, 15, 14, "인사관리 시스템 데이터 마이그레이션 계획",
     "인사관리 시스템 전환에 따른 데이터 마이그레이션 계획을 공유드립니다.\n\n마이그레이션 대상:\n- 임직원 기본 정보 (약 2,400건)\n- 급여 이력 (2020년~현재)\n- 인사 발령 이력\n- 교육 이수 기록\n\n마이그레이션 일정: 4월 1일~7일\n검증 기간: 4월 8일~14일\n\n각 팀의 데이터 정제 협조를 부탁드립니다.", "인사관리 시스템", 6),
    (8,  3, 17, 10, "구매관리 시스템 공급업체 포털 설계 검토",
     "구매관리 시스템의 공급업체 포털 설계안을 검토해 주시기 바랍니다.\n\n주요 기능:\n1. 견적 요청 수신 및 응답\n2. 발주서 확인 및 납기 확정\n3. 납품 실적 조회\n4. 대금 지급 현황 확인\n\n보안 요구사항:\n- SSL/TLS 암호화 필수\n- OTP 인증 적용\n\n설계 검토 회의는 3월 24일 오전 10시입니다.", "구매관리 시스템", 7),
    (9,  3, 19, 11, "고객관리 시스템 CRM 기능 범위 확정",
     "고객관리 시스템(CRM) 1단계 기능 범위를 확정하여 안내드립니다.\n\n포함 기능:\n- 고객 정보 통합 관리\n- 영업 기회 파이프라인\n- 고객 문의/불만 처리\n- 마케팅 캠페인 관리\n\n제외 기능 (2단계):\n- AI 기반 고객 이탈 예측\n- 실시간 채팅 상담\n\n개발 착수: 4월 1일 예정", "고객관리 시스템", 8),
    (10, 3, 22,  9, "물류관리 시스템 WMS 연계 방안 검토",
     "물류관리 시스템과 기존 WMS 연계 방안을 검토해 주시기 바랍니다.\n\n현황:\n- WMS는 2015년 구축된 레거시 시스템\n- REST API 미지원, FTP 방식으로 데이터 교환\n\n검토 방안:\n1. 미들웨어 방식 (EAI 솔루션 도입)\n2. DB 직접 연계\n3. WMS 동시 교체\n\n비용 및 리스크 분석 결과를 4월 5일까지 보고해 주세요.", "물류관리 시스템", 9),
    (11, 3, 24, 14, "보안 인프라 개선 취약점 점검 결과",
     "보안 인프라 개선 프로젝트 관련 외부 취약점 점검 결과를 보고드립니다.\n\n주요 취약점 (긴급):\n1. 내부망 방화벽 정책 미흡 (CVE-2025-1234)\n2. SSL 인증서 만료 임박 (3개 서버)\n3. 관리자 계정 패스워드 정책 미적용\n\n즉시 조치 필요 사항은 이번 주 내로 처리하겠습니다.\n전체 보고서는 첨부 파일을 확인해 주세요.", "보안 인프라 개선", 10),
    (12, 3, 26, 10, "모바일 앱 개발 UI/UX 프로토타입 리뷰",
     "모바일 앱 개발 프로젝트 UI/UX 프로토타입 리뷰 결과를 공유드립니다.\n\n주요 피드백:\n- 메인 화면 정보 밀도 과다 → 재설계 필요\n- 알림 설정 UI 직관성 부족\n- 다크 모드 지원 요청\n\n수정 프로토타입은 4월 10일까지 제출 예정입니다.\n와이어프레임 재작업에 약 3인/주 소요 예상입니다.", "모바일 앱 개발", 11),
    (13, 3, 29,  9, "데이터 분석 플랫폼 데이터 거버넌스 정책 수립",
     "데이터 분석 플랫폼 구축에 앞서 데이터 거버넌스 정책 수립이 필요합니다.\n\n주요 검토 사항:\n1. 개인정보 비식별화 기준\n2. 데이터 접근 권한 체계\n3. 데이터 품질 관리 기준\n4. 보존 기간 및 삭제 정책\n\n법무팀, 정보보안팀 협의 후 5월 중 정책 확정 예정입니다.", "데이터 분석 플랫폼", 12),
    (14, 4,  1, 11, "클라우드 마이그레이션 사전 조사 결과",
     "클라우드 마이그레이션을 위한 현행 인프라 사전 조사 결과입니다.\n\n현행 서버 현황:\n- 온프레미스 서버: 47대\n- 가상화 서버: 23대\n- 연간 인프라 운영 비용: 약 4억 8천만원\n\n클라우드 전환 시 예상 절감액: 약 1억 5천만원/년\n전환 우선 대상: 개발/테스트 환경 → 웹 서비스 → 배치 시스템\n\n상세 분석 보고서는 4월 15일 제출 예정입니다.", "클라우드 마이그레이션", 13),
    (15, 4,  3, 14, "Proma 개발 스프린트 1 완료 보고",
     "Proma 개발 프로젝트 스프린트 1이 완료되었습니다.\n\n완료 항목:\n- 프로젝트 CRUD 기능\n- 태스크 관리 기능\n- 이메일 수신 및 파싱\n- 기본 AI 분류 모델 연동\n\n스프린트 2 계획:\n- 일정 관리 Calendar View\n- AI 답장 초안 생성\n- 대시보드 개선\n\n회고 미팅은 4월 5일 오후 3시입니다.", "Proma 개발", 14),
    (16, 4,  6,  9, "ERP 구축 현장 방문 결과 보고",
     "4월 4일 실시한 ERP 구축 현장 방문 결과를 보고드립니다.\n\n방문 공장: 안산 2공장, 평택 공장\n\n주요 확인 사항:\n- 바코드 스캐너 26대 교체 필요\n- 생산 라인 PC 노후화로 성능 문제 우려\n- 네트워크 증설 필요 구역 3곳 확인\n\n인프라 추가 예산 약 8천만원 필요합니다.\n다음 주 예산 협의 회의에서 검토 예정입니다.", "ERP 구축", 0),
    (17, 4,  8, 10, "MES 개선 인터페이스 설계서 검토 의견",
     "MES 개선 프로젝트 인터페이스 설계서에 대한 검토 의견을 회신드립니다.\n\n수정 요청 사항:\n1. PLC 통신 프로토콜: OPC-UA 우선 적용 (현재 Modbus 설계)\n2. 데이터 수집 주기: 1초 → 500ms 단축 요청\n3. 알람 처리 우선순위 체계 추가 필요\n\n수정된 설계서는 4월 15일까지 제출 부탁드립니다.", "MES 개선", 1),
    (18, 4, 10, 14, "품질관리 시스템 검사 기준서 초안 공유",
     "품질관리 시스템에 적용할 검사 기준서 초안을 공유드립니다.\n\n초안 주요 내용:\n- 입고 검사 기준 (AQL 수준별 샘플링)\n- 공정 검사 기준 (SPC 관리 한계)\n- 출하 검사 기준 (100% 전수 검사 품목)\n\n4월 17일까지 현장 의견 취합 후 최종 확정 예정입니다.\n품질팀과의 협의에 도움 주시기 바랍니다.", "품질관리 시스템", 5),
    (19, 4, 13,  9, "인사관리 시스템 급여 계산 로직 검증 요청",
     "인사관리 시스템 급여 계산 로직 검증을 요청드립니다.\n\n검증 필요 항목:\n- 통상임금 계산 방식\n- 초과근무 수당 산출\n- 4대보험 공제 로직\n- 연말정산 자동 계산\n\n현행 급여 프로그램과 결과 비교 테스트를 4월 25일까지 완료해야 합니다.\n급여팀 협조 부탁드립니다.", "인사관리 시스템", 6),
    (20, 4, 15, 11, "구매관리 시스템 전자입찰 기능 요건 추가",
     "구매관리 시스템 범위에 전자입찰 기능 추가를 요청드립니다.\n\n추가 요건:\n- 입찰 공고 등록 및 공개\n- 업체별 입찰서 온라인 접수\n- 개찰 및 낙찰 처리\n- 계약서 전자 서명 연동\n\n범위 추가에 따른 일정 및 예산 영향도 분석을 5월 1일까지 보고해 주세요.", "구매관리 시스템", 7),
    (21, 4, 17, 14, "고객관리 시스템 API 연동 테스트 결과",
     "고객관리 시스템 외부 API 연동 테스트 결과를 보고드립니다.\n\n테스트 항목: 카카오 알림톡, SMS 발송, 이메일 발송\n\n결과:\n- 카카오 알림톡: 정상 (발송 성공률 99.8%)\n- SMS: 정상 (LGU+ 연동)\n- 이메일: SMTP 인증 오류 발생 → 수정 중\n\n이메일 발송 기능은 4월 25일까지 재테스트 예정입니다.", "고객관리 시스템", 8),
    (22, 4, 20,  9, "물류관리 시스템 바코드 라벨 설계 확정",
     "물류관리 시스템에 적용할 바코드 라벨 표준을 확정하여 안내드립니다.\n\n적용 규격: GS1-128 바코드\n라벨 포함 정보:\n- 품목 코드, 수량, 로트번호\n- 유효기간, 입고일\n- QR코드 (모바일 확인용)\n\n라벨 출력 프린터: Zebra ZT410 (각 창고별 2대)\n소프트웨어: ZPL 방식 적용", "물류관리 시스템", 9),
    (23, 4, 22, 10, "보안 인프라 개선 제로트러스트 도입 검토",
     "보안 인프라 개선 프로젝트에 제로트러스트 아키텍처 도입을 검토해 주시기 바랍니다.\n\n현황 문제:\n- VPN 기반 원격접속의 보안 한계\n- 내부망 신뢰 과도 부여\n\n도입 검토 솔루션:\n1. Zscaler ZIA/ZPA\n2. Palo Alto Prisma Access\n3. 국산 솔루션 (파수, 지니언스)\n\n PoC 일정: 5월~6월 (2개월)\n최종 선정: 7월 예정", "보안 인프라 개선", 10),
    (24, 4, 24, 14, "모바일 앱 개발 QA 테스트 케이스 작성 완료",
     "모바일 앱 개발 QA 테스트 케이스 작성이 완료되었습니다.\n\n작성 현황:\n- 기능 테스트: 287개\n- 회귀 테스트: 143개\n- 성능 테스트: 32개\n- 보안 테스트: 25개\n\n테스트 도구: Appium (자동화), TestRail (관리)\n1차 테스트 실행: 5월 1일 예정\n\n테스트 케이스 검토에 개발팀 참여 부탁드립니다.", "모바일 앱 개발", 11),
    (25, 4, 27,  9, "데이터 분석 플랫폼 ETL 설계 완료",
     "데이터 분석 플랫폼 ETL(추출/변환/적재) 파이프라인 설계가 완료되었습니다.\n\n설계 내용:\n- 소스 시스템: ERP, MES, CRM, 물류 시스템\n- ETL 도구: Apache Airflow + Spark\n- 데이터 레이크: AWS S3\n- 데이터 웨어하우스: Snowflake\n\n구현 착수: 5월 4일\n1차 파이프라인 완성: 6월 30일 목표", "데이터 분석 플랫폼", 12),
    (26, 4, 29, 11, "클라우드 마이그레이션 CSP 선정 결과",
     "클라우드 서비스 제공업체(CSP) 최종 선정 결과를 보고드립니다.\n\n선정: AWS (Amazon Web Services)\n선정 이유:\n- 국내 리전 운영 (서울, 부산)\n- 금융/공공 레퍼런스 다수\n- 기술 지원 체계 우수\n- 협상 결과 최적 가격 확보\n\n계약 체결: 5월 2일 예정\nPOC 환경 구성: 5월 중순 예정", "클라우드 마이그레이션", 13),
    (27, 5,  4,  9, "Proma 개발 AI 분류 정확도 개선 결과",
     "Proma 이메일 AI 분류 모델 정확도 개선 결과를 보고드립니다.\n\n개선 전: 정확도 74.3%\n개선 후: 정확도 91.2%\n\n주요 개선 사항:\n- 학습 데이터 3배 확충 (500 → 1,500건)\n- 프로젝트명 키워드 가중치 조정\n- 부정확 분류 패턴 수동 레이블링\n\n다음 목표: 95% 정확도 달성 (6월 말)\n추가 학습 데이터 수집 중입니다.", "Proma 개발", 14),
    (28, 5,  6, 14, "ERP 구축 2차 개발 착수 보고",
     "ERP 구축 2차 개발이 착수되었습니다.\n\n2차 개발 범위:\n- 구매/조달 모듈\n- 회계/원가 모듈\n- 인사/급여 모듈 연계\n\n투입 인력:\n- 개발팀 8명\n- 컨설턴트 3명\n\n2차 개발 완료 목표: 8월 31일\n중간 점검 회의: 7월 1일 예정", "ERP 구축", 0),
    (29, 5,  8, 10, "MES 개선 설비 연동 테스트 완료",
     "MES 개선 프로젝트 설비 연동 테스트가 완료되었습니다.\n\n테스트 대상 설비: CNC 머시닝센터 12대, 사출성형기 8대\n\n결과:\n- 실시간 가동 현황 수집: 정상\n- 알람 신호 전달: 정상\n- 생산 카운터 연동: 2대 오류 발생 → 수정 완료\n\n다음 단계: 생산 현장 시범 운영 (5월 20일~6월 10일)", "MES 개선", 1),
    (30, 5, 10,  9, "전자결재 시스템 모바일 서명 기능 추가",
     "전자결재 시스템에 모바일 전자서명 기능 추가가 확정되었습니다.\n\n추가 기능:\n- 공인인증서 기반 전자서명\n- 생체인증 (지문/Face ID) 연동\n- 결재선 모바일 변경 기능\n\n개발 일정: 5월 15일~6월 30일\n추가 개발비: 약 2,500만원\n\n계약 변경은 5월 15일까지 완료 예정입니다.", "전자결재 시스템", 2),
    (31, 5, 12, 14, "그룹웨어 개선 성능 테스트 결과",
     "그룹웨어 개선 버전 성능 테스트 결과를 보고드립니다.\n\n테스트 환경: 500 동시 접속 시뮬레이션\n\n결과:\n- 로그인 응답: 평균 0.8초 (기존 3.2초)\n- 메일 목록 조회: 평균 1.1초 (기존 4.7초)\n- 파일 업로드 (10MB): 평균 2.3초 (기존 8.1초)\n\n성능 목표 달성! 6월 안정화 후 전사 배포 예정입니다.", "그룹웨어 개선", 4),
    (32, 5, 14, 10, "구매관리 시스템 테스트 환경 구성 완료",
     "구매관리 시스템 QA 테스트 환경 구성이 완료되었습니다.\n\n환경 구성:\n- 테스트 서버: 2대 (WAS, DB 분리)\n- 테스트 계정: 50개 생성 완료\n- 샘플 데이터: 거래처 300개, 품목 1,200개\n\n테스트 시작: 5월 18일\n테스트 완료 목표: 6월 15일\n\n테스트 참여 인원은 QA 팀장에게 배정 확인 바랍니다.", "구매관리 시스템", 7),
    (33, 5, 16,  9, "클라우드 마이그레이션 1단계 환경 구성 완료",
     "클라우드 마이그레이션 1단계 AWS 환경 구성이 완료되었습니다.\n\n구성 완료 항목:\n- VPC 및 서브넷 설계/구성\n- IAM 계정 및 권한 체계\n- 기본 보안 그룹 설정\n- 개발/테스트 환경 서버 배포\n\n다음 단계: 개발 환경 마이그레이션 (5월 25일 예정)\n운영 환경 이전: 8월 예정\n\n상세 아키텍처 도식은 컨플루언스 참고 바랍니다.", "클라우드 마이그레이션", 13),
]

for idx, (num, month, day, hour, subject, body, project, sender_idx) in enumerate(work_mails):
    s_name, s_email = SENDERS[sender_idx % len(SENDERS)]
    content = simple_eml(f"mail{num:03d}", s_name, s_email, subject, body, make_date(month, day, hour))
    write_eml(f"mail_{num:03d}.eml", content)

# ── mail_034~053: 프로젝트 관련 메일 ─────────────────────────────────────
project_mails = [
    (34, 3,  2,  9, "ERP 시스템 도입 필요성 검토 보고", "ERP 구축",
     "당사 ERP 시스템 도입의 필요성 및 기대 효과에 대한 검토 보고서를 제출합니다.\n\n현행 문제점:\n- 부서별 분산된 엑셀 관리로 인한 데이터 불일치\n- 실시간 경영 현황 파악 불가\n- 반복 업무로 인한 인력 낭비\n\nERP 도입 시 기대 효과:\n- 업무 효율 30% 향상\n- 데이터 정합성 확보\n- 의사결정 속도 향상"),
    (35, 3,  4, 10, "MES 생산 관리 현황 분석", "MES 개선",
     "현행 MES 시스템의 생산 관리 현황을 분석한 결과를 보고드립니다.\n\n주요 분석 결과:\n- 설비 가동률: 평균 68.3% (목표 85%)\n- OEE: 52.1% (업계 평균 65%)\n- 불량률: 2.8% (목표 1.5%)\n\nMES 개선을 통한 목표:\n- 설비 가동률 80% 달성\n- OEE 60% 이상\n- 불량률 2% 미만"),
    (36, 3,  6, 14, "전자결재 워크플로우 설계 검토", "전자결재 시스템",
     "전자결재 시스템 워크플로우 설계안에 대한 검토 의견을 드립니다.\n\n현행 결재 프로세스 분석:\n- 평균 결재 소요 시간: 3.2일\n- 반려율: 12.4%\n- 종이 문서 연간 사용량: 48,000장\n\n전자결재 도입 후 목표:\n- 결재 소요 시간: 0.5일 이내\n- 반려율: 8% 이하\n- 종이 문서 80% 감소"),
    (37, 3,  9, 11, "생산관리 시스템 생산 계획 모듈 설계", "생산관리 시스템",
     "생산관리 시스템 생산 계획 모듈 설계서를 검토해 주시기 바랍니다.\n\n주요 기능:\n1. 주간/월간 생산 계획 수립\n2. 자재 소요량 계획(MRP) 연동\n3. 능력 소요 계획(CRP) 분석\n4. 생산 계획 변경 이력 관리\n\n설계 완료: 3월 20일 예정"),
    (38, 3, 11,  9, "그룹웨어 화상회의 솔루션 선정", "그룹웨어 개선",
     "그룹웨어 개선 프로젝트에서 화상회의 솔루션 최종 선정 결과를 안내드립니다.\n\n선정: Cisco Webex Enterprise\n선정 이유:\n- 500인 동시 접속 지원\n- 녹화 및 자막 기능\n- 기존 AD 계정 연동\n- 보안 인증(CC인증) 보유\n\n서비스 적용: 4월 1일 예정"),
    (39, 3, 13, 14, "품질관리 통계적 공정 관리 도입 계획", "품질관리 시스템",
     "품질관리 시스템에 SPC(통계적 공정 관리) 도입 계획을 공유드립니다.\n\n도입 범위:\n- 주요 공정 15개 적용\n- 관리도 종류: X-bar R, X-bar S, P관리도\n- 실시간 모니터링 대시보드\n\n기대 효과:\n- 공정 이상 조기 감지\n- 불량 사전 예방\n- 품질 데이터 축적"),
    (40, 3, 16, 10, "인사관리 채용 프로세스 디지털화 방안", "인사관리 시스템",
     "인사관리 시스템을 활용한 채용 프로세스 디지털화 방안을 검토합니다.\n\n현행 문제:\n- 입사 지원서 이메일 수기 처리\n- 면접 일정 조율 수동 진행\n- 합격자 온보딩 서류 반복 제출\n\n디지털화 방안:\n- 온라인 입사 지원 시스템\n- AI 기반 서류 1차 스크리닝\n- 화상 면접 통합 관리"),
    (41, 3, 18, 11, "구매관리 공급망 리스크 관리 기능", "구매관리 시스템",
     "구매관리 시스템에 공급망 리스크 관리 기능 추가를 제안드립니다.\n\n리스크 관리 기능:\n- 공급업체 재무 건전성 모니터링\n- 납기 지연 예측 알림\n- 대체 공급업체 정보 관리\n- 비상 조달 프로세스 지원\n\n이 기능은 2단계 개발 범위로 포함 요청드립니다."),
    (42, 3, 20,  9, "고객관리 고객 세그먼테이션 분석 요청", "고객관리 시스템",
     "고객관리 시스템 구축 전 현행 고객 데이터 세그먼테이션 분석을 요청드립니다.\n\n분석 대상:\n- 활성 고객 12,400명\n- 구매 이력 3년치\n\n분석 요청 항목:\n1. RFM 분석 (최근 구매, 빈도, 금액)\n2. 고객 생애 가치(LTV) 산출\n3. 이탈 위험 고객 식별\n\n분석 결과는 CRM 1차 요구사항에 반영 예정입니다."),
    (43, 3, 23, 14, "물류관리 실시간 배송 추적 기능 요건", "물류관리 시스템",
     "물류관리 시스템 실시간 배송 추적 기능 요건을 정의합니다.\n\n기능 요건:\n- 배송사 API 연동 (CJ대한통운, 한진, 롯데택배)\n- GPS 기반 차량 위치 추적\n- 고객 SMS/카카오 알림 자동 발송\n- 배송 예상 도착 시간 표시\n\n연동 대상 배송사는 5월까지 최종 확정 예정입니다."),
    (44, 3, 25, 10, "보안 인프라 망분리 솔루션 도입 검토", "보안 인프라 개선",
     "보안 인프라 개선을 위한 망분리 솔루션 도입을 검토합니다.\n\n현황:\n- 인터넷망/업무망 논리적 분리만 적용\n- 물리적 망분리 미적용\n\n검토 솔루션:\n1. 가상화 기반 망분리 (VM)\n2. 스트리밍 기반 망분리\n3. CBT(클라이언트 기반) 방식\n\n도입 비용 및 사용자 편의성 종합 검토 후 4월 중 결정 예정"),
    (45, 3, 27,  9, "모바일 앱 푸시 알림 시스템 설계", "모바일 앱 개발",
     "모바일 앱 개발 프로젝트 푸시 알림 시스템 설계서를 공유드립니다.\n\n알림 종류:\n- 업무 요청/승인 알림\n- 일정 리마인더\n- 공지사항 알림\n- 긴급 알림\n\n기술 스택:\n- FCM (Firebase Cloud Messaging)\n- APNs (Apple Push Notification service)\n- 알림 서버: Node.js + Redis"),
    (46, 4,  2, 14, "데이터 분석 플랫폼 BI 도구 선정", "데이터 분석 플랫폼",
     "데이터 분석 플랫폼 BI(Business Intelligence) 도구 최종 선정 결과입니다.\n\n선정: Tableau Server + Power BI 이중 도입\n\n사용 목적 구분:\n- Tableau: 경영진용 대시보드, 복잡한 시각화\n- Power BI: 팀별 자율 분석, Office 365 연동\n\n라이선스 비용: 연간 약 4,200만원\n구축 완료 목표: 7월 31일"),
    (47, 4,  7, 10, "클라우드 마이그레이션 보안 아키텍처 설계", "클라우드 마이그레이션",
     "클라우드 마이그레이션을 위한 보안 아키텍처 설계안을 공유드립니다.\n\n보안 구성 요소:\n- WAF (AWS WAF)\n- DDoS 방어 (AWS Shield)\n- 암호화 (AWS KMS)\n- 접근 제어 (AWS IAM + SSO)\n- 감사 로그 (CloudTrail + CloudWatch)\n\n보안 검토는 정보보안팀과 협의하여 4월 20일까지 완료 예정입니다."),
    (48, 4,  9, 11, "ERP 구축 기준 정보 등록 현황", "ERP 구축",
     "ERP 시스템 운영을 위한 기준 정보 등록 현황을 보고드립니다.\n\n등록 현황 (목표 대비):\n- 품목 마스터: 8,234건 / 9,000건 (91.5%)\n- 거래처 마스터: 1,456건 / 1,500건 (97.1%)\n- BOM: 3,267건 / 4,000건 (81.7%)\n- 공정 마스터: 234건 / 280건 (83.6%)\n\n미등록 데이터는 5월 15일까지 완료 목표입니다."),
    (49, 4, 11,  9, "MES 생산 실적 집계 로직 검토", "MES 개선",
     "MES 개선 프로젝트 생산 실적 집계 로직에 대한 검토 의견을 요청드립니다.\n\n현재 설계:\n- 작업자 수동 입력 방식\n- 교대 기준 집계 (3교대)\n- 불량 유형 코드: 15종\n\n추가 요청:\n- 자동 카운터 연동 시 실적 자동 집계\n- 불량 유형 확장 (15 → 30종)\n- 생산 중단 사유 코드 추가"),
    (50, 4, 13, 14, "전자결재 결재 문서 보존 정책 수립", "전자결재 시스템",
     "전자결재 시스템의 문서 보존 정책을 수립합니다.\n\n보존 기간 (법적 기준):\n- 이사회 의사록: 영구\n- 계약서: 10년\n- 세금계산서: 5년\n- 일반 품의서: 3년\n\n시스템 요건:\n- 문서 위·변조 방지 (해시값 저장)\n- 장기 보존 포맷: PDF/A\n- 보존 기간 만료 시 자동 알림"),
    (51, 4, 14, 10, "그룹웨어 전자메일 보안 강화", "그룹웨어 개선",
     "그룹웨어 개선 프로젝트에서 이메일 보안 기능 강화 방안을 공유드립니다.\n\n강화 방안:\n1. 스팸/피싱 필터링 고도화\n2. 메일 암호화 (S/MIME)\n3. 외부 발송 승인 프로세스\n4. 대용량 첨부파일 링크 방식 전환\n5. 발신자 인증 (SPF, DKIM, DMARC)\n\n5월 중 보안 업그레이드 적용 예정입니다."),
    (52, 4, 16, 11, "인사관리 성과 평가 시스템 연동", "인사관리 시스템",
     "인사관리 시스템과 성과 평가 시스템 연동 방안을 검토합니다.\n\n연동 정보:\n- 목표 설정 및 진행 현황\n- 역량 평가 결과\n- 360도 다면 평가\n- 성과급 산정 기준 데이터\n\n연동 방식: REST API (JSON)\n연동 주기: 실시간 (이벤트 기반)\n\n성과 평가 시스템 담당팀과 4월 25일 협의 예정"),
    (53, 4, 18,  9, "구매관리 시스템 전자세금계산서 연동", "구매관리 시스템",
     "구매관리 시스템에 전자세금계산서 자동 연동 기능을 추가합니다.\n\n연동 범위:\n- 홈택스 전자세금계산서 수신\n- 매입 전표 자동 생성\n- ERP 회계 모듈 자동 연계\n\n연동 솔루션: 케이렉스 전자세금계산서 솔루션\n구축 일정: 5월~6월\n예상 비용: 1,800만원 (구축) + 연 300만원 (유지보수)"),
]

for num, month, day, hour, subject, project, body in project_mails:
    sender_idx = (num - 34) % len(SENDERS)
    s_name, s_email = SENDERS[sender_idx]
    content = simple_eml(f"mail{num:03d}", s_name, s_email, subject, body, make_date(month, day, hour))
    write_eml(f"mail_{num:03d}.eml", content)

# ── mail_054~068: 일정 관련 메일 ─────────────────────────────────────────
schedule_mails = [
    (54, 3,  3, 10, "ERP 구축 주간 회의 안내 (3/10)",
     "ERP 구축 프로젝트 주간 회의를 안내드립니다.\n\n일시: 2026년 3월 10일(화) 오전 10:00\n장소: 본관 2층 대회의실\n참석자: 프로젝트팀 전원\n\n안건:\n1. 주간 진행 현황 보고\n2. 이슈 및 리스크 공유\n3. 다음 주 계획 확인\n\n자료는 회의 전날까지 공유 부탁드립니다."),
    (55, 3,  6, 11, "MES 개선 착수 회의 일정 변경 안내",
     "MES 개선 프로젝트 착수 회의 일정이 변경되었습니다.\n\n변경 전: 3월 9일(월) 10:00\n변경 후: 3월 11일(수) 14:00\n장소: 동일 (공장 2층 회의실)\n\n일정 변경 사유: 공장장 외부 일정 충돌\n변경된 일정 캘린더에 업데이트 부탁드립니다."),
    (56, 3, 10,  9, "전자결재 시스템 킥오프 미팅 안내",
     "전자결재 시스템 프로젝트 킥오프 미팅을 안내드립니다.\n\n일시: 2026년 3월 16일(월) 오후 2:00\n장소: IT센터 3층 회의실 A\n참석 대상: PM, 개발팀, 컨설턴트, 사용자 대표\n\n킥오프 순서:\n1. 프로젝트 개요 설명\n2. 팀원 소개\n3. 추진 일정 공유\n4. 협업 규칙 및 도구 안내\n\n도시락 제공 예정입니다."),
    (57, 3, 13, 14, "생산관리 시스템 설계 검토 회의 (3/20)",
     "생산관리 시스템 설계 검토 회의를 안내드립니다.\n\n일시: 3월 20일(금) 오전 10:00~12:00\n장소: 본관 대회의실\n\n검토 항목:\n1. 생산 계획 화면 설계\n2. 작업 지시 프로세스\n3. 실적 집계 방식\n\n설계서는 3월 18일까지 공유 예정입니다."),
    (58, 3, 17, 10, "품질관리 시스템 워크숍 일정 안내",
     "품질관리 시스템 워크숍 일정을 안내드립니다.\n\n일시: 3월 25일(수)~26일(목) 1박 2일\n장소: 용인 연수원\n대상: 품질팀, 생산팀, IT팀\n\n워크숍 내용:\n- 품질 관리 현황 및 문제점 공유\n- To-Be 프로세스 설계\n- 시스템 요건 도출\n\n참가 여부를 3월 20일까지 회신해 주세요."),
    (59, 3, 20,  9, "모바일 앱 UX 리뷰 회의 (4/3)",
     "모바일 앱 개발 UX 리뷰 회의를 안내드립니다.\n\n일시: 4월 3일(금) 오후 3:00\n장소: 디자인센터 1층 회의실\n참석자: UX 디자이너, 개발팀 리드, PM\n\n리뷰 내용:\n- 메인 화면 와이어프레임\n- 주요 플로우 UX 검토\n- 디자인 시스템 적용 방안\n\n프로토타입은 회의 당일 시연 예정입니다."),
    (60, 3, 24, 11, "데이터 분석 플랫폼 착수 회의 (4/7)",
     "데이터 분석 플랫폼 프로젝트 착수 회의를 안내드립니다.\n\n일시: 4월 7일(화) 오전 10:00\n장소: 본관 5층 소회의실\n\n착수 안건:\n1. 프로젝트 목표 및 범위 확인\n2. WBS 검토\n3. 데이터 현황 조사 방법론\n\n참석 필수: 데이터 분석팀, IT팀, 기획팀"),
    (61, 3, 27, 14, "ERP 구축 월간 진행 보고 (4/10)",
     "ERP 구축 프로젝트 4월 월간 진행 보고 회의를 안내드립니다.\n\n일시: 4월 10일(금) 오후 2:00\n장소: 임원회의실\n\n보고 내용:\n1. 3월 진행 현황 (완료율)\n2. 4월 계획\n3. 예산 집행 현황\n4. 리스크 현황\n\n임원진 참석 예정이니 보고 자료 완성도 높여 주시기 바랍니다."),
    (62, 4,  1,  9, "클라우드 마이그레이션 기술 검토 회의",
     "클라우드 마이그레이션 기술 검토 회의를 안내드립니다.\n\n일시: 4월 15일(수) 오전 10:00~12:00\n장소: IT센터 회의실\n\n검토 의제:\n1. 마이그레이션 전략 (Lift & Shift vs Re-architecture)\n2. 네트워크 아키텍처 설계\n3. 보안 요건 정의\n4. 재해 복구 방안\n\nAWS 솔루션 아키텍트 참석 예정입니다."),
    (63, 4,  5, 10, "그룹웨어 개선 Beta 테스트 일정 안내",
     "그룹웨어 개선 Beta 버전 테스트 일정을 안내드립니다.\n\n테스트 기간: 4월 20일(월)~5월 1일(금)\n테스터 모집: 각 팀 대표 1명 (총 20명)\n\n테스트 항목:\n- 이메일 기능\n- 캘린더\n- 전자결재 연동\n- 모바일 앱\n\n테스터 신청은 4월 10일까지 IT팀으로 제출해 주세요."),
    (64, 4,  8, 14, "인사관리 시스템 데모 시연 일정",
     "인사관리 시스템 1차 데모 시연 일정을 안내드립니다.\n\n일시: 4월 28일(화) 오후 2:00\n장소: 인사팀 교육실\n대상: 인사팀 전원\n\n시연 항목:\n- 임직원 정보 관리\n- 발령 처리\n- 근태 관리\n- 급여 계산 (테스트)\n\n시연 후 의견 수렴하여 개선 사항 반영 예정입니다."),
    (65, 4, 12,  9, "물류관리 현장 실사 일정 (4/22~23)",
     "물류관리 시스템 구축을 위한 창고 현장 실사 일정입니다.\n\n일정: 4월 22일(수)~23일(목)\n대상 창고: 인천 물류센터, 수원 배송센터\n\n실사 내용:\n- 현행 입출고 프로세스 파악\n- 바코드/RFID 인프라 현황\n- 냉장/냉동 구역 특이 사항\n\n현장 담당자와 사전 협의 후 일정 확정하겠습니다."),
    (66, 4, 16, 11, "Proma 개발 스프린트 2 계획 회의",
     "Proma 개발 스프린트 2 계획 회의를 안내드립니다.\n\n일시: 4월 21일(화) 오전 10:00\n장소: 개발실\n\n스프린트 2 후보 기능:\n- 이메일 스레드 시각화\n- 일정 Calendar View\n- AI 답장 초안 생성\n- 알림 기능\n\n스프린트 용량 확인 후 우선순위 결정 예정입니다."),
    (67, 4, 20,  9, "구매관리 시스템 통합 테스트 계획 회의",
     "구매관리 시스템 통합 테스트 계획 회의를 안내드립니다.\n\n일시: 5월 4일(월) 오전 10:00\n장소: IT센터 회의실 B\n\n회의 목적:\n- 통합 테스트 범위 확정\n- 테스트 케이스 검토\n- 테스트 팀 구성\n- 결함 관리 프로세스 확정\n\n개발팀, QA팀, 업무팀 참석 필수입니다."),
    (68, 4, 24, 14, "보안 인프라 개선 PoC 결과 발표 (5/8)",
     "보안 인프라 개선 PoC 결과 발표 회의를 안내드립니다.\n\n일시: 5월 8일(금) 오후 2:00\n장소: 임원회의실\n발표자: 보안팀 + PoC 참여 벤더\n\n발표 내용:\n- 제로트러스트 PoC 결과\n- 제품별 기능 비교\n- 비용 및 도입 일정 제안\n\n최종 솔루션 결정은 5월 15일 예정입니다."),
]

for num, month, day, hour, subject, body in schedule_mails:
    sender_idx = (num - 54) % len(SENDERS)
    s_name, s_email = SENDERS[sender_idx]
    content = simple_eml(f"mail{num:03d}", s_name, s_email, subject, body, make_date(month, day, hour))
    write_eml(f"mail_{num:03d}.eml", content)

# ── mail_069~078: 회의록 메일 ────────────────────────────────────────────
minutes_mails = [
    (69, 3,  4, 15, "회의록: ERP 구축 착수 회의 (3/4)",
     "ERP 구축 착수 회의 회의록을 공유드립니다.\n\n일시: 2026년 3월 4일(수) 14:00~16:00\n참석자: 김민준(PM), 이서연, 박지훈, 최유진, 정수빈\n\n회의 내용:\n1. 프로젝트 목표 및 범위 확인\n2. 팀 구성 및 역할 분담\n3. 일정 검토\n\n액션 아이템:\n- [김민준] 프로젝트 계획서 최종본 3/10까지 배포\n- [이서연] 현행 업무 프로세스 분석 시작\n- [박지훈] 개발 환경 구성 3/6까지 완료\n- [최유진] 사용자 인터뷰 일정 3/7까지 확정\n\n다음 회의: 3월 10일(화) 10:00"),
    (70, 3, 11, 15, "회의록: MES 개선 1차 요건 정의 회의",
     "MES 개선 1차 요건 정의 회의 회의록입니다.\n\n일시: 2026년 3월 11일(수) 14:00~16:30\n참석자: 한승우, 오다은, 임재원, 현장 담당자 3명\n\n주요 논의 사항:\n- 현행 MES 문제점 12가지 도출\n- 개선 요건 우선순위 결정\n- 현장 데이터 수집 방식 논의\n\n액션 아이템:\n- [한승우] 요건 정의서 초안 3/18까지 작성\n- [임재원] PLC 통신 프로토콜 사양 3/13까지 확인\n- [오다은] 기존 MES 벤더 미팅 3/16 조율\n\n차기 회의: 3월 18일(수) 10:00"),
    (71, 3, 18, 16, "회의록: 그룹웨어 개선 요건 워크숍",
     "그룹웨어 개선 요건 워크숍 회의록을 공유합니다.\n\n일시: 2026년 3월 18일(수) 10:00~17:00\n장소: 연수원 3층 세미나실\n참석자: 각 팀 대표 15명\n\n워크숍 결과:\n- 핵심 개선 요건 28가지 도출\n- 우선순위: 성능 개선 > 모바일 > 화상회의\n- 제외 항목 5가지 확정\n\n액션 아이템:\n- [신예린] 요건 목록 취합 및 3/20까지 배포\n- [강태양] 벤더 데모 일정 4/1~5 조율\n- 전 참석자: 요건 우선순위 투표 3/20까지 완료"),
    (72, 3, 25, 15, "회의록: 전자결재 시스템 설계 검토 (3/25)",
     "전자결재 시스템 설계 검토 회의록입니다.\n\n일시: 2026년 3월 25일(수) 14:00~16:00\n참석자: 윤하늘(PM), 장소희, 홍길동, 배수진\n\n검토 결과:\n- 결재 워크플로우 엔진: Camunda BPM 선정\n- 문서 저장: S3 + 메타데이터 DB\n- 전자서명 솔루션: 드림시큐리티 확정\n\n액션 아이템:\n- [장소희] API 설계서 4/3까지 완성\n- [홍길동] 전자서명 벤더 계약 4/7까지 완료\n- [배수진] DB 스키마 설계 4/1까지 초안 작성\n\n차기 회의: 4월 7일"),
    (73, 4,  8, 15, "회의록: 고객관리 시스템 1차 설계 리뷰",
     "고객관리 시스템 1차 설계 리뷰 회의록을 공유드립니다.\n\n일시: 2026년 4월 8일(수) 14:00~16:00\n참석자: 조민서(PM), 개발팀 4명, 사용자 대표 2명\n\n주요 결정 사항:\n- 고객 세그먼트: 7개 그룹으로 정의\n- 영업 파이프라인 단계: 5단계 (리드-기회-제안-협상-계약)\n- 모바일 앱 우선 지원 결정\n\n액션 아이템:\n- [조민서] 설계서 수정본 4/15까지 배포\n- [개발팀] DB ERD 수정 4/12까지\n- [사용자 대표] 고객 코드 체계 4/10까지 확정\n\n차기 회의: 4월 20일"),
    (74, 4, 15, 16, "회의록: 인사관리 시스템 데이터 마이그레이션 회의",
     "인사관리 시스템 데이터 마이그레이션 회의록입니다.\n\n일시: 2026년 4월 15일(수) 14:00~15:30\n참석자: 한승우, 인사팀 담당자 3명, DBA 1명\n\n논의 결과:\n- 마이그레이션 도구: Python 스크립트 자체 개발\n- 데이터 정제 담당: 인사팀 자체 처리\n- 마이그레이션 완료 기준: 오류율 0.1% 이하\n\n액션 아이템:\n- [DBA] 소스 DB 분석 4/18까지\n- [인사팀] 데이터 정제 가이드 작성 4/20까지\n- [한승우] 마이그레이션 스크립트 개발 4/25까지"),
    (75, 4, 22, 15, "회의록: 클라우드 마이그레이션 아키텍처 확정 회의",
     "클라우드 마이그레이션 아키텍처 확정 회의록을 공유합니다.\n\n일시: 2026년 4월 22일(수) 10:00~12:00\n참석자: 임재원(PM), AWS SA, 보안팀장, 인프라팀장\n\n확정 사항:\n- 리전: ap-northeast-2 (서울)\n- 멀티 AZ 구성: 필수 적용\n- 재해 복구 목표: RTO 4시간, RPO 1시간\n- VPN 연결: AWS Site-to-Site VPN\n\n액션 아이템:\n- [임재원] 아키텍처 확정본 4/25 배포\n- [인프라팀] VPN 설정 4/28까지\n- [보안팀] 보안 정책 문서 4/30까지"),
    (76, 5,  6, 15, "회의록: Proma 스프린트 2 회고 미팅",
     "Proma 개발 스프린트 2 회고 미팅 회의록입니다.\n\n일시: 2026년 5월 6일(수) 15:00~16:00\n참석자: 개발팀 전원 (6명)\n\n잘한 점:\n- AI 분류 정확도 대폭 향상\n- Calendar View 기능 예정일 내 완료\n\n개선할 점:\n- 코드 리뷰 시간 확보 필요\n- 테스트 커버리지 60% → 80% 목표\n\n액션 아이템:\n- 스프린트 3 시작 전 기술 부채 정리 1일 할당\n- 자동화 테스트 강화\n- 매주 금요일 코드 리뷰 1시간 확보"),
    (77, 5, 13, 16, "회의록: 데이터 분석 플랫폼 데이터 품질 회의",
     "데이터 분석 플랫폼 데이터 품질 관리 회의록입니다.\n\n일시: 2026년 5월 13일(수) 14:00~16:00\n참석자: 신예린(PM), 데이터팀 3명, ERP팀 1명, MES팀 1명\n\n주요 이슈:\n- ERP 데이터 중복 키 4,234건 발견\n- MES 데이터 누락 기간: 2025년 11~12월\n- CRM 데이터 포맷 불일치\n\n액션 아이템:\n- [ERP팀] 중복 키 정제 5/20까지\n- [MES팀] 누락 데이터 복구 또는 대체값 협의 5/18\n- [신예린] 데이터 품질 기준서 5/25까지 작성"),
    (78, 5, 20, 15, "회의록: 보안 인프라 개선 PoC 중간 점검",
     "보안 인프라 개선 PoC 중간 점검 회의록을 공유드립니다.\n\n일시: 2026년 5월 20일(수) 14:00~15:30\n참석자: 강태양(보안팀장), PoC 참여 벤더 3사 담당자\n\nPoC 현황:\n- Zscaler: 성능 테스트 완료, 호환성 이슈 1건\n- Palo Alto: 정책 관리 UI 우수, 비용 높음\n- 국산 솔루션: 기능 제한적, 가격 경쟁력 있음\n\n액션 아이템:\n- 벤더 각사: 이슈 해결 방안 5/25까지 제출\n- [강태양] 비교 평가표 작성 5/27까지\n- 최종 선정 회의: 6월 3일 예정"),
]

for num, month, day, hour, subject, body in minutes_mails:
    sender_idx = (num - 69) % len(SENDERS)
    s_name, s_email = SENDERS[sender_idx]
    content = simple_eml(f"mail{num:03d}", s_name, s_email, subject, body, make_date(month, day, hour))
    write_eml(f"mail_{num:03d}.eml", content)

# ── mail_079~088: 첨부파일 메일 ─────────────────────────────────────────
def make_attachment_eml(mid, sender_name, sender_email, subject, body, date, attachments):
    boundary = f"boundary_{mid}"
    lines = [
        f"From: {sender_name} <{sender_email}>",
        f"To: {RECIPIENT[0]} <{RECIPIENT[1]}>",
        f"Subject: {subject}",
        f"Date: {date}",
        f"Message-ID: <{mid}@company.com>",
        "MIME-Version: 1.0",
        f'Content-Type: multipart/mixed; boundary="{boundary}"',
        "",
        f"--{boundary}",
        "Content-Type: text/plain; charset=UTF-8",
        "",
        body,
        "",
    ]
    for att_name, att_type, att_data in attachments:
        encoded = base64.b64encode(att_data).decode("ascii")
        lines += [
            f"--{boundary}",
            f'Content-Type: {att_type}; name="{att_name}"',
            "Content-Transfer-Encoding: base64",
            f'Content-Disposition: attachment; filename="{att_name}"',
            "",
        ]
        for i in range(0, len(encoded), 76):
            lines.append(encoded[i:i+76])
        lines.append("")
    lines.append(f"--{boundary}--")
    return "\n".join(lines)

# Dummy binary data for attachments
PDF_DUMMY = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\nxref\n0 1\n0000000000 65535 f\ntrailer\n<< /Root 1 0 R >>\nstartxref\n9\n%%EOF"
XLSX_DUMMY = b"PK\x03\x04\x14\x00\x00\x00\x00\x00" + b"\x00" * 50 + b"[Content_Types].xml" + b"\x00" * 30
DOCX_DUMMY = b"PK\x03\x04\x14\x00\x00\x00\x00\x00" + b"\x00" * 50 + b"word/document.xml" + b"\x00" * 30
PNG_DUMMY = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"

attachment_mails = [
    (79, 3,  5, 10, "ERP 구축 요구사항 명세서 첨부",
     "ERP 구축 요구사항 명세서를 첨부하여 발송드립니다.\n검토 후 의견을 3월 12일까지 회신해 주세요.",
     [("요구사항명세서_ERP.pdf", "application/pdf", PDF_DUMMY)]),
    (80, 3, 12, 11, "MES 개선 예산 계획서 첨부",
     "MES 개선 프로젝트 예산 계획서를 첨부드립니다.\n예산 검토 후 승인 요청드립니다.",
     [("MES_예산계획서.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", XLSX_DUMMY)]),
    (81, 3, 19, 14, "전자결재 시스템 제안서 첨부",
     "전자결재 시스템 구축 제안서입니다.\n견적 포함되어 있으니 검토 부탁드립니다.",
     [("전자결재_제안서.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", DOCX_DUMMY),
      ("견적서.pdf", "application/pdf", PDF_DUMMY)]),
    (82, 3, 26, 10, "품질관리 시스템 화면 설계안 이미지 첨부",
     "품질관리 시스템 화면 설계안 이미지를 첨부드립니다.\n UI 검토 후 의견 주세요.",
     [("화면설계_품질관리.png", "image/png", PNG_DUMMY)]),
    (83, 4,  2, 11, "생산관리 시스템 기능 명세서 첨부",
     "생산관리 시스템 기능 명세서를 첨부드립니다.\n확인 후 개발 착수 부탁드립니다.",
     [("생산관리_기능명세서.pdf", "application/pdf", PDF_DUMMY),
      ("생산관리_WBS.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", XLSX_DUMMY)]),
    (84, 4,  9, 14, "클라우드 마이그레이션 아키텍처 설계서 첨부",
     "AWS 클라우드 마이그레이션 아키텍처 설계서를 첨부합니다.",
     [("클라우드_아키텍처.pdf", "application/pdf", PDF_DUMMY)]),
    (85, 4, 16, 10, "보안 취약점 점검 보고서 첨부",
     "외부 보안 취약점 점검 보고서 첨부드립니다. 보안 사항이니 제한 배포 바랍니다.",
     [("취약점점검보고서.pdf", "application/pdf", PDF_DUMMY),
      ("조치계획서.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", DOCX_DUMMY)]),
    (86, 4, 23,  9, "데이터 분석 플랫폼 ETL 설계서 첨부",
     "데이터 분석 플랫폼 ETL 파이프라인 설계서를 첨부합니다.",
     [("ETL_설계서.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", DOCX_DUMMY)]),
    (87, 5,  7, 11, "모바일 앱 테스트 케이스 엑셀 첨부",
     "모바일 앱 전체 테스트 케이스 목록을 엑셀로 첨부합니다.",
     [("모바일앱_테스트케이스.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", XLSX_DUMMY)]),
    (88, 5, 14, 14, "인사관리 시스템 급여 계산 테스트 결과 첨부",
     "인사관리 시스템 급여 계산 검증 테스트 결과를 첨부드립니다.",
     [("급여계산_검증결과.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", XLSX_DUMMY),
      ("검증보고서.pdf", "application/pdf", PDF_DUMMY)]),
]

for num, month, day, hour, subject, body, attachments in attachment_mails:
    sender_idx = (num - 79) % len(SENDERS)
    s_name, s_email = SENDERS[sender_idx]
    content = make_attachment_eml(f"mail{num:03d}", s_name, s_email, subject, body, make_date(month, day, hour), attachments)
    write_eml(f"mail_{num:03d}.eml", content)

# ── mail_089~093: 영문 메일 ──────────────────────────────────────────────
english_mails = [
    (89, 3,  6, 10, "ERP Implementation Progress Update - Week 1",
     "Dear Team,\n\nPlease find below the progress update for the ERP implementation project for Week 1.\n\nCompleted tasks:\n- Project kickoff meeting conducted\n- Core team members assigned\n- Development environment setup\n- Initial requirements review started\n\nUpcoming tasks:\n- Requirements workshop (March 10-11)\n- Gap analysis initiation\n\nPlease review and provide feedback by EOD Friday.\n\nBest regards,\nMinjun Kim\nProject Manager"),
    (90, 3, 13, 11, "MES Improvement Project - Technical Review Request",
     "Hi,\n\nI am writing to request a technical review of the MES improvement project architecture design.\n\nKey points for review:\n1. PLC communication protocol selection (OPC-UA vs Modbus)\n2. Data collection frequency requirements\n3. Real-time monitoring dashboard architecture\n4. Integration with existing ERP system\n\nPlease share your feedback by March 20.\n\nThanks,\nSeoyeon Lee"),
    (91, 4,  3, 14, "Cloud Migration - AWS Architecture Proposal",
     "Dear Stakeholders,\n\nAttached is our proposed AWS cloud architecture for the migration project.\n\nHighlights:\n- Multi-AZ deployment for high availability\n- Auto-scaling groups for web and application tiers\n- RDS Aurora for database with read replicas\n- CloudFront CDN for static assets\n- Estimated monthly cost: USD 15,000\n\nPlease review and schedule a meeting to discuss.\n\nBest regards,\nJihoon Park\nCloud Architect"),
    (92, 4, 17,  9, "Data Analytics Platform - BI Tool Evaluation Summary",
     "Team,\n\nHere is the summary of our BI tool evaluation for the Data Analytics Platform project.\n\nEvaluation criteria:\n- Functionality (30%)\n- Performance (25%)\n- Ease of use (25%)\n- Total cost of ownership (20%)\n\nResults:\n1. Tableau: Score 87/100\n2. Power BI: Score 82/100\n3. Looker: Score 79/100\n\nRecommendation: Tableau for executive dashboards, Power BI for self-service.\n\nRegards,\nYujin Choi"),
    (93, 5,  5, 11, "Mobile App Development - QA Test Execution Report",
     "Hello,\n\nPlease find the QA test execution report for the Mobile App Development project.\n\nTest Summary:\n- Total test cases: 487\n- Passed: 423 (86.9%)\n- Failed: 52 (10.7%)\n- Blocked: 12 (2.5%)\n\nCritical defects found: 3\n- DEF-001: Login failure on iOS 17.4 (in progress)\n- DEF-002: Push notification delay on Android 14 (in progress)\n- DEF-003: Calendar sync error (fixed)\n\nTarget release date remains May 31.\n\nBest,\nSubin Jung"),
]

for num, month, day, hour, subject, body in english_mails:
    sender_idx = (num - 89) % len(SENDERS)
    s_name, s_email = SENDERS[sender_idx]
    content = simple_eml(f"mail{num:03d}", s_name, s_email, subject, body, make_date(month, day, hour))
    write_eml(f"mail_{num:03d}.eml", content)

# ── mail_094~098: 순수 한글 메일 ─────────────────────────────────────────
hangul_mails = [
    (94, 3,  7,  9, "안녕하세요 반갑습니다",
     "안녕하세요.\n\n저는 한승우입니다.\n이번에 그룹웨어 개선 프로젝트에 참여하게 되었습니다.\n\n앞으로 잘 부탁드립니다.\n열심히 하겠습니다.\n\n감사합니다."),
    (95, 3, 14, 10, "일정 조율 부탁드립니다",
     "안녕하세요.\n\n다음 주 회의 일정을 조율하고 싶습니다.\n\n가능한 시간:\n- 월요일 오전\n- 화요일 오후\n- 수요일 종일\n\n편하신 시간 알려 주시면 감사하겠습니다."),
    (96, 4,  5, 11, "요청 사항 확인 바랍니다",
     "안녕하세요.\n\n지난번에 요청드린 사항들 확인하셨나요?\n\n요청 사항:\n하나. 보고서 작성\n둘. 데이터 정리\n셋. 회의 자료 준비\n\n이번 주 안으로 처리 부탁드립니다.\n감사합니다."),
    (97, 4, 19, 14, "회의 결과 공유",
     "오늘 회의 결과를 공유드립니다.\n\n결정 사항:\n첫째, 다음 달부터 새로운 업무 프로세스를 적용합니다.\n둘째, 매주 월요일 오전에 팀 스탠드업 미팅을 진행합니다.\n셋째, 문서는 모두 협업 도구에 업로드합니다.\n\n궁금한 점은 연락 주세요."),
    (98, 5,  3,  9, "수고 많으셨습니다",
     "안녕하세요.\n\n이번 분기 동안 수고 많으셨습니다.\n\n여러분 덕분에 프로젝트가 순조롭게 진행되고 있습니다.\n\n다음 분기도 함께 열심히 해봅시다.\n\n건강 챙기시고 좋은 하루 되세요.\n감사합니다."),
]

for num, month, day, hour, subject, body in hangul_mails:
    sender_idx = (num - 94) % len(SENDERS)
    s_name, s_email = SENDERS[sender_idx]
    content = simple_eml(f"mail{num:03d}", s_name, s_email, subject, body, make_date(month, day, hour))
    write_eml(f"mail_{num:03d}.eml", content)

# ── mail_099~100: 자동 발송 메일 ─────────────────────────────────────────
auto_mails = [
    (99, 4, 10,  8, "noreply@company.kr", "[시스템 알림] ERP 구축 프로젝트 마감일 임박",
     "이 메일은 자동으로 발송된 알림 메일입니다. 답장하지 마세요.\n\n[프로젝트 관리 시스템 자동 알림]\n\nERP 구축 프로젝트의 다음 마일스톤 마감일이 7일 남았습니다.\n\n마일스톤: 1차 요구사항 정의 완료\n마감일: 2026년 4월 17일\n현재 완료율: 78%\n\n시스템에 접속하여 진행 상황을 업데이트해 주세요.\n\n[자동 발송 시스템]\nproject-system@company.kr"),
    (100, 5, 5,  7, "noreply@monitoring.company.kr", "[모니터링 알림] 서버 CPU 사용률 임계치 초과",
     "이 메일은 인프라 모니터링 시스템에서 자동 발송되었습니다.\n\n[경고] 서버 CPU 사용률 임계치 초과\n\n발생 시각: 2026-05-05 07:00:00\n대상 서버: web-prod-01 (10.10.1.101)\n현재 CPU: 92% (임계치: 85%)\n지속 시간: 15분\n\n확인 후 조치 바랍니다.\n\n모니터링 대시보드: http://monitoring.company.kr\n\n본 메일은 자동 발송입니다. 회신하지 마세요."),
]

for num, month, day, hour, sender_email, subject, body in auto_mails:
    raw = f"""From: System <{sender_email}>
To: {RECIPIENT[0]} <{RECIPIENT[1]}>
Subject: {subject}
Date: {make_date(month, day, hour)}
Message-ID: <mail{num:03d}@company.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
X-Auto-Response-Suppress: All
Precedence: bulk

{body}"""
    write_eml(f"mail_{num:03d}.eml", raw)

# ── mail_101: 동일 Message-ID (mail_001과 동일) ──────────────────────────
raw_101 = f"""From: 김민준 <minjun.kim@samsung.com>
To: {RECIPIENT[0]} <{RECIPIENT[1]}>
Subject: [재발송] ERP 구축 프로젝트 요구사항 검토 요청
Date: {make_date(3, 2, 10)}
Message-ID: <mail001@company.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

이전에 발송된 메일의 재발송입니다.

ERP 구축 프로젝트의 요구사항 분석 결과를 검토해 주시기 바랍니다.
(mail_001과 동일한 Message-ID입니다 - 중복 메일 테스트용)

감사합니다."""
write_eml("mail_101.eml", raw_101)

# ── mail_102: 빈 본문 ────────────────────────────────────────────────────
raw_102 = f"""From: 박지훈 <jihoon.park@company.kr>
To: {RECIPIENT[0]} <{RECIPIENT[1]}>
Subject: 빈 본문 테스트 메일
Date: {make_date(4, 1, 11)}
Message-ID: <mail102@company.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

"""
write_eml("mail_102.eml", raw_102)

# ── mail_103: 매우 긴 본문 (5000자 이상) ────────────────────────────────
long_body = "데이터 분석 플랫폼 구축을 위한 상세 기술 요건 명세서입니다.\n\n"
sections = [
    ("1. 개요", "데이터 분석 플랫폼은 전사 데이터를 통합하여 인사이트를 도출하는 핵심 시스템입니다. 본 플랫폼은 ERP, MES, CRM, 물류 시스템 등 다양한 소스 시스템의 데이터를 실시간 및 배치 방식으로 수집하고 분석합니다."),
    ("2. 아키텍처 요건", "데이터 레이크 아키텍처를 채택하여 정형/비정형 데이터를 모두 수용합니다. AWS S3를 원시 데이터 저장소로 사용하고 Snowflake를 데이터 웨어하우스로 구성합니다. Apache Airflow를 사용하여 ETL 파이프라인을 오케스트레이션합니다. Apache Spark를 활용하여 대용량 데이터 처리를 수행합니다. 실시간 처리를 위해 Apache Kafka를 도입합니다."),
    ("3. 데이터 수집 요건", "소스 시스템: ERP (SAP), MES (자체 개발), CRM (Salesforce), 물류 시스템, 품질 시스템\n수집 방식: CDC (Change Data Capture), API 연동, FTP 파일 전송, DB 직접 연동\n수집 주기: 실시간 (Kafka), 1시간 배치, 일간 배치, 월간 배치\n데이터 형식: JSON, CSV, XML, Parquet, ORC"),
    ("4. 데이터 변환 요건", "데이터 정제: 결측값 처리, 이상값 탐지, 데이터 타입 변환\n데이터 통합: 마스터 데이터 기준 통합, 조인 키 표준화\n데이터 품질: Great Expectations 기반 품질 검증 자동화\n비즈니스 로직: KPI 계산식 구현, 집계 테이블 생성"),
    ("5. 데이터 시각화 요건", "BI 도구: Tableau (경영진), Power BI (팀별 자율 분석)\n실시간 대시보드: Grafana (인프라 모니터링)\n리포팅: 정기 자동 리포트 이메일 발송, PDF 출력\n사용자 정의: 드래그앤드롭 방식 대시보드 구성"),
    ("6. 보안 요건", "데이터 접근 제어: 역할 기반 접근 제어 (RBAC)\n개인정보 보호: 마스킹, 비식별화 처리\n암호화: 저장 데이터 및 전송 데이터 암호화\n감사 로그: 모든 데이터 접근 이력 기록\n보안 인증: ISO 27001, ISMS-P 준수"),
    ("7. 성능 요건", "배치 처리: 야간 배치 4시간 이내 완료\n실시간 처리: 99% 메시지 1초 이내 처리\n대시보드 조회: 95% 이상 3초 이내 응답\n동시 사용자: 200명 동시 접속 지원\n데이터 보존: 원시 데이터 7년, 집계 데이터 10년"),
    ("8. 운영 요건", "모니터링: 24/7 파이프라인 상태 모니터링\n알림: 이상 탐지 시 즉시 알림 (이메일, Slack)\n백업: 일간 백업, 3 copies 유지\n재해 복구: RTO 4시간, RPO 1시간\n유지보수: 야간 및 주말 점검 윈도우"),
    ("9. 구현 일정", "1단계 (2026.05~07): 인프라 구성, ETL 파이프라인 개발\n2단계 (2026.08~09): BI 도구 구축, 핵심 대시보드 개발\n3단계 (2026.10~11): 고급 분석 기능, AI/ML 모델 연동\n4단계 (2026.12): 안정화 및 운영 전환"),
    ("10. 예산 계획", "인프라 구축: 2억 5천만원\nBI 도구 라이선스: 4,200만원/년\nETL 개발: 1억 2천만원\nBI 개발: 8,000만원\n교육 및 변화관리: 3,000만원\n총 구축 비용: 약 5억원\n연간 운영 비용: 약 1억 5천만원"),
]
for title, content in sections:
    long_body += f"\n{'='*60}\n{title}\n{'='*60}\n{content}\n"
    long_body += "\n상세 설명:\n"
    for i in range(1, 8):
        long_body += f"  {i}. 세부 항목 {i}: 이 항목에 대한 상세한 기술 요건 및 구현 방안을 기술합니다. 관련 기술 스택과 도구를 명시하고 성능 기준을 정의합니다.\n"

raw_103 = f"""From: 신예린 <yerin.shin@company.kr>
To: {RECIPIENT[0]} <{RECIPIENT[1]}>
Subject: 데이터 분석 플랫폼 상세 기술 요건 명세서 (전문)
Date: {make_date(5, 1, 10)}
Message-ID: <mail103@company.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

{long_body}
"""
write_eml("mail_103.eml", raw_103)

# ── mail_104: HTML 메일 ──────────────────────────────────────────────────
raw_104 = f"""From: 강태양 <taeyang.kang@hyundai.com>
To: {RECIPIENT[0]} <{RECIPIENT[1]}>
Subject: 보안 인프라 개선 프로젝트 현황 보고
Date: {make_date(5, 8, 11)}
Message-ID: <mail104@company.com>
MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif;">
<h2 style="color: #2c3e50;">보안 인프라 개선 프로젝트 현황 보고</h2>
<p>안녕하세요. 강태양 보안팀장입니다.</p>
<p>보안 인프라 개선 프로젝트 현황을 HTML 형식으로 보고드립니다.</p>
<h3 style="color: #2980b9;">진행 현황</h3>
<table border="1" style="border-collapse: collapse; width: 100%;">
  <tr style="background-color: #3498db; color: white;">
    <th>구분</th><th>목표</th><th>완료</th><th>진행률</th>
  </tr>
  <tr><td>방화벽 정책 개선</td><td>100%</td><td>85%</td><td style="color: orange;">85%</td></tr>
  <tr><td>SSL 인증서 갱신</td><td>100%</td><td>100%</td><td style="color: green;">완료</td></tr>
  <tr><td>패스워드 정책 강화</td><td>100%</td><td>60%</td><td style="color: orange;">60%</td></tr>
  <tr><td>제로트러스트 PoC</td><td>100%</td><td>50%</td><td style="color: red;">진행 중</td></tr>
</table>
<h3 style="color: #e74c3c;">주요 이슈</h3>
<ul>
  <li>일부 레거시 시스템 제로트러스트 적용 불가 → 대안 검토 중</li>
  <li>망분리 솔루션 도입 일정 2주 지연</li>
</ul>
<p style="color: #7f8c8d;">본 메일은 HTML 형식으로 발송됩니다. 보안 인프라 개선 프로젝트 관련 문의는 보안팀으로 연락 주세요.</p>
</body>
</html>
"""
write_eml("mail_104.eml", raw_104)

# ── mail_105: multipart/alternative ──────────────────────────────────────
raw_105 = f"""From: 윤하늘 <haneul.yoon@naver.com>
To: {RECIPIENT[0]} <{RECIPIENT[1]}>
Subject: 그룹웨어 개선 배포 완료 안내
Date: {make_date(5, 15, 10)}
Message-ID: <mail105@company.com>
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="alt_boundary_105"

--alt_boundary_105
Content-Type: text/plain; charset=UTF-8

그룹웨어 개선 버전 배포가 완료되었습니다.

주요 개선 사항:
- 이메일 로딩 속도 70% 향상
- 모바일 앱 UI 개선
- 화상회의 Webex 연동
- 캘린더 공유 기능 추가

접속 URL: https://groupware.company.kr
문의: IT 헬프데스크 (내선 9999)

--alt_boundary_105
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif;">
<h2 style="color: #27ae60;">그룹웨어 개선 버전 배포 완료</h2>
<p>그룹웨어 개선 버전 배포가 완료되었습니다.</p>
<h3>주요 개선 사항</h3>
<ul>
  <li>✅ 이메일 로딩 속도 70% 향상</li>
  <li>✅ 모바일 앱 UI 개선</li>
  <li>✅ 화상회의 Webex 연동</li>
  <li>✅ 캘린더 공유 기능 추가</li>
</ul>
<p><a href="https://groupware.company.kr" style="color: #3498db;">그룹웨어 접속하기</a></p>
<p>문의: IT 헬프데스크 (내선 9999)</p>
</body>
</html>

--alt_boundary_105--
"""
write_eml("mail_105.eml", raw_105)

# ── mail_106: UTF-8 Base64 인코딩 Subject ────────────────────────────────
import base64 as b64
subj_text = "클라우드 마이그레이션 최종 완료 보고"
encoded_subj = b64.b64encode(subj_text.encode("utf-8")).decode("ascii")
raw_106 = f"""From: 임재원 <jaewon.im@samsung.com>
To: {RECIPIENT[0]} <{RECIPIENT[1]}>
Subject: =?UTF-8?B?{encoded_subj}?=
Date: {make_date(6, 10, 10)}
Message-ID: <mail106@company.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

클라우드 마이그레이션 프로젝트가 최종 완료되었습니다.

완료 내역:
- 전체 서버 47대 AWS 마이그레이션 완료
- 온프레미스 서버 단계적 폐기 진행 중
- 연간 인프라 비용 1억 5천만원 절감 확인
- 가용성 99.99% 달성

프로젝트 결과 보고서는 별도로 공유드리겠습니다.

감사합니다.
임재원 드림
"""
write_eml("mail_106.eml", raw_106)

# ── mail_107: 잘못된 프로젝트명 ──────────────────────────────────────────
raw_107 = f"""From: 배수진 <sujin.bae@hyundai.com>
To: {RECIPIENT[0]} <{RECIPIENT[1]}>
Subject: Alpha Project 관련 협조 요청
Date: {make_date(4, 20, 11)}
Message-ID: <mail107@company.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

안녕하세요.

Alpha Project 관련하여 협조 요청드립니다.

Alpha Project는 당사 신제품 개발 프로젝트로, 현재 시스템 연동이 필요한 상황입니다.

요청 사항:
1. Alpha Project 데이터 연동 API 제공
2. 테스트 환경 계정 발급
3. 기술 지원 담당자 지정

알파 프로젝트는 내부 비공개 프로젝트이오니 기밀 유지 부탁드립니다.

감사합니다.
배수진 드림
"""
write_eml("mail_107.eml", raw_107)

# ── mail_108: 프로젝트와 무관한 개인 메일 ───────────────────────────────
raw_108 = f"""From: 조민서 <minseo.jo@company.kr>
To: {RECIPIENT[0]} <{RECIPIENT[1]}>
Subject: 이번 주말 등산 모임 안내
Date: {make_date(5, 21, 12)}
Message-ID: <mail108@company.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

안녕하세요 여러분!

이번 주말 팀 등산 모임 안내드립니다.

일시: 5월 24일(일) 오전 8시
장소: 북한산 국립공원 (북악 탐방지원센터 집결)
코스: 북악 → 보국문 → 대남문 (약 5시간 소요)
준비물: 등산화, 간식, 물, 우비

참가 여부 이번 주 금요일까지 알려 주세요.
총무 조민서가 도시락 준비할 예정입니다.

많은 참여 바랍니다~
감사합니다!
조민서 드림
"""
write_eml("mail_108.eml", raw_108)

# ── attachments/ 실제 파일 생성 ──────────────────────────────────────────
att_files = {
    "report.pdf": PDF_DUMMY + b"\n% Sample report content for testing\n",
    "budget.xlsx": XLSX_DUMMY + b"\x00" * 100,
    "quotation.docx": DOCX_DUMMY + b"\x00" * 100,
    "image.png": PNG_DUMMY,
    "specification.pdf": PDF_DUMMY + b"\n% Specification document\n" + b"x" * 500,
}

for fname, data in att_files.items():
    fpath = os.path.join(ATT_DIR, fname)
    with open(fpath, "wb") as f:
        f.write(data)

print("=" * 60)
print("파일 생성 완료!")
print("=" * 60)

# 생성된 EML 목록 확인
eml_files = sorted(os.listdir(EML_DIR))
print(f"\nEML 파일 수: {len(eml_files)}")
for f in eml_files:
    fpath = os.path.join(EML_DIR, f)
    size = os.path.getsize(fpath)
    print(f"  {f}: {size} bytes")

att_files_list = sorted(os.listdir(ATT_DIR))
print(f"\n첨부파일 수: {len(att_files_list)}")
for f in att_files_list:
    fpath = os.path.join(ATT_DIR, f)
    size = os.path.getsize(fpath)
    print(f"  {f}: {size} bytes")
