'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/use-auth-store';

export default function RootPage() {
  const router = useRouter();
  const { user, hasHydrated } = useAuthStore();

  useEffect(() => {
    if (!hasHydrated) return;

    if (!user) {
      router.push('/login');
      return;
    }

    const userRole = user?.roles?.[0]?.toUpperCase();

    // Redirect based on role
    switch (userRole) {
      case 'SUPER_ADMIN':
      case 'ADMIN':
      case 'PRINCIPAL':
      case 'ADMISSION_OFFICER':
      case 'ODC_COORDINATOR':
      case 'ACCOUNTS':
      case 'LIBRARIAN':
      case 'WARDEN':
      case 'FACULTY':
        // Admin and faculty go to dashboard
        router.push('/dashboard');
        break;
      case 'STUDENT':
      default:
        // Students/applicants go to applicant portal
        router.push('/applicant');
        break;
    }
  }, [user, hasHydrated, router]);

  // Loading state
  return (
    <div className="flex h-screen w-full items-center justify-center">
      <div className="text-center">
        <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-primary" />
        <p className="mt-2 text-sm text-slate-500">Loading...</p>
      </div>
    </div>
  );
}
