import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { emailApi } from '../features/email/api';
import { projectApi } from '../features/project/api';
import type { EmailWithMeta } from '../features/email/types';
import type { Project } from '../features/project/types';

function formatDate(iso: string | null) {
  if (!iso) return '—';
  try {
    return new Date(iso).toLocaleString('ko-KR', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', hour12: false,
    });
  } catch {
    return iso;
  }
}

function formatSize(bytes: number | null) {
  if (bytes == null) return '';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

export default function EmailDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const emailId = Number(id);

  const [data, setData] = useState<EmailWithMeta | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [linkedProjects, setLinkedProjects] = useState<Project[]>([]);
  const [allProjects, setAllProjects] = useState<Project[]>([]);
  const [linkProjectId, setLinkProjectId] = useState('');

  const load = () => {
    setLoading(true);
    emailApi.get(emailId)
      .then((d) => {
        if (!d) { setError('이메일을 찾을 수 없습니다.'); return; }
        setData(d);
        return d.project_ids;
      })
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    projectApi.list().then(setAllProjects).catch(() => {});
  }, [emailId]);

  useEffect(() => {
    if (!data) return;
    const linked = allProjects.filter((p) => data.project_ids.includes(p.id));
    setLinkedProjects(linked);
  }, [data, allProjects]);

  const handleDelete = async () => {
    if (!confirm('이 이메일을 삭제하시겠습니까?')) return;
    setDeleting(true);
    try {
      await emailApi.delete(emailId);
      navigate('/emails');
    } catch (e) {
      alert(String(e));
      setDeleting(false);
    }
  };

  const handleLinkProject = async () => {
    if (!linkProjectId) return;
    try {
      await emailApi.linkProject(emailId, Number(linkProjectId));
      setLinkProjectId('');
      load();
    } catch (e) {
      alert(String(e));
    }
  };

  const handleUnlinkProject = async (projectId: number) => {
    try {
      await emailApi.unlinkProject(emailId, projectId);
      load();
    } catch (e) {
      alert(String(e));
    }
  };

  if (loading) return <div className="page"><p className="state-message">불러오는 중…</p></div>;
  if (error || !data) return <div className="page"><p className="state-message state-error">{error ?? '오류'}</p></div>;

  const { email, attachments, project_ids } = data;
  const unlinkableProjects = allProjects.filter((p) => !project_ids.includes(p.id));

  return (
    <div className="page">
      <div className="page-header">
        <button className="btn btn-secondary" onClick={() => navigate('/emails')}>← 목록</button>
        <button className="btn btn-danger" onClick={handleDelete} disabled={deleting}>삭제</button>
      </div>

      <div className="detail-card">
        <div className="email-detail-header">
          <h2 className="email-detail-subject">{email.subject ?? '(제목 없음)'}</h2>
        </div>
        <div className="email-meta-row">
          <span><strong>발신:</strong> {email.sender ?? '—'}</span>
          <span><strong>수신:</strong> {email.recipients ? JSON.parse(email.recipients).join(', ') : '—'}</span>
          {email.cc && <span><strong>참조:</strong> {JSON.parse(email.cc).join(', ')}</span>}
          <span><strong>날짜:</strong> {formatDate(email.sent_at)}</span>
        </div>

        <div className="email-body">
          {email.body_text ?? '(본문 없음)'}
        </div>

        {attachments.length > 0 && (
          <div className="email-attachments">
            <div className="email-attachments-title">첨부파일 ({attachments.length})</div>
            {attachments.map((att) => (
              <div key={att.id} className="email-attachment-item">
                <span>📎</span>
                <span>{att.filename}</span>
                {att.size_bytes != null && (
                  <span style={{ color: '#bbb' }}>{formatSize(att.size_bytes)}</span>
                )}
              </div>
            ))}
          </div>
        )}

        <div className="email-project-links">
          <div className="email-project-links-title">연결된 프로젝트</div>
          {linkedProjects.length === 0 && (
            <p style={{ fontSize: 12, color: '#bbb', marginBottom: 8 }}>연결된 프로젝트 없음</p>
          )}
          {linkedProjects.map((p) => (
            <div key={p.id} className="email-project-link-item">
              <span>{p.title}</span>
              <button
                className="email-project-unlink-btn"
                onClick={() => handleUnlinkProject(p.id)}
                title="연결 해제"
              >✕</button>
            </div>
          ))}
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <select
              className="form-input"
              style={{ flex: 1, padding: '6px 8px', fontSize: 12 }}
              value={linkProjectId}
              onChange={(e) => setLinkProjectId(e.target.value)}
            >
              <option value="">프로젝트 선택…</option>
              {unlinkableProjects.map((p) => (
                <option key={p.id} value={String(p.id)}>{p.title}</option>
              ))}
            </select>
            <button
              className="btn btn-secondary"
              style={{ fontSize: 12, padding: '6px 12px' }}
              onClick={handleLinkProject}
              disabled={!linkProjectId}
            >연결</button>
          </div>
        </div>
      </div>
    </div>
  );
}
