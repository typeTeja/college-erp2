'use client';

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { SubjectMaster } from '@/components/academics/SubjectMaster';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Subjects Page
 * 
 * New Location: /setup/subjects
 * Badge: Setup
 * 
 * Central catalog for all academic subjects/courses.
 * Subjects defined here are later mapped to regulations and semesters.
 */
export default function SubjectsPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Subjects"
                description="Manage central subject catalog"
                badge="setup"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage subjects.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Subjects"
            description="Manage central course catalog and subject definitions"
            badge="setup"
        >
            <SubjectMaster />
        </ConfigPageTemplate>
    );
}
