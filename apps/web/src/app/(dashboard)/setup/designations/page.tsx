"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { DesignationTab } from '../../settings/MasterDataTabs';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Designations Page
 * 
 * Migrated from: Settings > Designations
 * New Location: /setup/designations
 * Badge: Setup
 * 
 * Rare setup for faculty designations (Professor, Associate Professor, etc.)
 */
export default function DesignationsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Designations"
                description="Manage faculty designations"
                badge="setup"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage designations.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Designations"
            description="Manage faculty designations and positions"
            badge="setup"
            movedFrom="Settings > Designations"
        >
            <DesignationTab />
        </ConfigPageTemplate>
    );
}
