import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EmailList, { type EmailListRef } from '../features/email/EmailList';
import { emailApi } from '../features/email/api';
import { openEmlFileDialog } from '../shared/lib/dialog';

export default function EmailPage() {
  const navigate = useNavigate();
  const listRef = useRef<EmailListRef>(null);
  const [importing, setImporting] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleImport = async () => {
    const files = await openEmlFileDialog();
    if (!files || files.length === 0) return;
    setImporting(true);
    try {
      for (const filePath of files) {
        await emailApi.import(filePath);
      }
      listRef.current?.refresh();
    } catch (e) {
      alert(String(e));
    } finally {
      setImporting(false);
    }
  };

  const handleDeleteAll = async () => {
    if (!confirm('임포트된 이메일을 전부 삭제합니다. 계속하시겠습니까?')) return;
    setDeleting(true);
    try {
      await emailApi.deleteAll();
      listRef.current?.refresh();
    } catch (e) {
      alert(String(e));
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h2 className="page-title">메일</h2>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button className="btn btn-danger" onClick={handleDeleteAll} disabled={deleting || importing}>
            {deleting ? '삭제 중…' : '전체 삭제'}
          </button>
          <button className="btn btn-primary" onClick={handleImport} disabled={importing || deleting}>
            {importing ? '임포트 중…' : '+ EML 임포트'}
          </button>
        </div>
      </div>
      <EmailList ref={listRef} onSelect={(id) => navigate(`/emails/${id}`)} />
    </div>
  );
}
