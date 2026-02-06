"use client"

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { toast } from 'sonner';
import {
    Save,
    CreditCard,
    Mail,
    MessageSquare,
    UserPlus,
    Globe,
    AlertCircle,
    Loader2
} from 'lucide-react';
import { useAdmissionSettings, useUpdateAdmissionSettings } from '@/hooks/use-admissions';
import { AdmissionSettingsUpdate } from '@/types/admissions';

export function AdmissionSettingsTab() {
    const { data: settings, isLoading, isError } = useAdmissionSettings();
    const updateMutation = useUpdateAdmissionSettings();

    const [formState, setFormState] = useState<AdmissionSettingsUpdate>({
        application_fee_enabled: false,
        application_fee_amount: 0,
        online_payment_enabled: false,
        offline_payment_enabled: false,
        send_credentials_email: false,
        send_credentials_sms: false,
        auto_create_student_account: false,
        portal_base_url: '',
    });
    const [isDirty, setIsDirty] = useState(false);

    useEffect(() => {
        if (settings) {
            setFormState({
                application_fee_enabled: settings.application_fee_enabled ?? false,
                application_fee_amount: settings.application_fee_amount ?? 0,
                online_payment_enabled: settings.online_payment_enabled ?? false,
                offline_payment_enabled: settings.offline_payment_enabled ?? false,
                send_credentials_email: settings.send_credentials_email ?? false,
                send_credentials_sms: settings.send_credentials_sms ?? false,
                auto_create_student_account: settings.auto_create_student_account ?? false,
                portal_base_url: settings.portal_base_url ?? '',
            });
        }
    }, [settings]);

    const handleToggle = (field: keyof AdmissionSettingsUpdate) => (checked: boolean) => {
        setFormState(prev => ({ ...prev, [field]: checked }));
        setIsDirty(true);
    };

    const handleInputChange = (field: keyof AdmissionSettingsUpdate) => (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.type === 'number' ? parseFloat(e.target.value) : e.target.value;
        setFormState(prev => ({ ...prev, [field]: value }));
        setIsDirty(true);
    };

    const handleSave = async () => {
        try {
            await updateMutation.mutateAsync(formState);
            toast.success('Admission settings updated successfully');
            setIsDirty(false);
        } catch (error) {
            toast.error('Failed to update settings');
        }
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center p-12">
                <Loader2 className="h-8 w-8 animate-spin text-slate-400" />
            </div>
        );
    }

    if (isError) {
        return (
            <div className="p-6 text-center text-red-500 bg-red-50 rounded-lg">
                <AlertCircle className="h-10 w-10 mx-auto mb-2" />
                <p>Failed to load admission settings. Please try again later.</p>
            </div>
        );
    }

    return (
        <div className="space-y-6 max-w-4xl">
            {/* Application Fee Configuration */}
            <Card>
                <CardHeader>
                    <div className="flex items-center gap-2">
                        <div className="p-2 bg-blue-50 rounded-lg">
                            <CreditCard className="h-5 w-5 text-blue-600" />
                        </div>
                        <div>
                            <CardTitle>Application Fee Configuration</CardTitle>
                            <CardDescription>Configure how application fees are collected from applicants.</CardDescription>
                        </div>
                    </div>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <Label>Enable Application Fee</Label>
                            <p className="text-sm text-slate-500">Require payment before application submission.</p>
                        </div>
                        <Switch
                            checked={formState.application_fee_enabled}
                            onCheckedChange={handleToggle('application_fee_enabled')}
                        />
                    </div>

                    {formState.application_fee_enabled && (
                        <div className="grid gap-2 max-w-sm pt-4 border-t">
                            <Label htmlFor="fee_amount">Application Fee Amount (INR)</Label>
                            <div className="relative">
                                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">₹</span>
                                <Input
                                    id="fee_amount"
                                    type="number"
                                    value={formState.application_fee_amount ?? 0}
                                    onChange={handleInputChange('application_fee_amount')}
                                    className="pl-7"
                                />
                            </div>
                        </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t">
                        <div className="flex items-center justify-between p-3 border rounded-lg">
                            <div className="space-y-0.5">
                                <Label>Online Payment</Label>
                                <p className="text-xs text-slate-500">Allow Easebuzz/Paytm etc.</p>
                            </div>
                            <Switch
                                checked={formState.online_payment_enabled}
                                onCheckedChange={handleToggle('online_payment_enabled')}
                            />
                        </div>
                        <div className="flex items-center justify-between p-3 border rounded-lg">
                            <div className="space-y-0.5">
                                <Label>Offline Payment</Label>
                                <p className="text-xs text-slate-500">Allow Cash/Challan.</p>
                            </div>
                            <Switch
                                checked={formState.offline_payment_enabled}
                                onCheckedChange={handleToggle('offline_payment_enabled')}
                            />
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Notification Settings */}
            <Card>
                <CardHeader>
                    <div className="flex items-center gap-2">
                        <div className="p-2 bg-purple-50 rounded-lg">
                            <Mail className="h-5 w-5 text-purple-600" />
                        </div>
                        <div>
                            <CardTitle>Notification Settings</CardTitle>
                            <CardDescription>Manage how portal credentials are sent to applicants.</CardDescription>
                        </div>
                    </div>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <Mail className="h-4 w-4 text-slate-400" />
                            <Label>Send Credentials via Email</Label>
                        </div>
                        <Switch
                            checked={formState.send_credentials_email}
                            onCheckedChange={handleToggle('send_credentials_email')}
                        />
                    </div>
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <MessageSquare className="h-4 w-4 text-slate-400" />
                            <Label>Send Credentials via SMS</Label>
                        </div>
                        <Switch
                            checked={formState.send_credentials_sms}
                            onCheckedChange={handleToggle('send_credentials_sms')}
                        />
                    </div>
                </CardContent>
            </Card>

            {/* Account & Portal Settings */}
            <Card>
                <CardHeader>
                    <div className="flex items-center gap-2">
                        <div className="p-2 bg-orange-50 rounded-lg">
                            <Globe className="h-5 w-5 text-orange-600" />
                        </div>
                        <div>
                            <CardTitle>Account & Portal Settings</CardTitle>
                            <CardDescription>Configure automated account creation and portal access.</CardDescription>
                        </div>
                    </div>
                </CardHeader>
                <CardContent className="space-y-6">
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <div className="flex items-center gap-2">
                                <UserPlus className="h-4 w-4 text-slate-400" />
                                <Label>Auto-create Student Account</Label>
                            </div>
                            <p className="text-sm text-slate-500">Create portal account instantly upon successful payment.</p>
                        </div>
                        <Switch
                            checked={formState.auto_create_student_account}
                            onCheckedChange={handleToggle('auto_create_student_account')}
                        />
                    </div>

                    <div className="grid gap-2 pt-4 border-t">
                        <Label htmlFor="portal_url">Portal Base URL</Label>
                        <Input
                            id="portal_url"
                            type="url"
                            value={formState.portal_base_url ?? ''}
                            onChange={handleInputChange('portal_base_url')}
                            placeholder="https://portal.yourcollege.edu"
                        />
                        <p className="text-xs text-slate-500">URL used for portal links in emails and SMS.</p>
                    </div>
                </CardContent>
            </Card>

            {/* Actions */}
            <div className="flex justify-end gap-3 pt-4">
                <Button
                    variant="outline"
                    onClick={() => {
                        if (settings) {
                            setFormState({
                                application_fee_enabled: settings.application_fee_enabled ?? false,
                                application_fee_amount: settings.application_fee_amount ?? 0,
                                online_payment_enabled: settings.online_payment_enabled ?? false,
                                offline_payment_enabled: settings.offline_payment_enabled ?? false,
                                send_credentials_email: settings.send_credentials_email ?? false,
                                send_credentials_sms: settings.send_credentials_sms ?? false,
                                auto_create_student_account: settings.auto_create_student_account ?? false,
                                portal_base_url: settings.portal_base_url ?? '',
                            });
                            setIsDirty(false);
                        }
                    }}
                    disabled={!isDirty || updateMutation.isPending}
                >
                    Discard Changes
                </Button>
                <Button
                    className="bg-blue-600 hover:bg-blue-700 min-w-[120px]"
                    onClick={handleSave}
                    disabled={!isDirty || updateMutation.isPending}
                >
                    {updateMutation.isPending ? (
                        <>
                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                            Saving...
                        </>
                    ) : (
                        <>
                            <Save className="h-4 w-4 mr-2" />
                            Save Settings
                        </>
                    )}
                </Button>
            </div>
        </div>
    );
}
