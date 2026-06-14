use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Schedule {
    pub id: i64,
    pub project_id: Option<i64>,
    pub title: String,
    pub description: Option<String>,
    pub scheduled_at: String,
    pub duration_minutes: Option<i32>,
    pub is_recurring: bool,
    pub recurrence_rule: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Debug, Deserialize)]
pub struct CreateScheduleRequest {
    pub project_id: Option<i64>,
    pub title: String,
    pub description: Option<String>,
    pub scheduled_at: String,
    pub duration_minutes: Option<i32>,
    pub is_recurring: Option<bool>,
    pub recurrence_rule: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct UpdateScheduleRequest {
    pub project_id: Option<i64>,
    pub title: String,
    pub description: Option<String>,
    pub scheduled_at: String,
    pub duration_minutes: Option<i32>,
    pub is_recurring: bool,
    pub recurrence_rule: Option<String>,
}
