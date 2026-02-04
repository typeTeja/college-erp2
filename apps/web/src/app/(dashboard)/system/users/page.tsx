"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { Card, CardContent } from '@/components/ui/card';
import { useAuthStore } from '@/store/use-auth-store';
import { Users, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';

/**
 * Users Page
 * 
 * New Location: /system/users
 * Badge: Admin
 * 
 * System-level user management (placeholder for future implementation).
 */
export default function UsersPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is super admin
    const isSuperAdmin = !!user?.roles.some(r => r === "SUPER_ADMIN");

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isSuperAdmin) {
        return (
            <ConfigPageTemplate
                title="Users"
                description="Manage system users"
                badge="admin"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage users.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Users"
            description="Manage system users and their access"
            badge="admin"
            actions={
                <Button className="bg-blue-600 hover:bg-blue-700">
                    <Plus className="h-4 w-4 mr-2" />
                    Add User
                </Button>
            }
        >
            <Card>
                <CardContent className="pt-6">
                    <div className="text-center py-12">
                        <Users className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-slate-900 mb-2">
                            User Management
                        </h3>
                        <p className="text-sm text-slate-500 mb-4">
                            User management interface will be implemented in a future update.
                        </p>
                        <p className="text-xs text-slate-400">
                            This is a placeholder page for the frontend architecture overhaul.
                        </p>
                    </div>
                </CardContent>
            </Card>
        </ConfigPageTemplate>
    );
}
