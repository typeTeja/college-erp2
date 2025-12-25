'use client';

import { useAuthStore } from '@/store/use-auth-store';
import { AdminFeePanel } from '@/components/fees/AdminFeePanel';
import { FeeDashboard } from '@/components/fees/FeeDashboard';

export default function FeesPage() {
    const { user, hasHydrated } = useAuthStore();

    // Loading state for hydration
    if (!hasHydrated) {
        return (
            <div className="flex h-[50vh] w-full items-center justify-center">
                <div className="text-center">
                    <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-primary" />
                    <p className="mt-2 text-sm text-slate-500">Loading fee details...</p>
                </div>
            </div>
        );
    }

    const userRole = user?.roles?.[0]?.toUpperCase();

    // Determine which view to show based on role
    const renderFeeView = () => {
        switch (userRole) {
            case 'SUPER_ADMIN':
            case 'ADMIN':
            case 'PRINCIPAL':
            case 'ACCOUNTS':
                // Admin view - show fee management panel
                return <AdminFeePanel />;

            case 'STUDENT':
                // Student view - show their fee dashboard
                // In a real app, you'd get the student_id from the user object
                const studentId = user?.id || 0;
                return <FeeDashboard studentId={studentId} />;

            default:
                // For other roles, show a message
                return (
                    <div className="flex h-[50vh] w-full items-center justify-center">
                        <div className="text-center">
                            <p className="text-lg text-slate-600">Fee management access not available for your role.</p>
                        </div>
                    </div>
                );
        }
    };

    return (
        <>
            {renderFeeView()}
        </>
    );
}
