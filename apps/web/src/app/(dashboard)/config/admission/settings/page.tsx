"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { AdmissionSettingsTab } from '@/components/admission/AdmissionSettingsTab';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Admission Settings Page
 * 
 * Migrated from: Settings > Admission Settings
 * New Location: /config/admission/settings
 * Badge: Config
 * 
 * Yearly configuration for admission process settings.
 */
export default function AdmissionSettingsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Admission Settings"
                description="Manage admission process settings"
                badge="config"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage admission settings.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Admission Settings"
            description="Configure admission process, deadlines, and workflow settings"
            badge="config"
            movedFrom="Settings > Admission Settings"
        >
            <AdmissionSettingsTab />
        </ConfigPageTemplate>
    );
}
