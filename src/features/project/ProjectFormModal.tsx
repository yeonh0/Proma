import { useEffect, useRef, useState } from 'react';
import { projectApi } from './api';
import type { Project, CreateProjectRequest, UpdateProjectRequest, Status, Priority } from './types';

interface Props {
  project?: Project;
  onClose: () => void;
  onSaved: () => void;
}

const STATUS_OPTIONS = [
  { value: 'active', label: '진행 중' },
  { value: 'paused', label: '일시 중단' },
  { value: 'completed', label: '완료' },
  { value: 'archived', label: '보관' },
] as const;

const PRIORITY_OPTIONS = [
  { value: 'high', label: '높음' },
  { value: 'medium', label: '보통' },
  { value: 'low', label: '낮음' },
] as const;

export default function ProjectFormModal({ project, onClose, onSaved }: Props) {
  const isEdit = project !== undefined;

  const [title, setTitle] = useState(project?.title ?? '');
  const [description, setDescription] = useState(project?.description ?? '');
  const [status, setStatus] = useState<Status>(project?.status ?? 'active');
  const [priority, setPriority] = useState<Priority>(project?.priority ?? 'medium');
  const [startDate, setStartDate] = useState(project?.start_date ?? '');
  const [dueDate, setDueDate] = useState(project?.due_date ?? '');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const titleRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    titleRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('프로젝트 이름을 입력하세요.');
      titleRef.current?.focus();
      return;
    }

    setSaving(true);
    setError(null);

    try {
      if (isEdit) {
        const req: UpdateProjectRequest = {
          parent_id: project.parent_id,
          title: title.trim(),
          description: description.trim() || null,
          status,
          priority,
          start_date: startDate || null,
          due_date: dueDate || null,
          completed_at: status === 'completed' ? (project.completed_at ?? new Date().toISOString().slice(0, 10)) : null,
        };
        await projectApi.update(project.id, req);
      } else {
        const req: CreateProjectRequest = {
          title: title.trim(),
          description: description.trim() || null,
          status,
          priority,
          start_date: startDate || null,
          due_date: dueDate || null,
        };
        await projectApi.create(req);
      }
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
          <h3 className="modal-title">{isEdit ? '프로젝트 수정' : '새 프로젝트'}</h3>
          <button className="modal-close" onClick={onClose} aria-label="닫기">✕</button>
        </div>

        <form className="modal-body" onSubmit={handleSubmit}>
          {error && <p className="form-error">{error}</p>}

          <label className="form-label">
            프로젝트 이름 <span className="form-required">*</span>
            <input
              ref={titleRef}
              className="form-input"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="프로젝트 이름 입력"
              maxLength={100}
            />
          </label>

          <label className="form-label">
            설명
            <textarea
              className="form-input form-textarea"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="프로젝트 설명 (선택)"
              rows={3}
            />
          </label>

          <div className="form-row">
            <label className="form-label">
              상태
              <select className="form-input" value={status} onChange={(e) => setStatus(e.target.value as Status)}>
                {STATUS_OPTIONS.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
            </label>
            <label className="form-label">
              우선순위
              <select className="form-input" value={priority} onChange={(e) => setPriority(e.target.value as Priority)}>
                {PRIORITY_OPTIONS.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
            </label>
          </div>

          <div className="form-row">
            <label className="form-label">
              시작일
              <input
                className="form-input"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </label>
            <label className="form-label">
              마감일
              <input
                className="form-input"
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
              />
            </label>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={saving}>
              취소
            </button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? '저장 중…' : isEdit ? '수정' : '생성'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
