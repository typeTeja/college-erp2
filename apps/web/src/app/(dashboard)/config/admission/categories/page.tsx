"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { ReservationCategoryTab } from '../../../settings/MasterDataTabs';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Categories Page
 * 
 * Migrated from: Settings > Reservation Categories
 * New Location: /config/admission/categories
 * Badge: Config
 * 
 * Rare configuration for student reservation categories.
 */
export default function CategoriesPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Categories"
                description="Manage student categories"
                badge="config"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage categories.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Categories"
            description="Manage student reservation categories (SC, ST, OBC, etc.)"
            badge="config"
            movedFrom="Settings > Reservation Categories"
        >
            <ReservationCategoryTab />
        </ConfigPageTemplate>
    );
}
