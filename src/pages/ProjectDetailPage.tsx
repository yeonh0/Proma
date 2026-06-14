import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { projectApi } from '../features/project/api';
import ProjectFormModal from '../features/project/ProjectFormModal';
import TaskList from '../features/task/TaskList';
import type { Project } from '../features/project/types';
import type { Status } from '../features/project/types';

const STATUS_LABEL: Record<string, string> = {
  active: '진행 중', paused: '일시 중단', completed: '완료', archived: '보관',
};
const PRIORITY_LABEL: Record<string, string> = {
  high: '높음', medium: '보통', low: '낮음',
};
const STATUS_OPTIONS: { value: Status; label: string }[] = [
  { value: 'active', label: '진행 중' },
  { value: 'paused', label: '일시 중단' },
  { value: 'completed', label: '완료' },
  { value: 'archived', label: '보관' },
];

type Tab = 'overview' | 'tasks';

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const projectId = Number(id);

  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [tab, setTab] = useState<Tab>('overview');
  const [changingStatus, setChangingStatus] = useState(false);

  const load = () => {
    setLoading(true);
    projectApi.get(projectId)
      .then((p) => {
        if (!p) setError('프로젝트를 찾을 수 없습니다.');
        else setProject(p);
      })
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [projectId]);

  const handleDelete = async () => {
    if (!confirm(`"${project?.title}" 프로젝트를 삭제하시겠습니까?\n하위 Task도 모두 삭제됩니다.`)) return;
    setDeleting(true);
    try {
      await projectApi.delete(projectId);
      navigate('/projects');
    } catch (e) {
      alert(String(e));
      setDeleting(false);
    }
  };

  const handleStatusChange = async (newStatus: Status) => {
    if (!project || newStatus === project.status) return;
    setChangingStatus(true);
    try {
      const updated = await projectApi.update(projectId, {
        parent_id: project.parent_id,
        title: project.title,
        description: project.description,
        status: newStatus,
        priority: project.priority,
        start_date: project.start_date,
        due_date: project.due_date,
        completed_at: newStatus === 'completed'
          ? (project.completed_at ?? new Date().toISOString().slice(0, 10))
          : null,
      });
      setProject(updated);
    } catch (e) {
      alert(String(e));
    } finally {
      setChangingStatus(false);
    }
  };

  if (loading) return <div className="page"><p className="state-message">불러오는 중…</p></div>;
  if (error || !project) return <div className="page"><p className="state-message state-error">{error ?? '오류'}</p></div>;

  return (
    <div className="page">
      <div className="page-header">
        <button className="btn btn-secondary" onClick={() => navigate('/projects')}>← 목록</button>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-secondary" onClick={() => setShowEditModal(true)}>수정</button>
          <button className="btn btn-danger" onClick={handleDelete} disabled={deleting}>삭제</button>
        </div>
      </div>

      <div className="detail-card">
        <div className="detail-header">
          <h2 className="detail-title">{project.title}</h2>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <select
              className="form-input"
              style={{ padding: '4px 8px', fontSize: 12 }}
              value={project.status}
              onChange={(e) => handleStatusChange(e.target.value as Status)}
              disabled={changingStatus}
            >
              {STATUS_OPTIONS.map((o) => (
                <option key={o.value} value={o.value}>{o.label}</option>
              ))}
            </select>
            <span className={`badge badge-priority badge-priority--${project.priority}`}>
              {PRIORITY_LABEL[project.priority]}
            </span>
          </div>
        </div>

        {project.description && (
          <p className="detail-desc">{project.description}</p>
        )}

        <div className="detail-meta">
          {project.start_date && <span>시작: {project.start_date}</span>}
          {project.due_date && <span>마감: {project.due_date}</span>}
          {project.completed_at && <span>완료: {project.completed_at}</span>}
          <span>생성: {project.created_at.slice(0, 10)}</span>
        </div>
      </div>

      <div className="tabs">
        <button className={`tab-btn ${tab === 'overview' ? 'active' : ''}`} onClick={() => setTab('overview')}>
          개요
        </button>
        <button className={`tab-btn ${tab === 'tasks' ? 'active' : ''}`} onClick={() => setTab('tasks')}>
          Task
        </button>
      </div>

      {tab === 'overview' && (
        <div className="detail-card">
          <p style={{ fontSize: 13, color: '#888' }}>
            상태: {STATUS_LABEL[project.status]} · 우선순위: {PRIORITY_LABEL[project.priority]}
          </p>
          {!project.description && (
            <p className="empty-state-sub" style={{ marginTop: 8 }}>설명이 없습니다. 수정 버튼으로 추가하세요.</p>
          )}
        </div>
      )}

      {tab === 'tasks' && (
        <TaskList projectId={projectId} />
      )}

      {showEditModal && (
        <ProjectFormModal
          project={project}
          onClose={() => setShowEditModal(false)}
          onSaved={load}
        />
      )}
    </div>
  );
}
