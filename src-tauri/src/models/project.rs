use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Project {
    pub id: i64,
    pub parent_id: Option<i64>,
    pub title: String,
    pub description: Option<String>,
    pub status: String,
    pub priority: String,
    pub start_date: Option<String>,
    pub due_date: Option<String>,
    pub completed_at: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Debug, Deserialize)]
pub struct CreateProjectRequest {
    pub parent_id: Option<i64>,
    pub title: String,
    pub description: Option<String>,
    pub status: Option<String>,
    pub priority: Option<String>,
    pub start_date: Option<String>,
    pub due_date: Option<String>,
}
