import { useEffect, useState } from 'react';
import { scheduleApi } from './api';
import { projectApi } from '../project/api';
import type { Schedule, CreateScheduleRequest, UpdateScheduleRequest } from './types';
import type { Project } from '../project/types';

interface Props {
  schedule?: Schedule;
  onClose: () => void;
  onSaved: () => void;
}

export default function ScheduleFormModal({ schedule, onClose, onSaved }: Props) {
  const isEdit = Boolean(schedule);

  const [title, setTitle] = useState(schedule?.title ?? '');
  const [description, setDescription] = useState(schedule?.description ?? '');
  const [scheduledAt, setScheduledAt] = useState(
    schedule ? schedule.scheduled_at.slice(0, 16) : ''
  );
  const [durationMinutes, setDurationMinutes] = useState(
    schedule?.duration_minutes != null ? String(schedule.duration_minutes) : ''
  );
  const [isRecurring, setIsRecurring] = useState(schedule?.is_recurring ?? false);
  const [recurrenceRule, setRecurrenceRule] = useState(schedule?.recurrence_rule ?? '');
  const [projectId, setProjectId] = useState<string>(
    schedule?.project_id != null ? String(schedule.project_id) : ''
  );

  const [projects, setProjects] = useState<Project[]>([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    projectApi.list().then(setProjects).catch(() => {});
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) { setError('일정 이름을 입력하세요.'); return; }
    if (!scheduledAt) { setError('날짜/시간을 입력하세요.'); return; }
    setSaving(true);
    setError(null);

    const pid = projectId ? Number(projectId) : null;
    const dur = durationMinutes ? Number(durationMinutes) : null;

    try {
      if (isEdit && schedule) {
        const req: UpdateScheduleRequest = {
          project_id: pid,
          title: title.trim(),
          description: description.trim() || null,
          scheduled_at: scheduledAt,
          duration_minutes: dur,
          is_recurring: isRecurring,
          recurrence_rule: (isRecurring && recurrenceRule.trim()) ? recurrenceRule.trim() : null,
        };
        await scheduleApi.update(schedule.id, req);
      } else {
        const req: CreateScheduleRequest = {
          project_id: pid,
          title: title.trim(),
          description: description.trim() || null,
          scheduled_at: scheduledAt,
          duration_minutes: dur,
          is_recurring: isRecurring,
          recurrence_rule: (isRecurring && recurrenceRule.trim()) ? recurrenceRule.trim() : null,
        };
        await scheduleApi.create(req);
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
          <h3 className="modal-title">{isEdit ? '일정 수정' : '일정 추가'}</h3>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <form className="modal-body" onSubmit={handleSubmit}>
          {error && <p className="form-error">{error}</p>}

          <label className="form-label">
            일정 이름 <span className="form-required">*</span>
            <input className="form-input" type="text" value={title}
              onChange={(e) => setTitle(e.target.value)} placeholder="일정 이름" autoFocus />
          </label>

          <label className="form-label">
            설명
            <textarea className="form-input form-textarea" value={description}
              onChange={(e) => setDescription(e.target.value)} rows={2} />
          </label>

          <div className="form-row">
            <label className="form-label">
              날짜/시간 <span className="form-required">*</span>
              <input className="form-input" type="datetime-local" value={scheduledAt}
                onChange={(e) => setScheduledAt(e.target.value)} />
            </label>
            <label className="form-label">
              소요 시간 (분)
              <input className="form-input" type="number" min={1} value={durationMinutes}
                onChange={(e) => setDurationMinutes(e.target.value)} placeholder="예: 60" />
            </label>
          </div>

          <label className="form-label">
            연결 프로젝트
            <select className="form-input" value={projectId}
              onChange={(e) => setProjectId(e.target.value)}>
              <option value="">없음</option>
              {projects.map((p) => (
                <option key={p.id} value={String(p.id)}>{p.title}</option>
              ))}
            </select>
          </label>

          <label className="form-label" style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
            <input type="checkbox" checked={isRecurring}
              onChange={(e) => setIsRecurring(e.target.checked)} />
            반복 일정
          </label>

          {isRecurring && (
            <label className="form-label">
              반복 규칙 (RRULE)
              <input className="form-input" type="text" value={recurrenceRule}
                onChange={(e) => setRecurrenceRule(e.target.value)}
                placeholder="예: FREQ=WEEKLY;BYDAY=MO" />
            </label>
          )}

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={saving}>취소</button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? '저장 중…' : isEdit ? '저장' : '추가'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
