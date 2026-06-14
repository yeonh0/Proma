import { Outlet } from 'react-router-dom';
import Sidebar from '../shared/components/Sidebar';

export default function AppLayout() {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
