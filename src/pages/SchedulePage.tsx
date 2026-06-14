import { useRef, useState } from 'react';
import ScheduleList, { type ScheduleListRef } from '../features/schedule/ScheduleList';
import ScheduleFormModal from '../features/schedule/ScheduleFormModal';
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

  const handleClose = () => setShowModal(false);
  const handleSaved = () => listRef.current?.refresh();

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
        <ScheduleFormModal
          schedule={editTarget ?? undefined}
          onClose={handleClose}
          onSaved={handleSaved}
        />
      )}
    </div>
  );
}
