"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { FeeHeadMaster } from '@/components/finance/FeeHeadMaster';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Fee Heads Page
 * 
 * Migrated from: Settings > Fee Heads
 * New Location: /config/finance/fee-heads
 * Badge: Config
 * 
 * Yearly configuration for fee categories and amounts.
 */
export default function FeeHeadsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Fee Heads"
                description="Manage fee categories and amounts"
                badge="config"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage fee heads.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Fee Heads"
            description="Configure fee categories, amounts, and payment structures"
            badge="config"
            movedFrom="Settings > Fee Heads"
        >
            <FeeHeadMaster />
        </ConfigPageTemplate>
    );
}
