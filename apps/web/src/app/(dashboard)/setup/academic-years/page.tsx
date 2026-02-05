"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { AcademicYearMaster } from '@/components/academics/AcademicYearMaster';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Academic Years Page
 * 
 * Migrated from: Settings > Academic Years
 * New Location: /setup/academic-years
 * Badge: Setup
 * 
 * Yearly setup for academic year periods.
 * Defines start/end dates and current academic year status.
 */
export default function AcademicYearsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Academic Years"
                description="Manage academic year periods"
                badge="setup"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage academic years.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Academic Years"
            description="Manage academic year periods and set the current active year"
            badge="setup"
            movedFrom="Settings > Academic Years"
        >
            <AcademicYearMaster />
        </ConfigPageTemplate>
    );
}
