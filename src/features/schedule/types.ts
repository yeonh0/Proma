export interface Schedule {
  id: number;
  project_id: number | null;
  title: string;
  description: string | null;
  scheduled_at: string;
  duration_minutes: number | null;
  is_recurring: boolean;
  recurrence_rule: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateScheduleRequest {
  project_id?: number | null;
  title: string;
  description?: string | null;
  scheduled_at: string;
  duration_minutes?: number | null;
  is_recurring?: boolean;
  recurrence_rule?: string | null;
}

export interface UpdateScheduleRequest {
  project_id: number | null;
  title: string;
  description: string | null;
  scheduled_at: string;
  duration_minutes: number | null;
  is_recurring: boolean;
  recurrence_rule: string | null;
}
