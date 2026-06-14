import { useRef, useState } from 'react';
import ScheduleList, { type ScheduleListRef } from '../features/schedule/ScheduleList';
import type { Schedule } from '../features/schedule/types';

export default function SchedulePage() {
  const listRef = useRef<ScheduleListRef>(null);
  const [editTarget, setEditTarget] = useState<Schedule | null>(null);
  const [showModal, setShowModal] = useState(false);

  const handleAdd = () => {
    setEditTarget(null);
    setShowModal(true);
  };

  const handleEdit = (s: Schedule) => {
    setEditTarget(s);
    setShowModal(true);
  };

  return (
    <div className="page">
      <div className="page-header">
        <h2 className="page-title">일정</h2>
      </div>
      <ScheduleList
        ref={listRef}
        onAdd={handleAdd}
        onEdit={handleEdit}
      />
      {showModal && (
        <div className="modal-backdrop" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">
                {editTarget ? '일정 수정' : '일정 추가'}
              </h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>✕</button>
            </div>
            <div className="modal-body">
              <p className="state-message">일정 추가/수정 폼은 Task 2-4에서 구현됩니다.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
