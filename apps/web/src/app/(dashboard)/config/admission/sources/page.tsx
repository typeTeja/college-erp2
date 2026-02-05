"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { LeadSourceMaster } from '@/components/admission/LeadSourceMaster';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Sources Page
 * 
 * Migrated from: Settings > Lead Sources
 * New Location: /config/admission/sources
 * Badge: Config
 * 
 * Yearly configuration for admission lead sources.
 */
export default function SourcesPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Sources"
                description="Manage admission sources"
                badge="config"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage sources.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Sources"
            description="Manage admission lead sources for tracking student inquiries"
            badge="config"
            movedFrom="Settings > Lead Sources"
        >
            <LeadSourceMaster />
        </ConfigPageTemplate>
    );
}
