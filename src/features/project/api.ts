import { invokeCommand } from '../../shared/lib/tauri';
import type { Project, CreateProjectRequest, UpdateProjectRequest } from './types';

export const projectApi = {
  create: (req: CreateProjectRequest) =>
    invokeCommand<Project>('project_create', { req }),

  list: () =>
    invokeCommand<Project[]>('project_list'),

  get: (id: number) =>
    invokeCommand<Project | null>('project_get', { id }),

  update: (id: number, req: UpdateProjectRequest) =>
    invokeCommand<Project>('project_update', { id, req }),

  delete: (id: number) =>
    invokeCommand<boolean>('project_delete', { id }),
};
