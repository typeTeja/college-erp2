'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { BatchDetail } from '@/components/academics/BatchDetail';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

export default function BatchDetailPage() {
    const params = useParams();
    const batchId = params.id ? parseInt(params.id as string) : 0;
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Batch Management"
                description="Manage academic batch details"
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
            title="Batch Management"
            description="Manage academic structure and student roster for this batch"
            badge="setup"
        >
            <BatchDetail batchId={batchId} />
        </ConfigPageTemplate>
    );
}
