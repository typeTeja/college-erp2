"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';
import { History } from 'lucide-react';

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
            <Card>
                <CardContent className="pt-6">
                    <div className="text-center py-12">
                        <History className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-slate-900 mb-2">
                            Audit Logs
                        </h3>
                        <p className="text-sm text-slate-500 mb-4">
                            Audit log viewer will be implemented in a future update.
                        </p>
                        <p className="text-xs text-slate-400">
                            This page will display system-wide audit trail of all user actions.
                        </p>
                    </div>
                </CardContent>
            </Card>
        </ConfigPageTemplate>
    );
}
