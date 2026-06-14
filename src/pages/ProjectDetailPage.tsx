import { useParams } from 'react-router-dom';

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  return (
    <div className="page">
      <h2 className="page-title">프로젝트 상세</h2>
      <p className="page-placeholder">ID: {id} — Phase 1에서 구현 예정</p>
    </div>
  );
}
