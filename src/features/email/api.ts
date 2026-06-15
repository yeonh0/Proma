import { invokeCommand } from '../../shared/lib/tauri';
import type { Email, EmailWithMeta, EmailProjectMapping } from './types';

export const emailApi = {
  import: (filePath: string) =>
    invokeCommand<Email>('email_import', { file_path: filePath }),

  list: () =>
    invokeCommand<Email[]>('email_list'),

  get: (id: number) =>
    invokeCommand<EmailWithMeta | null>('email_get', { id }),

  delete: (id: number) =>
    invokeCommand<boolean>('email_delete', { id }),

  linkProject: (emailId: number, projectId: number) =>
    invokeCommand<EmailProjectMapping>('email_link_project', { email_id: emailId, project_id: projectId }),

  unlinkProject: (emailId: number, projectId: number) =>
    invokeCommand<boolean>('email_unlink_project', { email_id: emailId, project_id: projectId }),

  listProjectIds: (emailId: number) =>
    invokeCommand<number[]>('email_list_project_ids', { email_id: emailId }),
};
