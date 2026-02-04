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
import { AnnouncementBanner } from '@/components/ui/announcement-banner';
import { FeedbackWidget } from '@/components/ui/feedback-widget';
import { isFeatureEnabled } from '@/config/feature-flags';

function DashboardContent({ children }: { children: React.ReactNode }) {
    const { sidebarCollapsed } = useNavPreferences();
    const { user } = useAuthStore();

    // Enable keyboard shortcuts (inside provider)
    useKeyboardShortcuts();

    // Check if feedback widget should be shown
    const showFeedbackWidget = user?.id && isFeatureEnabled('ROLLOUT_PERCENTAGE', user.id);

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

                {/* Announcement Banner */}
                <AnnouncementBanner
                    title="Welcome to the New College ERP Experience!"
                    message="We've completed the upgrade to the new navigation and dashboards. Everything you need is now faster and easier to find."
                    ctaText="Take a Tour"
                    ctaLink="/docs/whats-new"
                    variant="success"
                    dismissible
                    storageKey="announcement-launch-v1-feb-2026"
                />

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

            {/* Feedback Widget (conditionally rendered based on rollout) */}
            {showFeedbackWidget && <FeedbackWidget />}
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
