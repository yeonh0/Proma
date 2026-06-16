import { NavLink } from 'react-router-dom';

const NAV_ITEMS = [
  { to: '/',          label: '대시보드', end: true  },
  { to: '/projects',  label: '프로젝트', end: false },
  { to: '/schedule',  label: '일정',    end: false },
  { to: '/emails',    label: '메일',    end: false },
  { to: '/settings',  label: '설정',    end: false },
] as const;

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">Proma</div>
      <nav className="sidebar-nav">
        {NAV_ITEMS.map(({ to, label, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) => isActive ? 'active' : undefined}
          >
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
