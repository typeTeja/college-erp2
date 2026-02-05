"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { BatchMaster } from '@/components/academics/BatchMaster';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Batches Page
 * 
 * Migrated from: Settings > Academic Batches
 * New Location: /setup/batches
 * Badge: Setup
 * 
 * Yearly setup for student batches.
 * Batches are program-specific and linked to academic years.
 */
export default function BatchesPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Batches"
                description="Manage student batches"
                badge="setup"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage batches.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Batches"
            description="Manage student batches by program and academic year"
            badge="setup"
            movedFrom="Settings > Academic Batches"
        >
            <BatchMaster />
        </ConfigPageTemplate>
    );
}
