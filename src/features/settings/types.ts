export interface AppSettings {
  ollama_base_url: string;
  ollama_model: string;
  app_language: string;
  email_storage_path: string;
  ai_provider: string;
  internal_api_url: string;
  internal_api_token: string;
  internal_workspace_id: string;
}

export type AiProvider = 'ollama' | 'internal';
