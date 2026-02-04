"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { ProgramsTab } from '../../settings/MasterDataTabs';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Programs Page
 * 
 * Migrated from: Settings > Programs/Courses
 * New Location: /setup/programs
 * Badge: Setup
 * 
 * One-time institutional setup for degree programs.
 * Programs are linked to departments and define duration, type, and academic structure.
 */
export default function ProgramsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Programs"
                description="Manage degree programs and courses"
                badge="setup"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage programs.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Programs"
            description="Manage degree programs, courses, and their configurations"
            badge="setup"
            movedFrom="Settings > Programs/Courses"
        >
            <ProgramsTab />
        </ConfigPageTemplate>
    );
}
