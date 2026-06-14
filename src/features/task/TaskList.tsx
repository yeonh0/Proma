import { useEffect, useState } from 'react';
import { taskApi } from './api';
import type { Task, CreateTaskRequest, UpdateTaskRequest, TaskStatus, Priority } from './types';

const STATUS_LABEL: Record<TaskStatus, string> = {
  todo: '할 일', in_progress: '진행 중', done: '완료',
};
const PRIORITY_LABEL: Record<string, string> = {
  high: '높음', medium: '보통', low: '낮음',
};
const NEXT_STATUS: Record<TaskStatus, TaskStatus> = {
  todo: 'in_progress', in_progress: 'done', done: 'todo',
};

interface Props {
  projectId: number;
}

export default function TaskList({ projectId }: Props) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  const load = () => {
    setLoading(true);
    taskApi.list(projectId)
      .then(setTasks)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [projectId]);

  const cycleStatus = async (task: Task) => {
    const next = NEXT_STATUS[task.status];
    const req: UpdateTaskRequest = {
      title: task.title,
      description: task.description,
      status: next,
      priority: task.priority as Priority,
      due_date: task.due_date,
      completed_at: next === 'done' ? new Date().toISOString().slice(0, 10) : null,
    };
    try {
      const updated = await taskApi.update(task.id, req);
      setTasks((prev) => prev.map((t) => (t.id === task.id ? updated : t)));
    } catch (e) {
      alert(String(e));
    }
  };

  const deleteTask = async (task: Task) => {
    if (!confirm(`"${task.title}" Task를 삭제하시겠습니까?`)) return;
    try {
      await taskApi.delete(task.id);
      setTasks((prev) => prev.filter((t) => t.id !== task.id));
    } catch (e) {
      alert(String(e));
    }
  };

  if (loading) return <p className="state-message">불러오는 중…</p>;
  if (error) return <p className="state-message state-error">{error}</p>;

  return (
    <div>
      <div className="task-list-header">
        <span className="task-count">{tasks.length}개</span>
        <button className="btn btn-primary" onClick={() => setShowForm(true)}>+ Task 추가</button>
      </div>

      {tasks.length === 0 ? (
        <div className="empty-state">
          <p className="empty-state-text">Task가 없습니다.</p>
          <p className="empty-state-sub">Task를 추가해 작업을 시작하세요.</p>
        </div>
      ) : (
        <ul className="task-list">
          {tasks.map((t) => (
            <li key={t.id} className={`task-item task-item--${t.status}`}>
              <button
                className={`task-status-btn task-status-btn--${t.status}`}
                onClick={() => cycleStatus(t)}
                title={`→ ${STATUS_LABEL[NEXT_STATUS[t.status]]}`}
              >
                {t.status === 'done' ? '✓' : t.status === 'in_progress' ? '▶' : '○'}
              </button>
              <div className="task-body">
                <span className="task-title">{t.title}</span>
                {t.description && <p className="task-desc">{t.description}</p>}
                <div className="task-meta">
                  <span className={`badge badge-priority badge-priority--${t.priority}`}>
                    {PRIORITY_LABEL[t.priority]}
                  </span>
                  {t.due_date && <span className="task-due">마감 {t.due_date}</span>}
                </div>
              </div>
              <button className="task-delete-btn" onClick={() => deleteTask(t)} title="삭제">✕</button>
            </li>
          ))}
        </ul>
      )}

      {showForm && (
        <TaskFormModal
          projectId={projectId}
          onClose={() => setShowForm(false)}
          onSaved={load}
        />
      )}
    </div>
  );
}

/* ── 인라인 Task 추가 모달 ── */

interface ModalProps {
  projectId: number;
  onClose: () => void;
  onSaved: () => void;
}

const PRIORITY_OPTIONS: { value: Priority; label: string }[] = [
  { value: 'high', label: '높음' },
  { value: 'medium', label: '보통' },
  { value: 'low', label: '낮음' },
];

function TaskFormModal({ projectId, onClose, onSaved }: ModalProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<Priority>('medium');
  const [dueDate, setDueDate] = useState('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) { setError('Task 이름을 입력하세요.'); return; }
    setSaving(true);
    setError(null);
    try {
      const req: CreateTaskRequest = {
        project_id: projectId,
        title: title.trim(),
        description: description.trim() || null,
        priority,
        due_date: dueDate || null,
      };
      await taskApi.create(req);
      onSaved();
      onClose();
    } catch (e) {
      setError(String(e));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">Task 추가</h3>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <form className="modal-body" onSubmit={handleSubmit}>
          {error && <p className="form-error">{error}</p>}
          <label className="form-label">
            이름 <span className="form-required">*</span>
            <input className="form-input" type="text" value={title}
              onChange={(e) => setTitle(e.target.value)} placeholder="Task 이름" autoFocus />
          </label>
          <label className="form-label">
            설명
            <textarea className="form-input form-textarea" value={description}
              onChange={(e) => setDescription(e.target.value)} rows={2} />
          </label>
          <div className="form-row">
            <label className="form-label">
              우선순위
              <select className="form-input" value={priority}
                onChange={(e) => setPriority(e.target.value as Priority)}>
                {PRIORITY_OPTIONS.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
            </label>
            <label className="form-label">
              마감일
              <input className="form-input" type="date" value={dueDate}
                onChange={(e) => setDueDate(e.target.value)} />
            </label>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={saving}>취소</button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? '저장 중…' : '추가'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
