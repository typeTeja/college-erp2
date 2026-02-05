"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { RegulationMaster } from '@/components/academics/RegulationMaster';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Academic Regulations Page
 * 
 * Migrated from: Settings > Regulations
 * New Location: /config/academic/regulations
 * Badge: Config
 * 
 * Yearly configuration for academic regulations and policies.
 */
export default function RegulationsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Academic Regulations"
                description="Manage academic regulations and policies"
                badge="config"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage academic regulations.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Academic Regulations"
            description="Manage academic regulations, policies, and compliance rules"
            badge="config"
            movedFrom="Settings > Regulations"
        >
            <RegulationMaster />
        </ConfigPageTemplate>
    );
}
