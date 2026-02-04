"use client"

import React from 'react';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { Card, CardContent } from '@/components/ui/card';
import { useAuthStore } from '@/store/use-auth-store';
import { Shield, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';

/**
 * Roles & Permissions Page
 * 
 * New Location: /system/roles
 * Badge: Admin
 * 
 * System-level role and permission management (placeholder for future implementation).
 */
export default function RolesPage() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is super admin
    const isSuperAdmin = !!user?.roles.some(r => r === "SUPER_ADMIN");

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isSuperAdmin) {
        return (
            <ConfigPageTemplate
                title="Roles & Permissions"
                description="Manage roles and permissions"
                badge="admin"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to manage roles and permissions.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Roles & Permissions"
            description="Manage role-based access control and permissions"
            badge="admin"
            actions={
                <Button className="bg-blue-600 hover:bg-blue-700">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Role
                </Button>
            }
        >
            <Card>
                <CardContent className="pt-6">
                    <div className="text-center py-12">
                        <Shield className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-slate-900 mb-2">
                            Role & Permission Management
                        </h3>
                        <p className="text-sm text-slate-500 mb-4">
                            Role and permission management interface will be implemented in a future update.
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
