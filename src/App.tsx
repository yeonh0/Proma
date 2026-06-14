import { MemoryRouter, Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import DashboardPage from './pages/DashboardPage';
import ProjectPage from './pages/ProjectPage';
import ProjectDetailPage from './pages/ProjectDetailPage';
import SchedulePage from './pages/SchedulePage';
import EmailPage from './pages/EmailPage';
import EmailDetailPage from './pages/EmailDetailPage';
import SettingsPage from './pages/SettingsPage';

export default function App() {
  return (
    <MemoryRouter initialEntries={['/']}>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="projects" element={<ProjectPage />} />
          <Route path="projects/:id" element={<ProjectDetailPage />} />
          <Route path="schedule" element={<SchedulePage />} />
          <Route path="emails" element={<EmailPage />} />
          <Route path="emails/:id" element={<EmailDetailPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </MemoryRouter>
  );
}
