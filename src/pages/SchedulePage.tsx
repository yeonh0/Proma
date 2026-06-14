import { useEffect, useRef, useState } from 'react';
import ScheduleList, { type ScheduleListRef } from '../features/schedule/ScheduleList';
import ScheduleFormModal from '../features/schedule/ScheduleFormModal';
import ScheduleCalendar from '../features/schedule/ScheduleCalendar';
import { scheduleApi } from '../features/schedule/api';
import type { Schedule } from '../features/schedule/types';

type Tab = 'list' | 'calendar';

export default function SchedulePage() {
  const listRef = useRef<ScheduleListRef>(null);
  const [editTarget, setEditTarget] = useState<Schedule | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [tab, setTab] = useState<Tab>('list');

  const today = new Date();
  const [calYear, setCalYear] = useState(today.getFullYear());
  const [calMonth, setCalMonth] = useState(today.getMonth());
  const [allSchedules, setAllSchedules] = useState<Schedule[]>([]);

  useEffect(() => {
    if (tab === 'calendar') {
      scheduleApi.list().then(setAllSchedules).catch(() => {});
    }
  }, [tab]);

  const handleAdd = () => {
    setEditTarget(null);
    setShowModal(true);
  };

  const handleEdit = (s: Schedule) => {
    setEditTarget(s);
    setShowModal(true);
  };

  const handleClose = () => setShowModal(false);
  const handleSaved = () => {
    listRef.current?.refresh();
    if (tab === 'calendar') {
      scheduleApi.list().then(setAllSchedules).catch(() => {});
    }
  };

  const prevMonth = () => {
    if (calMonth === 0) { setCalYear((y) => y - 1); setCalMonth(11); }
    else setCalMonth((m) => m - 1);
  };

  const nextMonth = () => {
    if (calMonth === 11) { setCalYear((y) => y + 1); setCalMonth(0); }
    else setCalMonth((m) => m + 1);
  };

  const MONTH_NAMES = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];

  return (
    <div className="page">
      <div className="page-header">
        <h2 className="page-title">일정</h2>
        <button className="btn btn-primary" onClick={handleAdd}>+ 일정 추가</button>
      </div>

      <div className="tabs">
        <button className={`tab-btn${tab === 'list' ? ' active' : ''}`} onClick={() => setTab('list')}>목록</button>
        <button className={`tab-btn${tab === 'calendar' ? ' active' : ''}`} onClick={() => setTab('calendar')}>캘린더</button>
      </div>

      {tab === 'list' && (
        <ScheduleList ref={listRef} onEdit={handleEdit} />
      )}

      {tab === 'calendar' && (
        <div>
          <div className="calendar-nav">
            <button className="btn btn-secondary" onClick={prevMonth}>‹</button>
            <span className="calendar-nav-title">{calYear}년 {MONTH_NAMES[calMonth]}</span>
            <button className="btn btn-secondary" onClick={nextMonth}>›</button>
          </div>
          <ScheduleCalendar
            year={calYear}
            month={calMonth}
            schedules={allSchedules}
          />
        </div>
      )}

      {showModal && (
        <ScheduleFormModal
          schedule={editTarget ?? undefined}
          onClose={handleClose}
          onSaved={handleSaved}
        />
      )}
    </div>
  );
}
