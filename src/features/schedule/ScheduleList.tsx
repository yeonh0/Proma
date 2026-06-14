import { useEffect, useImperativeHandle, forwardRef, useState } from 'react';
import { scheduleApi } from './api';
import type { Schedule } from './types';

function formatDateTime(iso: string): string {
  const d = new Date(iso);
  if (isNaN(d.getTime())) return iso;
  return d.toLocaleString('ko-KR', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', hour12: false,
  });
}

interface Props {
  onAdd?: () => void;
  onEdit?: (schedule: Schedule) => void;
}

export interface ScheduleListRef {
  refresh: () => void;
}

const ScheduleList = forwardRef<ScheduleListRef, Props>(function ScheduleList({ onAdd, onEdit }, ref) {
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setLoading(true);
    scheduleApi.list()
      .then(setSchedules)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  useImperativeHandle(ref, () => ({ refresh: load }));

  const handleDelete = async (s: Schedule) => {
    if (!confirm(`"${s.title}" 일정을 삭제하시겠습니까?`)) return;
    try {
      await scheduleApi.delete(s.id);
      setSchedules((prev) => prev.filter((x) => x.id !== s.id));
    } catch (e) {
      alert(String(e));
    }
  };

  if (loading) return <p className="state-message">불러오는 중…</p>;
  if (error) return <p className="state-message state-error">{error}</p>;

  return (
    <div>
      <div className="task-list-header">
        <span className="task-count">{schedules.length}개</span>
        {onAdd && (
          <button className="btn btn-primary" onClick={onAdd}>+ 일정 추가</button>
        )}
      </div>

      {schedules.length === 0 ? (
        <div className="empty-state">
          <p className="empty-state-text">일정이 없습니다.</p>
          <p className="empty-state-sub">일정 추가 버튼으로 첫 번째 일정을 만드세요.</p>
        </div>
      ) : (
        <ul className="schedule-list">
          {schedules.map((s) => (
            <li key={s.id} className="schedule-item">
              <div className="schedule-time">{formatDateTime(s.scheduled_at)}</div>
              <div className="schedule-body">
                <span className="schedule-title">{s.title}</span>
                {s.description && <p className="schedule-desc">{s.description}</p>}
                <div className="schedule-meta">
                  {s.duration_minutes != null && (
                    <span className="schedule-badge">{s.duration_minutes}분</span>
                  )}
                  {s.is_recurring && (
                    <span className="schedule-badge schedule-badge--recurring">반복</span>
                  )}
                </div>
              </div>
              <div className="schedule-actions">
                {onEdit && (
                  <button className="btn btn-secondary" style={{ padding: '4px 10px', fontSize: 12 }} onClick={() => onEdit(s)}>수정</button>
                )}
                <button className="task-delete-btn" onClick={() => handleDelete(s)} title="삭제">✕</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
});

export default ScheduleList;
