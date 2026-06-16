import { invokeCommand } from '../../shared/lib/tauri';
import type { Task, CreateTaskRequest, UpdateTaskRequest } from './types';

export const taskApi = {
  create: (req: CreateTaskRequest) =>
    invokeCommand<Task>('task_create', { req }),

  list: (projectId: number) =>
    invokeCommand<Task[]>('task_list', { projectId }),

  get: (id: number) =>
    invokeCommand<Task | null>('task_get', { id }),

  update: (id: number, req: UpdateTaskRequest) =>
    invokeCommand<Task>('task_update', { id, req }),

  delete: (id: number) =>
    invokeCommand<boolean>('task_delete', { id }),

  listAll: () =>
    invokeCommand<Task[]>('task_list_all'),
};
