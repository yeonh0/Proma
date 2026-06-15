import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { projectApi } from '../features/project/api';
import { scheduleApi } from '../features/schedule/api';
import { emailApi } from '../features/email/api';
import type { Project } from '../features/project/types';
import type { Schedule } from '../features/schedule/types';
import type { Email } from '../features/email/types';

function getThisWeekRange(): [Date, Date] {
  const now = new Date();
  const day = now.getDay();
  const diff = day === 0 ? -6 : 1 - day; // Monday as week start
  const start = new Date(now);
  start.setDate(now.getDate() + diff);
  start.setHours(0, 0, 0, 0);
  const end = new Date(start);
  end.setDate(start.getDate() + 6);
  end.setHours(23, 59, 59, 999);
  return [start, end];
}

function fmtSchedule(iso: string) {
  try {
    return new Date(iso).toLocaleString('ko-KR', {
      month: '2-digit', day: '2-digit', weekday: 'short',
      hour: '2-digit', minute: '2-digit', hour12: false,
    });
  } catch { return iso; }
}

function fmtDate(iso: string | null) {
  if (!iso) return '—';
  try {
    return new Date(iso).toLocaleDateString('ko-KR', { month: '2-digit', day: '2-digit' });
  } catch { return iso; }
}

const PRIORITY_LABEL: Record<string, string> = { high: '높음', medium: '보통', low: '낮음' };

export default function DashboardPage() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([projectApi.list(), scheduleApi.list(), emailApi.list()])
      .then(([p, s, e]) => { setProjects(p); setSchedules(s); setEmails(e); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const [weekStart, weekEnd] = getThisWeekRange();

  const thisWeek = schedules
    .filter((s) => { const d = new Date(s.scheduled_at); return d >= weekStart && d <= weekEnd; })
    .sort((a, b) => a.scheduled_at.localeCompare(b.scheduled_at));

  const active = projects.filter((p) => p.status === 'active');
  const recentEmails = emails.slice(0, 5);

  if (loading) return <div className="page"><p className="state-message">불러오는 중…</p></div>;

  return (
    <div className="page">
      <h2 className="page-title">대시보드</h2>

      {/* 통계 카드 */}
      <div className="dash-stats">
        <div className="stat-card">
          <span className="stat-value">{projects.length}</span>
          <span className="stat-label">전체 프로젝트</span>
          <span className="stat-sub">
            진행 {active.length} · 완료 {projects.filter((p) => p.status === 'completed').length}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{thisWeek.length}</span>
          <span className="stat-label">이번 주 일정</span>
          <span className="stat-sub">전체 {schedules.length}개</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{emails.length}</span>
          <span className="stat-label">이메일</span>
          <span className="stat-sub">
            최근 수신: {fmtDate(emails[0]?.sent_at ?? null)}
          </span>
        </div>
      </div>

      {/* 이번 주 일정 */}
      <section className="dash-section">
        <div className="dash-section-title">이번 주 일정</div>
        {thisWeek.length === 0
          ? <p className="dash-empty">이번 주 일정이 없습니다.</p>
          : (
            <ul className="dash-list">
              {thisWeek.map((s) => (
                <li key={s.id} className="dash-item dash-item--clickable" onClick={() => navigate('/schedule')}>
                  <span className="dash-item-time">{fmtSchedule(s.scheduled_at)}</span>
                  <span className="dash-item-title">{s.title}</span>
                  {s.duration_minutes != null && (
                    <span className="dash-item-badge">{s.duration_minutes}분</span>
                  )}
                </li>
              ))}
            </ul>
          )}
      </section>

      {/* 진행 중인 프로젝트 */}
      <section className="dash-section">
        <div className="dash-section-title">진행 중인 프로젝트</div>
        {active.length === 0
          ? <p className="dash-empty">진행 중인 프로젝트가 없습니다.</p>
          : (
            <ul className="dash-list">
              {active.map((p) => (
                <li key={p.id} className="dash-item dash-item--clickable" onClick={() => navigate(`/projects/${p.id}`)}>
                  <span className="dash-item-title">{p.title}</span>
                  {p.due_date && <span className="dash-item-due">마감 {p.due_date}</span>}
                  <span className={`badge badge-priority--${p.priority}`}>
                    {PRIORITY_LABEL[p.priority] ?? p.priority}
                  </span>
                </li>
              ))}
            </ul>
          )}
      </section>

      {/* 최근 이메일 */}
      <section className="dash-section">
        <div className="dash-section-title">최근 이메일</div>
        {recentEmails.length === 0
          ? <p className="dash-empty">이메일이 없습니다.</p>
          : (
            <ul className="dash-list">
              {recentEmails.map((e) => (
                <li key={e.id} className="dash-item dash-item--clickable dash-item--email" onClick={() => navigate(`/emails/${e.id}`)}>
                  <div className="dash-email-row">
                    <span className="dash-email-sender">{e.sender ?? '(발신자 없음)'}</span>
                    <span className="dash-item-due">{fmtDate(e.sent_at)}</span>
                  </div>
                  <div className="dash-email-subject">{e.subject ?? '(제목 없음)'}</div>
                </li>
              ))}
            </ul>
          )}
      </section>
    </div>
  );
}
