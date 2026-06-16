import { useEffect, useState } from 'react';
import { settingsApi } from '../features/settings';
import type { AiProvider } from '../features/settings';

export default function SettingsPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const [aiProvider, setAiProvider] = useState<AiProvider>('ollama');
  const [ollamaBaseUrl, setOllamaBaseUrl] = useState('http://localhost:11434');
  const [ollamaModel, setOllamaModel] = useState('llama3');
  const [internalApiUrl, setInternalApiUrl] = useState('');
  const [internalApiToken, setInternalApiToken] = useState('');
  const [internalWorkspaceId, setInternalWorkspaceId] = useState('');

  useEffect(() => {
    settingsApi.getAll()
      .then((s) => {
        setAiProvider((s.ai_provider as AiProvider) ?? 'ollama');
        setOllamaBaseUrl(s.ollama_base_url);
        setOllamaModel(s.ollama_model);
        setInternalApiUrl(s.internal_api_url);
        setInternalApiToken(s.internal_api_token);
        setInternalWorkspaceId(s.internal_workspace_id);
      })
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess(false);

    try {
      await Promise.all([
        settingsApi.set('ai_provider', aiProvider),
        settingsApi.set('ollama_base_url', ollamaBaseUrl.trim()),
        settingsApi.set('ollama_model', ollamaModel.trim()),
        settingsApi.set('internal_api_url', internalApiUrl.trim()),
        settingsApi.set('internal_api_token', internalApiToken.trim()),
        settingsApi.set('internal_workspace_id', internalWorkspaceId.trim()),
      ]);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (e) {
      setError(String(e));
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="page">
        <p className="state-message">불러오는 중…</p>
      </div>
    );
  }

  return (
    <div className="page">
      <h2 className="page-title">설정</h2>

      <form className="settings-form" onSubmit={handleSave}>
        {error && <p className="form-error">{error}</p>}
        {success && <p className="form-success">설정이 저장되었습니다.</p>}

        <section className="settings-section">
          <h3 className="settings-section-title">AI 설정</h3>

          <label className="form-label">
            AI 제공자
            <select
              className="form-input"
              value={aiProvider}
              onChange={(e) => setAiProvider(e.target.value as AiProvider)}
            >
              <option value="ollama">Ollama (로컬)</option>
              <option value="internal">내부 AI 서버</option>
            </select>
          </label>

          {aiProvider === 'ollama' && (
            <>
              <label className="form-label">
                Ollama 서버 URL
                <input
                  className="form-input"
                  type="text"
                  value={ollamaBaseUrl}
                  onChange={(e) => setOllamaBaseUrl(e.target.value)}
                  placeholder="http://localhost:11434"
                />
              </label>
              <label className="form-label">
                모델명
                <input
                  className="form-input"
                  type="text"
                  value={ollamaModel}
                  onChange={(e) => setOllamaModel(e.target.value)}
                  placeholder="llama3"
                />
              </label>
            </>
          )}

          {aiProvider === 'internal' && (
            <>
              <label className="form-label">
                API URL
                <input
                  className="form-input"
                  type="text"
                  value={internalApiUrl}
                  onChange={(e) => setInternalApiUrl(e.target.value)}
                  placeholder="https://내부망주소/api/chat"
                />
              </label>
              <label className="form-label">
                인증 토큰
                <input
                  className="form-input"
                  type="password"
                  value={internalApiToken}
                  onChange={(e) => setInternalApiToken(e.target.value)}
                  placeholder="Bearer 토큰"
                  autoComplete="off"
                />
              </label>
              <label className="form-label">
                Workspace ID
                <input
                  className="form-input"
                  type="text"
                  value={internalWorkspaceId}
                  onChange={(e) => setInternalWorkspaceId(e.target.value)}
                  placeholder="workspace_id"
                />
              </label>
            </>
          )}
        </section>

        <div className="settings-actions">
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? '저장 중…' : '저장'}
          </button>
        </div>
      </form>
    </div>
  );
}
