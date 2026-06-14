import { useParams } from 'react-router-dom';

export default function EmailDetailPage() {
  const { id } = useParams<{ id: string }>();
  return (
    <div className="page">
      <h2 className="page-title">메일 상세</h2>
      <p className="page-placeholder">ID: {id} — Phase 3에서 구현 예정</p>
    </div>
  );
}
