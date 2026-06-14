import { useRef, useState } from 'react';
import ProjectList from '../features/project/ProjectList';
import ProjectFormModal from '../features/project/ProjectFormModal';

export default function ProjectPage() {
  const refreshRef = useRef<() => void>(() => {});
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="page">
      <div className="page-header">
        <h2 className="page-title">프로젝트</h2>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          + 새 프로젝트
        </button>
      </div>

      <ProjectList onRefreshRef={(fn) => { refreshRef.current = fn; }} />

      {showModal && (
        <ProjectFormModal
          onClose={() => setShowModal(false)}
          onSaved={() => refreshRef.current()}
        />
      )}
    </div>
  );
}
