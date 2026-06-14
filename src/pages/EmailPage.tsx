import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EmailList, { type EmailListRef } from '../features/email/EmailList';
import { emailApi } from '../features/email/api';
import { openEmlFileDialog } from '../shared/lib/dialog';

export default function EmailPage() {
  const navigate = useNavigate();
  const listRef = useRef<EmailListRef>(null);
  const [importing, setImporting] = useState(false);

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

  return (
    <div className="page">
      <div className="page-header">
        <h2 className="page-title">메일</h2>
        <button className="btn btn-primary" onClick={handleImport} disabled={importing}>
          {importing ? '임포트 중…' : '+ EML 임포트'}
        </button>
      </div>
      <EmailList ref={listRef} onSelect={(id) => navigate(`/emails/${id}`)} />
    </div>
  );
}
