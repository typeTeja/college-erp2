"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { BoardMaster } from '@/components/admission/BoardMaster';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Boards Page
 * 
 * Migrated from: Settings > Boards/Universities
 * New Location: /config/admission/boards
 * Badge: Config
 * 
 * Rare configuration for education boards and universities.
 */
export default function BoardsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Boards"
                description="Manage education boards"
                badge="config"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage boards.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Boards"
            description="Manage education boards and universities for admission eligibility"
            badge="config"
            movedFrom="Settings > Boards/Universities"
        >
            <BoardMaster />
        </ConfigPageTemplate>
    );
}
