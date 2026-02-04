"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { IntegrationsTab } from '../../settings/IntegrationsTab';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Integrations Page
 * 
 * Migrated from: Settings > Integrations
 * New Location: /system/integrations
 * Badge: Admin
 * 
 * System-level configuration for third-party integrations.
 */
export default function IntegrationsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is super admin
    const isSuperAdmin = !!user?.roles.some(r => r === "SUPER_ADMIN");

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isSuperAdmin) {
        return (
            <ConfigPageTemplate
                title="Integrations"
                description="Manage third-party integrations"
                badge="admin"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage integrations.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Integrations"
            description="Manage third-party integrations and API configurations"
            badge="admin"
            movedFrom="Settings > Integrations"
        >
            <IntegrationsTab isSuperAdmin={isSuperAdmin} />
        </ConfigPageTemplate>
    );
}
