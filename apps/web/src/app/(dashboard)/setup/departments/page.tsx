"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { DepartmentsTab } from '../../settings/MasterDataTabs';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Departments Page
 * 
 * Migrated from: Settings > Departments
 * New Location: /setup/departments
 * Badge: Setup
 * 
 * One-time institutional setup for academic departments.
 */
export default function DepartmentsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Departments"
                description="Manage academic departments"
                badge="setup"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage departments.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Departments"
            description="Manage academic departments and their codes"
            badge="setup"
            movedFrom="Settings > Departments"
        >
            <DepartmentsTab />
        </ConfigPageTemplate>
    );
}
