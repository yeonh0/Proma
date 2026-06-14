import type { Status, Priority } from '../../shared/types';

export type { Status, Priority };

export interface Project {
  id: number;
  parent_id: number | null;
  title: string;
  description: string | null;
  status: Status;
  priority: Priority;
  start_date: string | null;
  due_date: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectRequest {
  parent_id?: number | null;
  title: string;
  description?: string | null;
  status?: Status;
  priority?: Priority;
  start_date?: string | null;
  due_date?: string | null;
}

export interface UpdateProjectRequest {
  parent_id: number | null;
  title: string;
  description: string | null;
  status: Status;
  priority: Priority;
  start_date: string | null;
  due_date: string | null;
  completed_at: string | null;
}
