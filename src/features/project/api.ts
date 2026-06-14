import { invokeCommand } from '../../shared/lib/tauri';
import type { Project, CreateProjectRequest } from './types';

export const projectApi = {
  create: (req: CreateProjectRequest) =>
    invokeCommand<Project>('project_create', { req }),

  list: () =>
    invokeCommand<Project[]>('project_list'),
};
