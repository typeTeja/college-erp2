"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { AuditLogsTab } from '../../settings/AuditLogsTab';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Audit Logs Page
 * 
 * Migrated from: Settings > Audit Logs
 * New Location: /system/audit
 * Badge: Admin
 * 
 * System-level audit trail for all user actions.
 */
export default function AuditPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is super admin
    const isSuperAdmin = !!user?.roles.some(r => r === "SUPER_ADMIN");

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isSuperAdmin) {
        return (
            <ConfigPageTemplate
                title="Audit Logs"
                description="View system audit trail"
                badge="admin"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to view audit logs.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Audit Logs"
            description="View system audit trail and user activity logs"
            badge="admin"
            movedFrom="Settings > Audit Logs"
        >
            <AuditLogsTab />
        </ConfigPageTemplate>
    );
}
