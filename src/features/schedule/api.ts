import { invokeCommand } from '../../shared/lib/tauri';
import type { Schedule, CreateScheduleRequest, UpdateScheduleRequest } from './types';

export const scheduleApi = {
  create: (req: CreateScheduleRequest) =>
    invokeCommand<Schedule>('schedule_create', { req }),

  list: () =>
    invokeCommand<Schedule[]>('schedule_list'),

  get: (id: number) =>
    invokeCommand<Schedule | null>('schedule_get', { id }),

  update: (id: number, req: UpdateScheduleRequest) =>
    invokeCommand<Schedule>('schedule_update', { id, req }),

  delete: (id: number) =>
    invokeCommand<boolean>('schedule_delete', { id }),
};
