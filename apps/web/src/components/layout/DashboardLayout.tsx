/**
 * Dashboard Layout
 * Main layout with new grouped navigation system
 */
'use client';

import { NavigationProvider } from '@/contexts/NavigationContext';
import { GroupedSidebar } from '@/components/navigation/GroupedSidebar';
import { CommandPalette } from '@/components/navigation/CommandPalette';
import { Breadcrumbs } from '@/components/navigation/Breadcrumbs';
import { MobileBottomNav } from '@/components/navigation/MobileBottomNav';
import { TopNav } from './TopNav';
import { useAuthStore } from '@/store/use-auth-store';
import { useKeyboardShortcuts } from '@/hooks/use-keyboard-shortcuts';
import { useNavPreferences } from '@/hooks/use-nav-preferences';

function DashboardContent({ children }: { children: React.ReactNode }) {
    const { sidebarCollapsed } = useNavPreferences();

    // Enable keyboard shortcuts (inside provider)
    useKeyboardShortcuts();

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Desktop Sidebar */}
            <GroupedSidebar />

            {/* Command Palette (Cmd+K) */}
            <CommandPalette />

            {/* Main Content */}
            <div
                className={`transition-all duration-300 ${sidebarCollapsed ? 'md:ml-20' : 'md:ml-64'
                    }`}
            >
                {/* Top Navigation */}
                <TopNav />

                {/* Page Content */}
                <main className="p-6 pb-24 md:pb-6">
                    {/* Breadcrumbs */}
                    <Breadcrumbs />

                    {/* Page Content */}
                    {children}
                </main>
            </div>

            {/* Mobile Bottom Navigation */}
            <MobileBottomNav />
        </div>
    );
}

export function DashboardLayout({ children }: { children: React.ReactNode }) {
    const { user } = useAuthStore();

    // Get user role and permissions
    const userRole = user?.roles?.[0]?.toUpperCase() || 'SUPER_ADMIN';
    const userPermissions = user?.roles || [];

    if (!user) {
        return null;
    }

    return (
        <NavigationProvider role={userRole} userPermissions={userPermissions}>
            <DashboardContent>{children}</DashboardContent>
        </NavigationProvider>
    );
}
