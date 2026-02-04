"use client"

import React, { useState, useEffect } from 'react';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { toast } from 'sonner';
import { getInstituteInfo, updateInstituteInfo } from '@/utils/institute-service';
import { InstituteInfo } from '@/types/institute';
import { ConfigPageTemplate } from '@/components/layout/ConfigPageTemplate';
import { useAuthStore } from '@/store/use-auth-store';
import { Save } from 'lucide-react';

/**
 * Institute Information Page
 * 
 * Migrated from: Settings > College Details
 * New Location: /setup/institute
 * Badge: Setup
 * 
 * One-time institutional setup for basic college information.
 */
export default function InstitutePage() {
    const { user, hasHydrated } = useAuthStore();
    const [info, setInfo] = useState<InstituteInfo | null>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    // Check if user is admin
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"].includes(r));

    useEffect(() => {
        if (!hasHydrated || !isAdmin) return;
        
        const fetch = async () => {
            try {
                const data = await getInstituteInfo();
                setInfo(data);
            } catch (e) {
                toast.error('Failed to load institute info');
            } finally {
                setLoading(false);
            }
        };
        fetch();
    }, [hasHydrated, isAdmin]);

    const handleChange = (field: keyof InstituteInfo) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        if (info) setInfo({ ...info, [field]: e.target.value });
    };

    const handleSave = async () => {
        if (!info) return;
        setSaving(true);
        try {
            await updateInstituteInfo(info);
            toast.success('Institute information updated successfully');
        } catch (e) {
            toast.error('Failed to update institute information');
        } finally {
            setSaving(false);
        }
    };

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isAdmin) {
        return (
            <ConfigPageTemplate
                title="Institute Information"
                description="Basic institutional details"
                badge="setup"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to view institute settings.
                        </p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    if (loading) {
        return (
            <ConfigPageTemplate
                title="Institute Information"
                description="Basic institutional details"
                badge="setup"
            >
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">Loading...</p>
                    </CardContent>
                </Card>
            </ConfigPageTemplate>
        );
    }

    return (
        <ConfigPageTemplate
            title="Institute Information"
            description="Basic institutional details and contact information"
            badge="setup"
            movedFrom="Settings > College Details"
            actions={
                <Button 
                    onClick={handleSave} 
                    disabled={saving}
                    className="bg-blue-600 hover:bg-blue-700"
                >
                    <Save className="h-4 w-4 mr-2" />
                    {saving ? 'Saving...' : 'Save Changes'}
                </Button>
            }
        >
            <Card>
                <CardContent className="pt-6">
                    <div className="space-y-6">
                        {/* Basic Information */}
                        <div>
                            <h3 className="text-lg font-semibold mb-4">Basic Information</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium mb-1">
                                        Institute Name <span className="text-red-500">*</span>
                                    </label>
                                    <Input 
                                        value={info?.name || ''} 
                                        onChange={handleChange('name')}
                                        placeholder="e.g., ABC Engineering College"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium mb-1">
                                        Short Code <span className="text-red-500">*</span>
                                    </label>
                                    <Input 
                                        value={info?.short_code || ''} 
                                        onChange={handleChange('short_code')}
                                        placeholder="e.g., ABC"
                                        className="uppercase"
                                    />
                                    <p className="text-xs text-slate-500 mt-1">
                                        Used in application numbers and certificates
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Contact Information */}
                        <div>
                            <h3 className="text-lg font-semibold mb-4">Contact Information</h3>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium mb-1">
                                        Address <span className="text-red-500">*</span>
                                    </label>
                                    <Textarea 
                                        value={info?.address || ''} 
                                        onChange={handleChange('address')}
                                        rows={3}
                                        placeholder="Full institutional address"
                                    />
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium mb-1">
                                            Contact Email <span className="text-red-500">*</span>
                                        </label>
                                        <Input 
                                            type="email" 
                                            value={info?.contact_email || ''} 
                                            onChange={handleChange('contact_email')}
                                            placeholder="contact@example.com"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium mb-1">
                                            Contact Phone <span className="text-red-500">*</span>
                                        </label>
                                        <Input 
                                            value={info?.contact_phone || ''} 
                                            onChange={handleChange('contact_phone')}
                                            placeholder="+91 1234567890"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Branding */}
                        <div>
                            <h3 className="text-lg font-semibold mb-4">Branding</h3>
                            <div>
                                <label className="block text-sm font-medium mb-1">
                                    Logo URL
                                </label>
                                <Input 
                                    value={info?.logo_url || ''} 
                                    onChange={handleChange('logo_url')}
                                    placeholder="https://example.com/logo.png"
                                />
                                <p className="text-xs text-slate-500 mt-1">
                                    Used in application forms, certificates, and emails
                                </p>
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </ConfigPageTemplate>
    );
}
