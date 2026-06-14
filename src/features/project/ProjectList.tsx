import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { projectApi } from './api';
import type { Project } from './types';

const STATUS_LABEL: Record<string, string> = {
  active: '진행 중',
  paused: '일시 중단',
  completed: '완료',
  archived: '보관',
};

const PRIORITY_LABEL: Record<string, string> = {
  high: '높음',
  medium: '보통',
  low: '낮음',
};

export default function ProjectList({ onRefreshRef }: { onRefreshRef?: (fn: () => void) => void }) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const load = () => {
    setLoading(true);
    setError(null);
    projectApi.list()
      .then(setProjects)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    onRefreshRef?.(load);
  }, []);

  if (loading) return <p className="state-message">불러오는 중…</p>;
  if (error) return <p className="state-message state-error">{error}</p>;

  if (projects.length === 0) {
    return (
      <div className="empty-state">
        <p className="empty-state-text">프로젝트가 없습니다.</p>
        <p className="empty-state-sub">새 프로젝트를 만들어 시작하세요.</p>
      </div>
    );
  }

  return (
    <ul className="project-list">
      {projects.map((p) => (
        <li
          key={p.id}
          className="project-item"
          onClick={() => navigate(`/projects/${p.id}`)}
        >
          <div className="project-item-main">
            <span className="project-item-title">{p.title}</span>
            <div className="project-item-badges">
              <span className={`badge badge-status badge-status--${p.status}`}>
                {STATUS_LABEL[p.status] ?? p.status}
              </span>
              <span className={`badge badge-priority badge-priority--${p.priority}`}>
                {PRIORITY_LABEL[p.priority] ?? p.priority}
              </span>
            </div>
          </div>
          {p.description && (
            <p className="project-item-desc">{p.description}</p>
          )}
          {p.due_date && (
            <p className="project-item-due">마감: {p.due_date}</p>
          )}
        </li>
      ))}
    </ul>
  );
}
