import { useEffect, forwardRef, useImperativeHandle, useState } from 'react';
import { emailApi } from './api';
import type { Email } from './types';

function formatSender(sender: string | null): string {
  if (!sender) return '(발신자 없음)';
  const match = sender.match(/^"?([^"<]+)"?\s*</);
  return match ? match[1].trim() : sender;
}

function formatDate(iso: string | null): string {
  if (!iso) return '';
  try {
    return new Date(iso).toLocaleString('ko-KR', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', hour12: false,
    });
  } catch {
    return iso;
  }
}

interface Props {
  onSelect: (id: number) => void;
}

export interface EmailListRef {
  refresh: () => void;
}

const EmailList = forwardRef<EmailListRef, Props>(function EmailList({ onSelect }, ref) {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setLoading(true);
    emailApi.list()
      .then(setEmails)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);
  useImperativeHandle(ref, () => ({ refresh: load }));

  if (loading) return <p className="state-message">불러오는 중…</p>;
  if (error) return <p className="state-message state-error">{error}</p>;

  if (emails.length === 0) {
    return (
      <div className="empty-state">
        <p className="empty-state-text">임포트된 이메일이 없습니다.</p>
        <p className="empty-state-sub">.eml 파일을 임포트해 시작하세요.</p>
      </div>
    );
  }

  return (
    <ul className="email-list">
      {emails.map((e) => (
        <li key={e.id} className="email-item" onClick={() => onSelect(e.id)}>
          <div className="email-item-header">
            <span className="email-sender">{formatSender(e.sender)}</span>
            <span className="email-date">{formatDate(e.sent_at)}</span>
          </div>
          <div className="email-subject">{e.subject ?? '(제목 없음)'}</div>
          {e.body_text && (
            <div className="email-preview">
              {e.body_text.trim().slice(0, 120)}
            </div>
          )}
        </li>
      ))}
    </ul>
  );
});

export default EmailList;
