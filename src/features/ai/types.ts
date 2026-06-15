export interface AiResult {
  id: number;
  source_type: string;
  source_id: number;
  result_type: 'summary' | 'classification' | 'draft_reply' | 'keywords' | 'action_items' | 'project_candidates';
  model_name: string;
  prompt: string | null;
  result: string;
  is_applied: boolean;
  created_at: string;
}

export type AnalysisType = 'summary' | 'classification' | 'draft_reply';
