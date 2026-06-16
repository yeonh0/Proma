import { useEffect, useState } from 'react';
import { settingsApi } from '../features/settings';
import type { AiProvider } from '../features/settings';
import { invokeCommand } from '../shared/lib/tauri';

export default function SettingsPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const [seeding, setSeeding] = useState(false);

  const handleSeedAutomotive = async () => {
    if (!confirm('자동차 시나리오 프로젝트 5개와 태스크 25개를 생성합니다.\n기존 데이터는 삭제되지 않습니다. 계속하시겠습니까?')) return;
    setSeeding(true);
    try {
      const result = await invokeCommand<{ projects: number; tasks: number }>('seed_automotive_data');
      alert(`생성 완료: 프로젝트 ${result.projects}개, 태스크 ${result.tasks}개`);
    } catch (e) {
      alert(`오류: ${String(e)}`);
    } finally {
      setSeeding(false);
    }
  };

  const [aiProvider, setAiProvider] = useState<AiProvider>('ollama');
  const [ollamaBaseUrl, setOllamaBaseUrl] = useState('http://localhost:11434');
  const [ollamaModel, setOllamaModel] = useState('llama3');
  const [internalApiUrl, setInternalApiUrl] = useState('');
  const [internalRawHeaders, setInternalRawHeaders] = useState('');
  const [internalWorkspaceId, setInternalWorkspaceId] = useState('');

  useEffect(() => {
    settingsApi.getAll()
      .then((s) => {
        setAiProvider((s.ai_provider as AiProvider) ?? 'ollama');
        setOllamaBaseUrl(s.ollama_base_url);
        setOllamaModel(s.ollama_model);
        setInternalApiUrl(s.internal_api_url);
        setInternalRawHeaders(s.internal_raw_headers);
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
        settingsApi.set('internal_raw_headers', internalRawHeaders),
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
                  placeholder="https://내부망주소/api/chat/search"
                />
              </label>
              <label className="form-label">
                Workspace ID
                <input
                  className="form-input"
                  type="text"
                  value={internalWorkspaceId}
                  onChange={(e) => setInternalWorkspaceId(e.target.value)}
                  placeholder="workspace_id 값"
                />
              </label>
              <label className="form-label">
                요청 헤더
                <textarea
                  className="form-input"
                  rows={10}
                  value={internalRawHeaders}
                  onChange={(e) => setInternalRawHeaders(e.target.value)}
                  placeholder={
                    'Cookie: session=abc123\nContent-Type: application/json\n\n또는 Python raw_headers 형식:\nCookie\nsession=abc123'
                  }
                  style={{ fontFamily: 'monospace', fontSize: '12px', resize: 'vertical' }}
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

      <section className="settings-section" style={{ marginTop: '24px' }}>
        <h3 className="settings-section-title">테스트 데이터</h3>
        <p style={{ fontSize: '13px', color: '#666', marginBottom: '12px' }}>
          자동차 회사 시나리오 프로젝트 5개 + 태스크 25개를 생성합니다.<br />
          (아반떼 CN7 / 쏘나타 DN8 / 투싼 NX4 / 팰리세이드 LX2 / 아이오닉5 NE)
        </p>
        <button className="btn btn-primary" onClick={handleSeedAutomotive} disabled={seeding}>
          {seeding ? '생성 중…' : '자동차 시나리오 데이터 불러오기'}
        </button>
      </section>
    </div>
  );
}
