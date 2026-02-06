"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { StructureExplorer } from '@/components/academics/structure-tree/StructureExplorer';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Academic Structure Page
 * 
 * Migrated from: Settings > Academic Structure
 * New Location: /config/academic/structure
 * Badge: Config
 * 
 * Yearly configuration for academic structure (semesters, subjects, credits).
 */
export default function AcademicStructurePage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Academic Structure"
                description="Manage academic structure"
                badge="config"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage academic structure.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Academic Structure"
            description="Configure semesters, subjects, credits, and academic organization"
            badge="config"
            movedFrom="Settings > Academic Structure"
        >
            <StructureExplorer />
        </ConfigPageTemplate>
    );
}
