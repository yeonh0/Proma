import { invokeCommand } from '../../shared/lib/tauri';
import type { AppSettings } from './types';

export const settingsApi = {
  get: (key: string) =>
    invokeCommand<string | null>('settings_get', { key }),

  set: (key: string, value: string) =>
    invokeCommand<void>('settings_set', { key, value }),

  getAll: () =>
    invokeCommand<AppSettings>('settings_get_all'),
};
