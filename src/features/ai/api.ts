import { invokeCommand } from '../../shared/lib/tauri';
import type { AiResult, AnalysisType } from './types';

export const aiApi = {
  emailAnalyze: (emailId: number, analysisType: AnalysisType) =>
    invokeCommand<AiResult>('email_analyze', {
      email_id: emailId,
      analysis_type: analysisType,
    }),

  emailListResults: (emailId: number) =>
    invokeCommand<AiResult[]>('email_list_ai_results', { email_id: emailId }),
};
