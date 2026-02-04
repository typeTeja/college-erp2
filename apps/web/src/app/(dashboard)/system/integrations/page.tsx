"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';
import { Globe } from 'lucide-react';

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
            <Card>
                <CardContent className="pt-6">
                    <div className="text-center py-12">
                        <Globe className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-slate-900 mb-2">
                            Integrations Management
                        </h3>
                        <p className="text-sm text-slate-500 mb-4">
                            Integration management interface will be implemented in a future update.
                        </p>
                        <p className="text-xs text-slate-400">
                            This page will manage payment gateways, email services, and other third-party integrations.
                        </p>
                    </div>
                </CardContent>
            </Card>
        </ConfigPageTemplate>
    );
}
