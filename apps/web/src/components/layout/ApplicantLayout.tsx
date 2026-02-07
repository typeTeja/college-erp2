'use client';

import { useAuthStore } from '@/store/use-auth-store';
import { LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';

export function ApplicantLayout({ children }: { children: React.ReactNode }) {
    const { user, logout } = useAuthStore();
    const router = useRouter();

    const handleLogout = () => {
        logout();
        router.push('/login');
    };

    if (!user) {
        return null;
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Minimal Header for Applicants */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-30">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        {/* Logo */}
                        <div className="flex items-center gap-3">
                            <h1 className="text-xl font-bold text-gray-900">College ERP</h1>
                            <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded">
                                Applicant Portal
                            </span>
                        </div>

                        {/* User Info & Logout */}
                        <div className="flex items-center gap-4">
                            <div className="hidden sm:block text-right">
                                <p className="text-sm font-medium text-gray-900">{user.name || user.email}</p>
                                <p className="text-xs text-gray-500">{user.email}</p>
                            </div>

                            <Button 
                                variant="ghost" 
                                size="sm" 
                                onClick={handleLogout}
                                className="gap-2 text-red-600 hover:text-red-700 hover:bg-red-50"
                            >
                                <LogOut className="h-4 w-4" />
                                <span className="hidden sm:inline">Logout</span>
                            </Button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {children}
            </main>
        </div>
    );
}
