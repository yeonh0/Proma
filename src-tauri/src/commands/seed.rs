use serde::Serialize;
use tauri::State;

use crate::models::{
    project::CreateProjectRequest,
    task::CreateTaskRequest,
};
use crate::repository::{project as project_repo, task as task_repo};
use crate::AppState;

#[derive(Serialize)]
pub struct SeedResult {
    pub projects: usize,
    pub tasks: usize,
}

struct ProjectSeed {
    title: &'static str,
    description: &'static str,
    priority: &'static str,
    tasks: &'static [(&'static str, &'static str)], // (title, status)
}

const AUTOMOTIVE_DATA: &[ProjectSeed] = &[
    ProjectSeed {
        title: "아반떼 CN7",
        description: "아반떼 CN7 페이스리프트 개발 프로젝트",
        priority: "high",
        tasks: &[
            ("1.6 GDi 엔진 내구성 검증", "in_progress"),
            ("DCT 변속기 진동 개선", "todo"),
            ("전방 충돌 방지 보조(FCA) 캘리브레이션", "todo"),
            ("실내 소음 저감 패키지 적용", "in_progress"),
            ("헤드램프 DRL 패턴 변경 승인", "done"),
        ],
    },
    ProjectSeed {
        title: "쏘나타 DN8",
        description: "쏘나타 DN8 연식 변경 및 하이브리드 라인업 확대",
        priority: "high",
        tasks: &[
            ("2.0 HEV 배터리 열관리 시스템 검토", "in_progress"),
            ("능동형 노이즈 컨트롤(ANC) 튜닝", "todo"),
            ("파노라믹 선루프 누수 재현 테스트", "in_progress"),
            ("12.3인치 클러스터 소프트웨어 업데이트", "todo"),
            ("리어 서스펜션 세팅 최종 승인", "done"),
        ],
    },
    ProjectSeed {
        title: "투싼 NX4",
        description: "투싼 NX4 오프로드 패키지 및 N Line 개발",
        priority: "medium",
        tasks: &[
            ("HTRAC AWD 제어로직 최적화", "in_progress"),
            ("하체 보호 스키드 플레이트 적용", "todo"),
            ("N Line 전용 서스펜션 세팅 확정", "todo"),
            ("오프로드 주행 모드 UI 검토", "todo"),
            ("견인 후크 강도 시험", "done"),
        ],
    },
    ProjectSeed {
        title: "팰리세이드 LX2",
        description: "팰리세이드 2026년형 개발 및 품질 개선",
        priority: "medium",
        tasks: &[
            ("3열 시트 접이 메커니즘 내구 시험", "in_progress"),
            ("3.5 T-GDi 엔진 오일 소비 원인 분석", "in_progress"),
            ("후측방 모니터(BVM) 화질 개선", "todo"),
            ("7인승 / 8인승 시트 배치 검토", "done"),
            ("루프랙 하중 기준 재정립", "todo"),
        ],
    },
    ProjectSeed {
        title: "아이오닉5 NE",
        description: "아이오닉5 배터리 2세대 및 V2L 확장 기능 개발",
        priority: "high",
        tasks: &[
            ("84kWh 배터리 팩 열폭주 시험", "in_progress"),
            ("800V 초급속 충전 안정성 검증", "in_progress"),
            ("V2L 출력 3.6kW → 5.0kW 업그레이드 검토", "todo"),
            ("원페달 드라이빙 응답성 튜닝", "todo"),
            ("리어 모터 소음 재현 및 원인 분석", "in_progress"),
        ],
    },
];

#[tauri::command]
pub fn seed_automotive_data(state: State<AppState>) -> Result<SeedResult, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    let conn = db.connection();

    let mut project_count = 0;
    let mut task_count = 0;

    for seed in AUTOMOTIVE_DATA {
        let project = project_repo::create(
            conn,
            &CreateProjectRequest {
                parent_id: None,
                title: seed.title.to_string(),
                description: Some(seed.description.to_string()),
                status: Some("active".to_string()),
                priority: Some(seed.priority.to_string()),
                start_date: None,
                due_date: None,
            },
        )
        .map_err(|e| e.to_string())?;

        project_count += 1;

        for (task_title, task_status) in seed.tasks {
            task_repo::create(
                conn,
                &CreateTaskRequest {
                    project_id: project.id,
                    title: task_title.to_string(),
                    description: None,
                    status: Some(task_status.to_string()),
                    priority: Some("medium".to_string()),
                    due_date: None,
                },
            )
            .map_err(|e| e.to_string())?;

            task_count += 1;
        }
    }

    Ok(SeedResult { projects: project_count, tasks: task_count })
}
