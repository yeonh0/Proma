import { invokeCommand } from '../../shared/lib/tauri';
import type { Email, EmailWithMeta, EmailProjectMapping } from './types';

export const emailApi = {
  import: (filePath: string) =>
    invokeCommand<Email>('email_import', { filePath }),

  list: () =>
    invokeCommand<Email[]>('email_list'),

  get: (id: number) =>
    invokeCommand<EmailWithMeta | null>('email_get', { id }),

  delete: (id: number) =>
    invokeCommand<boolean>('email_delete', { id }),

  deleteAll: () =>
    invokeCommand<number>('email_delete_all'),

  linkProject: (emailId: number, projectId: number) =>
    invokeCommand<EmailProjectMapping>('email_link_project', { emailId, projectId }),

  unlinkProject: (emailId: number, projectId: number) =>
    invokeCommand<boolean>('email_unlink_project', { emailId, projectId }),

  listProjectIds: (emailId: number) =>
    invokeCommand<number[]>('email_list_project_ids', { emailId }),
};
