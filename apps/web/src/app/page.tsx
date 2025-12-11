'use client';

import { useAuthStore } from '@/store/use-auth-store';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { AdminDashboard } from '@/components/dashboard/AdminDashboard';
import { StudentDashboard } from '@/components/dashboard/StudentDashboard';
import { FacultyDashboard } from '@/components/dashboard/FacultyDashboard';

export default function DashboardPage() {
  const { user } = useAuthStore();

  // Default to STUDENT if no role found, though login flow should ensure role
  const userRole = user?.roles?.[0] || 'STUDENT';

  const renderDashboard = () => {
    switch (userRole) {
      case 'SUPER_ADMIN':
      case 'ADMIN':
        return <AdminDashboard />;
      case 'FACULTY':
        return <FacultyDashboard />;
      case 'STUDENT':
        return <StudentDashboard />;
      default:
        return <StudentDashboard />;
    }
  };

  return (
    <DashboardLayout>
      {renderDashboard()}
    </DashboardLayout>
  );
}
