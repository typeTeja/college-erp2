"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import ScholarshipSlabTab from '@/components/finance/scholarships/ScholarshipSlabTab';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Scholarships Page
 * 
 * Migrated from: Settings > Scholarship Slabs
 * New Location: /config/finance/scholarships
 * Badge: Config
 * 
 * Yearly configuration for scholarship schemes and slabs.
 */
export default function ScholarshipsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Scholarships"
                description="Manage scholarship schemes"
                badge="config"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage scholarships.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Scholarships"
            description="Configure scholarship schemes, slabs, and eligibility criteria"
            badge="config"
            movedFrom="Settings > Scholarship Slabs"
        >
            <ScholarshipSlabTab />
        </ConfigPageTemplate>
    );
}
