'use client';

import { AdminDashboard } from '@/components/dashboard/AdminDashboard';
import { FacultyDashboard } from '@/components/dashboard/FacultyDashboard';
import { useAuthStore } from '@/store/use-auth-store';

export default function DashboardPage() {
  const { user, hasHydrated } = useAuthStore();

  // Loading state for hydration
  if (!hasHydrated) {
    return (
      <div className="flex h-[50vh] w-full items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-primary" />
          <p className="mt-2 text-sm text-slate-500">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // Default to nothing if no role found to prevent flashing unauthorized content
  const userRole = user?.roles?.[0]?.toUpperCase();

  if (!userRole) {
    return (
      <div className="flex h-[50vh] w-full items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-primary" />
          <p className="mt-2 text-sm text-slate-500">Verifying session...</p>
        </div>
      </div>
    );
  }

  const renderDashboard = () => {
    switch (userRole) {
      case 'SUPER_ADMIN':
      case 'ADMIN':
      case 'PRINCIPAL':
      case 'ADMISSION_OFFICER':
      case 'ODC_COORDINATOR':
      case 'ACCOUNTS':
      case 'LIBRARIAN':
      case 'WARDEN':
        return <AdminDashboard />;
      case 'FACULTY':
        return <FacultyDashboard />;
      default:
        return <AdminDashboard />;
    }
  };

  return renderDashboard();
}
