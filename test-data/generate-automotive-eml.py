#!/usr/bin/env python3
"""
자동차 회사 시나리오 테스트 EML 생성기
- 프로젝트: 아반떼 CN7, 쏘나타 DN8, 투싼 NX4, 팰리세이드 LX2, 아이오닉5 NE
- 태스크 키워드를 이메일 본문에 자연스럽게 포함
- 한국 비즈니스 이메일 스타일 (인사말 + 본론 + 감사)
"""

import os
import random
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "eml", "automotive")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_DATE = datetime(2025, 3, 1, 9, 0, 0)

EMAILS = [
    # ── 아반떼 CN7 ────────────────────────────────────────────────────────
    {
        "project": "아반떼 CN7",
        "task": "1.6 GDi 엔진 내구성 검증",
        "subject": "[아반떼 CN7] 1.6 GDi 엔진 내구성 검증 일정 협의 요청",
        "sender_name": "박준혁",
        "sender_email": "junhyuk.park@hmmc.co.kr",
        "recipient_name": "김도현",
        "recipient_email": "dohyun.kim@hmmc.co.kr",
        "body": """안녕하세요, 김도현 님.

파워트레인 연구팀 박준혁입니다.

아반떼 CN7 페이스리프트 일정에 따라 1.6 GDi 엔진 내구성 검증 일정을 조율드리고자 메일 드립니다.

현재 시험 장비 예약 현황상 다음 달 둘째 주(4월 14일 ~ 4월 18일) 중 3일을 확보할 수 있으며, 해당 기간 내 150,000km 상당의 가속 내구 사이클을 완료하는 것을 목표로 하고 있습니다.

검증 항목은 아래와 같습니다.
- 오일 소비량 측정 (매 10,000km 인터벌)
- 실린더 헤드 온도 분포 모니터링
- 크랭크샤프트 베어링 마모 육안 점검

일정 확정을 위해 이번 주 금요일까지 회신 부탁드립니다.

감사합니다.
박준혁 드림""",
    },
    {
        "project": "아반떼 CN7",
        "task": "DCT 변속기 진동 개선",
        "subject": "[아반떼 CN7] DCT 변속기 진동 이슈 재현 결과 공유",
        "sender_name": "이서연",
        "sender_email": "seoyeon.lee@hmmc.co.kr",
        "recipient_name": "최민준",
        "recipient_email": "minjun.choi@hmmc.co.kr",
        "body": """안녕하세요, 최민준 님.

섀시 NVH 팀 이서연입니다.

지난주에 논의드렸던 아반떼 CN7 DCT 변속기 진동 이슈에 대한 재현 시험 결과를 공유드립니다.

시험 차량 3대를 대상으로 저속 크리프 구간(0~15 km/h)에서 진동 레벨을 측정한 결과, 2단 → 3단 변속 시 스티어링 컬럼에서 평균 2.4 mm/s² 수준의 진동이 확인되었습니다. 이는 목표값(1.8 mm/s²)을 약 33% 초과하는 수치입니다.

원인으로는 클러치 결합 타이밍과 댐퍼 스프링 강성 미스매치가 유력하며, 변속기 소프트웨어 매핑 수정과 함께 댐퍼 교체 검토가 필요합니다.

다음 주 중 대책 회의를 잡을 수 있을지 일정 공유 부탁드립니다.

감사합니다.
이서연 드림""",
    },
    {
        "project": "아반떼 CN7",
        "task": "실내 소음 저감 패키지 적용",
        "subject": "[아반떼 CN7] 실내 소음 저감 패키지 부품 공급 지연 안내",
        "sender_name": "오태양",
        "sender_email": "taeyang.oh@hmmc.co.kr",
        "recipient_name": "정유진",
        "recipient_email": "yujin.jung@hmmc.co.kr",
        "body": """안녕하세요, 정유진 님.

구매 관리팀 오태양입니다.

아반떼 CN7 실내 소음 저감 패키지 적용에 사용되는 후펜도르프 사의 흡음재(Part No. HF-7742)가 원자재 수급 이슈로 인해 당초 납기일인 3월 28일에서 4월 11일로 약 2주 지연될 예정임을 알려드립니다.

이로 인해 1차 차체 실링 작업 일정이 영향을 받을 수 있으며, 대안 부품 검토(국내 대체 흡음재 3종)를 품질 팀과 함께 진행 중입니다.

일정 조정 필요 여부 확인 후 이번 주 내로 회신드리겠습니다.

감사합니다.
오태양 드림""",
    },
    # ── 쏘나타 DN8 ────────────────────────────────────────────────────────
    {
        "project": "쏘나타 DN8",
        "task": "2.0 HEV 배터리 열관리 시스템 검토",
        "subject": "[쏘나타 DN8] 2.0 HEV 배터리 열관리 시스템 검토 요청",
        "sender_name": "한지수",
        "sender_email": "jisoo.han@hmmc.co.kr",
        "recipient_name": "윤서준",
        "recipient_email": "seojun.yoon@hmmc.co.kr",
        "body": """안녕하세요, 윤서준 님.

전동화 시스템 팀 한지수입니다.

쏘나타 DN8 하이브리드 라인업 확대와 관련하여 2.0 HEV 배터리 열관리 시스템 검토를 요청드립니다.

여름철 고온 환경(외기 35°C 이상) 조건에서 1시간 연속 주행 후 배터리 모듈 온도가 42°C를 초과하는 케이스가 확인되었으며, 이는 BMS 온도 경고 임계값(40°C)보다 높은 수준입니다.

냉각 회로 유량 증가 또는 냉각 핀 형상 변경 두 가지 방향으로 검토 부탁드리며, 각 방향별 비용 및 일정 영향도를 다음 주 화요일까지 공유해주시면 감사하겠습니다.

감사합니다.
한지수 드림""",
    },
    {
        "project": "쏘나타 DN8",
        "task": "파노라믹 선루프 누수 재현 테스트",
        "subject": "[쏘나타 DN8] 파노라믹 선루프 누수 재현 테스트 협조 요청",
        "sender_name": "강민서",
        "sender_email": "minseo.kang@hmmc.co.kr",
        "recipient_name": "임재원",
        "recipient_email": "jaewon.lim@hmmc.co.kr",
        "body": """안녕하세요, 임재원 님.

차체 개발 팀 강민서입니다.

쏘나타 DN8 고객 VOC 중 파노라믹 선루프 누수 관련 건수가 이번 분기 7건 접수되었습니다. 재현 시험을 통해 원인을 특정하고자 협조 요청드립니다.

재현 조건은 다음과 같습니다.
- 방수 챔버 내 강수량 200 mm/h, 30분 연속 살수
- 주행 속도 80 km/h 상당 바람 부하 적용
- 선루프 전후 이동 10회 반복 후 누수 여부 확인

시험 장비 예약 현황 확인 후 가능한 일정을 이번 주 내로 알려주시면 감사하겠습니다.

감사합니다.
강민서 드림""",
    },
    {
        "project": "쏘나타 DN8",
        "task": "능동형 노이즈 컨트롤(ANC) 튜닝",
        "subject": "[쏘나타 DN8] ANC 튜닝 결과 검토 및 양산 승인 요청",
        "sender_name": "송재현",
        "sender_email": "jaehyun.song@hmmc.co.kr",
        "recipient_name": "백수아",
        "recipient_email": "sua.baek@hmmc.co.kr",
        "body": """안녕하세요, 백수아 님.

음향 설계 팀 송재현입니다.

쏘나타 DN8 능동형 노이즈 컨트롤(ANC) 최종 튜닝 결과를 공유드리며 양산 승인을 요청드립니다.

3차 튜닝 결과, 100 Hz 이하 저주파 로드 노이즈를 기존 대비 평균 4.2 dB(A) 저감하는 데 성공하였습니다. 목표값(3.5 dB(A) 이상)을 충족하였으며, 음질 평가단(10명) 주관 평가에서도 '체감 향상' 응답률 90%를 기록하였습니다.

양산 적용 결정을 위해 이번 주 목요일 검토 회의를 요청드리며, 상세 데이터는 첨부 파일을 참고 부탁드립니다.

감사합니다.
송재현 드림""",
    },
    # ── 투싼 NX4 ─────────────────────────────────────────────────────────
    {
        "project": "투싼 NX4",
        "task": "HTRAC AWD 제어로직 최적화",
        "subject": "[투싼 NX4] HTRAC AWD 제어로직 최적화 진행 현황 공유",
        "sender_name": "김예린",
        "sender_email": "yerin.kim@hmmc.co.kr",
        "recipient_name": "노현우",
        "recipient_email": "hyunwoo.roh@hmmc.co.kr",
        "body": """안녕하세요, 노현우 님.

사륜구동 시스템 팀 김예린입니다.

투싼 NX4 N Line 오프로드 패키지 대응을 위한 HTRAC AWD 제어로직 최적화 작업 현황을 공유드립니다.

현재 2단계 중 1단계(저마찰 노면 토크 배분 맵 수정)가 완료되었으며, 눈길 및 진흙 노면 시험에서 전후륜 토크 배분 응답 시간이 기존 180ms에서 120ms로 개선되었음을 확인하였습니다.

2단계(고속 선회 시 후륜 잠금 로직 추가) 작업은 다음 달 초 착수 예정이며, 해당 작업을 위해 동역학 팀과의 협의가 필요합니다. 일정 조율 가능하신지 확인 부탁드립니다.

감사합니다.
김예린 드림""",
    },
    {
        "project": "투싼 NX4",
        "task": "하체 보호 스키드 플레이트 적용",
        "subject": "[투싼 NX4] 스키드 플레이트 신규 공급사 검토 요청",
        "sender_name": "홍성민",
        "sender_email": "sungmin.hong@hmmc.co.kr",
        "recipient_name": "조아름",
        "recipient_email": "areum.cho@hmmc.co.kr",
        "body": """안녕하세요, 조아름 님.

차체 설계 팀 홍성민입니다.

투싼 NX4 오프로드 패키지에 적용할 하체 보호 스키드 플레이트 신규 공급사 검토를 요청드립니다.

기존 1차 공급사의 단가가 당초 목표 대비 18% 높게 견적이 제출되어, 원가 목표 달성을 위해 대안 공급사 2곳(A사: 알루미늄 다이캐스팅, B사: 고강도 스틸 프레스)을 추가 검토하고자 합니다.

두 공급사 모두 3월 말까지 시제품 납품 예정이며, 4월 중 비교 시험(충격 강도, 중량, 장착 편의성)을 진행할 계획입니다.

검토 일정 및 평가 기준에 대한 의견 부탁드립니다.

감사합니다.
홍성민 드림""",
    },
    {
        "project": "투싼 NX4",
        "task": "N Line 전용 서스펜션 세팅 확정",
        "subject": "[투싼 NX4] N Line 서스펜션 최종 세팅값 확정 요청",
        "sender_name": "유다은",
        "sender_email": "daeun.yu@hmmc.co.kr",
        "recipient_name": "권태민",
        "recipient_email": "taemin.kwon@hmmc.co.kr",
        "body": """안녕하세요, 권태민 님.

샤시 설계 팀 유다은입니다.

투싼 NX4 N Line 전용 서스펜션 세팅 확정을 위해 최종 검토 결과를 공유드립니다.

3가지 세팅안(S1: 스포츠 바이어스, S2: 컴포트 바이어스, S3: 복합형) 중 지난 서킷 및 일반도로 통합 평가에서 S3 복합형이 승객 만족도와 핸들링 성능 양쪽에서 가장 높은 점수를 받았습니다.

S3 기준 댐퍼 감쇠력과 스프링 상수를 최종 확정하고 설계 변경 반영을 진행하고자 하니, 이번 주 금요일 오후 3시 이전까지 최종 승인 회신 부탁드립니다.

감사합니다.
유다은 드림""",
    },
    # ── 팰리세이드 LX2 ──────────────────────────────────────────────────
    {
        "project": "팰리세이드 LX2",
        "task": "3열 시트 접이 메커니즘 내구 시험",
        "subject": "[팰리세이드 LX2] 3열 시트 접이 메커니즘 내구 시험 결과 보고",
        "sender_name": "안지현",
        "sender_email": "jihyun.ahn@hmmc.co.kr",
        "recipient_name": "문성호",
        "recipient_email": "sungho.moon@hmmc.co.kr",
        "body": """안녕하세요, 문성호 님.

실내 부품 품질 팀 안지현입니다.

팰리세이드 LX2 3열 시트 접이 메커니즘 내구 시험 결과를 보고드립니다.

총 5,000회 반복 접이 시험 결과, 3,820회 시점에서 좌측 폴딩 래치(Part No. PS-3841-L)의 스프링 하중이 초기값 대비 22% 저하되는 현상이 확인되었습니다. 이는 목표 내구(5,000회 이상) 미달에 해당합니다.

원인 분석 결과 스프링 와이어 직경이 설계 도면(1.8mm) 대비 실제 납품품(1.65mm)과 차이가 있음이 확인되었으며, 공급사(현진스프링)에 즉각 시정 조치를 요청한 상태입니다.

수정 부품 납품 후 재시험 일정은 추후 공유드리겠습니다.

감사합니다.
안지현 드림""",
    },
    {
        "project": "팰리세이드 LX2",
        "task": "3.5 T-GDi 엔진 오일 소비 원인 분석",
        "subject": "[팰리세이드 LX2] 3.5 T-GDi 엔진 오일 소비 과다 원인 분석 협의",
        "sender_name": "최성훈",
        "sender_email": "sunghoon.choi@hmmc.co.kr",
        "recipient_name": "황지민",
        "recipient_email": "jimin.hwang@hmmc.co.kr",
        "body": """안녕하세요, 황지민 님.

엔진 품질 보증 팀 최성훈입니다.

팰리세이드 LX2에 탑재된 3.5 T-GDi 엔진의 오일 소비 과다 관련 고객 클레임이 최근 증가 추세에 있어 원인 분석 협의를 요청드립니다.

현재까지 접수된 사례(총 23건) 분석 결과, 오일 소비량이 1,000km당 평균 0.8L 수준으로 허용 기준(0.5L/1,000km)을 초과하는 것으로 집계되었습니다.

예상 원인으로는 피스톤 오일 링 마모 또는 밸브 스템 씰 열화가 유력하며, 이를 확인하기 위한 엔진 분해 시험을 다음 주부터 착수하려 합니다.

분해 일정 및 분석 범위 협의를 위해 이번 주 수요일 오전 미팅을 제안드립니다. 시간 확인 부탁드립니다.

감사합니다.
최성훈 드림""",
    },
    {
        "project": "팰리세이드 LX2",
        "task": "후측방 모니터(BVM) 화질 개선",
        "subject": "[팰리세이드 LX2] BVM 카메라 화질 개선 부품 적용 일정 확인",
        "sender_name": "이진우",
        "sender_email": "jinwoo.lee@hmmc.co.kr",
        "recipient_name": "서하은",
        "recipient_email": "haeun.seo@hmmc.co.kr",
        "body": """안녕하세요, 서하은 님.

전장 설계 팀 이진우입니다.

팰리세이드 LX2 후측방 모니터(BVM) 화질 개선을 위한 신규 카메라 모듈(SONY IMX323 → IMX415 교체) 적용 일정 확인을 요청드립니다.

1차 파일럿 차량 장착 테스트에서 야간 해상도가 기존 대비 40% 향상되었음을 확인하였으며, 양산 적용 의향서를 지난주에 공급사에 발송하였습니다.

양산 시작 예정일(7월 1일) 기준으로 역산 시 5월 말까지 금형 승인이 완료되어야 하므로, 금형 설계 일정 현황을 이번 주 내로 공유해주시면 감사하겠습니다.

감사합니다.
이진우 드림""",
    },
    # ── 아이오닉5 NE ─────────────────────────────────────────────────────
    {
        "project": "아이오닉5 NE",
        "task": "84kWh 배터리 팩 열폭주 시험",
        "subject": "[아이오닉5 NE] 84kWh 배터리 팩 열폭주 시험 일정 및 안전 절차 협의",
        "sender_name": "정다인",
        "sender_email": "dain.jung@hmmc.co.kr",
        "recipient_name": "박성재",
        "recipient_email": "sungjae.park@hmmc.co.kr",
        "body": """안녕하세요, 박성재 님.

배터리 안전성 시험 팀 정다인입니다.

아이오닉5 NE 2세대 배터리 팩(84kWh) 열폭주 시험 일정 및 안전 절차 협의를 요청드립니다.

국내 법규(KMVSS 102조) 개정에 따라 올해부터 열폭주 전파 방지 성능 검증이 의무화되었으며, 당사 제품도 7월 이전 시험 완료가 필요합니다.

시험은 단일 셀 직접 가열 방식으로 진행될 예정이며, 외부 전문 기관(KCL)과 협력하여 5월 중 진행하는 방향으로 검토 중입니다. 시험 전 내부 안전 검토 위원회 승인이 필요하므로 관련 문서 준비를 함께 부탁드립니다.

이번 주 내로 킥오프 미팅 일정 잡아주시면 감사하겠습니다.

감사합니다.
정다인 드림""",
    },
    {
        "project": "아이오닉5 NE",
        "task": "800V 초급속 충전 안정성 검증",
        "subject": "[아이오닉5 NE] 800V 초급속 충전 안정성 검증 현장 시험 결과",
        "sender_name": "신호준",
        "sender_email": "hojun.shin@hmmc.co.kr",
        "recipient_name": "이채원",
        "recipient_email": "chaewon.lee@hmmc.co.kr",
        "body": """안녕하세요, 이채원 님.

충전 인프라 기술 팀 신호준입니다.

아이오닉5 NE 800V 초급속 충전 안정성 현장 시험(충전소 3개소, 총 120회 충전) 결과를 공유드립니다.

주요 결과는 다음과 같습니다.
- 평균 충전 속도: 232 kW (목표: 220 kW 이상 → 달성)
- 10% → 80% 충전 소요 시간 평균: 17분 22초
- 이상 종료 건수: 3건 (원인: 충전기 측 통신 오류 2건, 차량 측 BMS 오류 1건)

차량 측 BMS 오류 1건에 대해서는 로그 분석을 통해 원인 파악 중이며, 다음 주 중 결과 공유드리겠습니다.

전반적으로 목표 성능을 달성하였으나 이상 종료 건에 대한 후속 조치가 필요합니다. 검토 후 의견 부탁드립니다.

감사합니다.
신호준 드림""",
    },
    {
        "project": "아이오닉5 NE",
        "task": "V2L 출력 3.6kW → 5.0kW 업그레이드 검토",
        "subject": "[아이오닉5 NE] V2L 출력 업그레이드(5.0kW) 타당성 검토 결과 공유",
        "sender_name": "오지민",
        "sender_email": "jimin.oh@hmmc.co.kr",
        "recipient_name": "김태훈",
        "recipient_email": "taehoon.kim@hmmc.co.kr",
        "body": """안녕하세요, 김태훈 님.

전동화 아키텍처 팀 오지민입니다.

아이오닉5 NE V2L 출력 5.0kW 업그레이드 타당성 검토 결과를 공유드립니다.

현재 3.6kW에서 5.0kW로 출력을 높이기 위해서는 온보드 충전기(OBC) 내부 MOSFET 교체 및 열 방출 구조 보강이 필요하며, 이에 따른 원가 증가분은 차량 1대당 약 4.2만원으로 추산됩니다.

법규 측면에서는 국내 전기차 V2L 관련 규정상 5.0kW는 허용 범위 내이며, 유럽 수출 대응에도 긍정적입니다.

원가 증가와 마케팅 가치를 종합 고려 시 업그레이드 추진이 유리하다고 판단되나, 최종 결정은 상품 기획팀과 협의가 필요합니다. 관련 회의 일정 조율 부탁드립니다.

감사합니다.
오지민 드림""",
    },
    {
        "project": "아이오닉5 NE",
        "task": "리어 모터 소음 재현 및 원인 분석",
        "subject": "[아이오닉5 NE] 리어 모터 소음 재현 시험 협조 요청",
        "sender_name": "채민지",
        "sender_email": "minji.chae@hmmc.co.kr",
        "recipient_name": "한동현",
        "recipient_email": "donghyun.han@hmmc.co.kr",
        "body": """안녕하세요, 한동현 님.

전동 파워트레인 NVH 팀 채민지입니다.

아이오닉5 NE 리어 모터에서 발생하는 고주파 소음(약 3.2 kHz 대역) 재현 시험에 협조 요청드립니다.

해당 소음은 회생 제동 구간(30~60 km/h, 감속도 0.1~0.2g)에서 주로 발생하며, 기존 FR 모터에서는 확인되지 않는 RR 모터 특이 현상으로 파악되고 있습니다.

재현을 위해 섀시 다이나모 설비 사용이 필요하며, 다음 주 화요일 또는 수요일 오전 중 2시간 슬롯 확보가 가능한지 확인 부탁드립니다.

원인 분석에는 모터 제어 SW 팀도 함께 참여가 필요하므로 일정 공유 시 함께 안내드리겠습니다.

감사합니다.
채민지 드림""",
    },
]


def make_eml(idx, email_data, base_date):
    offset_days = idx * 2
    offset_hours = random.randint(8, 17)
    send_time = base_date + timedelta(days=offset_days, hours=offset_hours)

    msg = MIMEText(email_data["body"], "plain", "utf-8")
    msg["Subject"] = email_data["subject"]
    msg["From"] = f"{email_data['sender_name']} <{email_data['sender_email']}>"
    msg["To"] = f"{email_data['recipient_name']} <{email_data['recipient_email']}>"
    msg["Date"] = formatdate(send_time.timestamp(), localtime=True)
    msg["Message-ID"] = make_msgid(domain="hmmc.co.kr")
    msg["X-Project"] = email_data["project"]
    msg["X-Task"] = email_data["task"]

    filename = f"{idx+1:02d}_{email_data['project'].replace(' ', '_')}_{email_data['task'][:10].replace(' ', '_')}.eml"
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(msg.as_string())
    return filename


if __name__ == "__main__":
    random.seed(42)
    for i, email_data in enumerate(EMAILS):
        fname = make_eml(i, email_data, BASE_DATE)
        print(f"생성: {fname}")
    print(f"\n총 {len(EMAILS)}개 EML 생성 완료 → {OUTPUT_DIR}")
