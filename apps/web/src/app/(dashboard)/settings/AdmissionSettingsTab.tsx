'use client'

import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { admissionApi } from '@/services/admission-api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { useToast } from '@/hooks/use-toast'
import { Save, Loader2, DollarSign, CreditCard, Mail, MessageSquare, UserPlus, Trash2, AlertTriangle } from 'lucide-react'

export function AdmissionSettingsTab() {
    const { toast } = useToast()
    const queryClient = useQueryClient()

    // Fetch current settings
    const { data: settings, isLoading } = useQuery({
        queryKey: ['admission-settings'],
        queryFn: () => admissionApi.getSettings(),
    })

    const [formData, setFormData] = useState({
        application_fee_enabled: settings?.application_fee_enabled ?? true,
        application_fee_amount: settings?.application_fee_amount ?? 500,
        online_payment_enabled: settings?.online_payment_enabled ?? true,
        offline_payment_enabled: settings?.offline_payment_enabled ?? true,
        send_credentials_email: settings?.send_credentials_email ?? true,
        send_credentials_sms: settings?.send_credentials_sms ?? false,
        auto_create_student_account: settings?.auto_create_student_account ?? true,
        portal_base_url: settings?.portal_base_url ?? 'https://portal.college.edu',
    })

    // Update form data when settings load
    useEffect(() => {
        if (settings) {
            setFormData({
                application_fee_enabled: settings.application_fee_enabled,
                application_fee_amount: settings.application_fee_amount,
                online_payment_enabled: settings.online_payment_enabled,
                offline_payment_enabled: settings.offline_payment_enabled,
                send_credentials_email: settings.send_credentials_email,
                send_credentials_sms: settings.send_credentials_sms,
                auto_create_student_account: settings.auto_create_student_account,
                portal_base_url: settings.portal_base_url,
            })
        }
    }, [settings])

    // Update settings mutation
    const updateMutation = useMutation({
        mutationFn: (data: any) => admissionApi.updateSettings(data),
        onSuccess: () => {
            toast({
                title: "Settings Updated",
                description: "Admission settings have been saved successfully.",
            })
            queryClient.invalidateQueries({ queryKey: ['admission-settings'] })
        },
        onError: (error: any) => {
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to update settings",
                variant: "destructive"
            })
        }
    })

    const cleanupMutation = useMutation({
        mutationFn: () => admissionApi.cleanupTestData(),
        onSuccess: (data) => {
            toast({
                title: "Cleanup Completed",
                description: `Deleted ${data.deleted_count} test applications.`,
            })
        },
        onError: (error: any) => {
            toast({
                title: "Error",
                description: "Failed to run cleanup.",
                variant: "destructive"
            })
        }
    })

    const handleCleanupTestData = () => {
        if (!confirm("Are you sure you want to delete all test data? This cannot be undone.")) return;
        cleanupMutation.mutate();
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        updateMutation.mutate(formData)
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
            </div>
        )
    }

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold text-gray-900">Admission Settings</h2>
                <p className="text-gray-600 mt-1">Configure application fees, payment methods, and notification preferences</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Application Fee Configuration */}
                <Card>
                    <CardHeader>
                        <div className="flex items-center gap-2">
                            <DollarSign className="h-5 w-5 text-blue-600" />
                            <CardTitle>Application Fee Configuration</CardTitle>
                        </div>
                        <CardDescription>
                            Configure whether to charge an application fee and set the amount
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center justify-between">
                            <div className="space-y-0.5">
                                <Label htmlFor="fee-enabled">Enable Application Fee</Label>
                                <p className="text-sm text-gray-500">Charge applicants a fee to submit their application</p>
                            </div>
                            <Switch
                                id="fee-enabled"
                                checked={formData.application_fee_enabled}
                                onCheckedChange={(checked) =>
                                    setFormData({ ...formData, application_fee_enabled: checked })
                                }
                            />
                        </div>

                        {formData.application_fee_enabled && (
                            <div className="space-y-2">
                                <Label htmlFor="fee-amount">Application Fee Amount (₹)</Label>
                                <Input
                                    id="fee-amount"
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    value={formData.application_fee_amount}
                                    onChange={(e) =>
                                        setFormData({ ...formData, application_fee_amount: parseFloat(e.target.value) })
                                    }
                                    className="max-w-xs"
                                />
                                <p className="text-xs text-gray-500">
                                    This amount will be charged to all applicants during the application process
                                </p>
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Payment Methods */}
                <Card>
                    <CardHeader>
                        <div className="flex items-center gap-2">
                            <CreditCard className="h-5 w-5 text-green-600" />
                            <CardTitle>Payment Methods</CardTitle>
                        </div>
                        <CardDescription>
                            Choose which payment methods are available to applicants
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center justify-between">
                            <div className="space-y-0.5">
                                <Label htmlFor="online-payment">Online Payment</Label>
                                <p className="text-sm text-gray-500">Allow applicants to pay via payment gateway</p>
                            </div>
                            <Switch
                                id="online-payment"
                                checked={formData.online_payment_enabled}
                                onCheckedChange={(checked) =>
                                    setFormData({ ...formData, online_payment_enabled: checked })
                                }
                                disabled={!formData.application_fee_enabled}
                            />
                        </div>

                        <div className="flex items-center justify-between">
                            <div className="space-y-0.5">
                                <Label htmlFor="offline-payment">Offline Payment</Label>
                                <p className="text-sm text-gray-500">Allow applicants to pay at college office</p>
                            </div>
                            <Switch
                                id="offline-payment"
                                checked={formData.offline_payment_enabled}
                                onCheckedChange={(checked) =>
                                    setFormData({ ...formData, offline_payment_enabled: checked })
                                }
                                disabled={!formData.application_fee_enabled}
                            />
                        </div>

                        {formData.application_fee_enabled &&
                            !formData.online_payment_enabled &&
                            !formData.offline_payment_enabled && (
                                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                                    <p className="text-sm text-yellow-800">
                                        ⚠️ At least one payment method must be enabled when application fee is active
                                    </p>
                                </div>
                            )}
                    </CardContent>
                </Card>

                {/* Account Creation & Notifications */}
                <Card>
                    <CardHeader>
                        <div className="flex items-center gap-2">
                            <UserPlus className="h-5 w-5 text-purple-600" />
                            <CardTitle>Account Creation & Notifications</CardTitle>
                        </div>
                        <CardDescription>
                            Configure automatic account creation and credential delivery
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center justify-between">
                            <div className="space-y-0.5">
                                <Label htmlFor="auto-create">Auto-Create Student Accounts</Label>
                                <p className="text-sm text-gray-500">Automatically create portal accounts on Quick Apply</p>
                            </div>
                            <Switch
                                id="auto-create"
                                checked={formData.auto_create_student_account}
                                onCheckedChange={(checked) =>
                                    setFormData({ ...formData, auto_create_student_account: checked })
                                }
                            />
                        </div>

                        {formData.auto_create_student_account && (
                            <>
                                <div className="flex items-center justify-between">
                                    <div className="space-y-0.5 flex items-center gap-2">
                                        <Mail className="h-4 w-4 text-gray-500" />
                                        <div>
                                            <Label htmlFor="email-creds">Send Credentials via Email</Label>
                                            <p className="text-sm text-gray-500">Email login credentials to applicants</p>
                                        </div>
                                    </div>
                                    <Switch
                                        id="email-creds"
                                        checked={formData.send_credentials_email}
                                        onCheckedChange={(checked) =>
                                            setFormData({ ...formData, send_credentials_email: checked })
                                        }
                                    />
                                </div>

                                <div className="flex items-center justify-between">
                                    <div className="space-y-0.5 flex items-center gap-2">
                                        <MessageSquare className="h-4 w-4 text-gray-500" />
                                        <div>
                                            <Label htmlFor="sms-creds">Send Credentials via SMS</Label>
                                            <p className="text-sm text-gray-500">SMS login credentials to applicants</p>
                                        </div>
                                    </div>
                                    <Switch
                                        id="sms-creds"
                                        checked={formData.send_credentials_sms}
                                        onCheckedChange={(checked) =>
                                            setFormData({ ...formData, send_credentials_sms: checked })
                                        }
                                    />
                                </div>

                                {formData.send_credentials_sms && (
                                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                                        <p className="text-sm text-blue-800">
                                            ℹ️ SMS gateway must be configured in backend settings for SMS delivery to work
                                        </p>
                                    </div>
                                )}
                            </>
                        )}
                    </CardContent>
                </Card>

                {/* Portal Configuration */}
                <Card>
                    <CardHeader>
                        <CardTitle>Portal Configuration</CardTitle>
                        <CardDescription>
                            Configure student portal settings
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="portal-url">Portal Base URL</Label>
                            <Input
                                id="portal-url"
                                type="url"
                                value={formData.portal_base_url}
                                onChange={(e) =>
                                    setFormData({ ...formData, portal_base_url: e.target.value })
                                }
                                placeholder="https://portal.college.edu"
                            />
                            <p className="text-xs text-gray-500">
                                This URL will be included in notification emails
                            </p>
                        </div>
                    </CardContent>
                </Card>

                {/* Data Cleanup (Admin Only) */}
                <Card className="border-red-200">
                    <CardHeader>
                        <div className="flex items-center gap-2">
                            <Trash2 className="h-5 w-5 text-red-600" />
                            <CardTitle className="text-red-600">Data Cleanup</CardTitle>
                        </div>
                        <CardDescription>
                            Destructive actions for maintaining the system
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-100">
                            <div className="space-y-0.5">
                                <Label className="text-red-900 font-medium">Cleanup Test Data</Label>
                                <p className="text-sm text-red-700">
                                    Soft-delete unpaid applications with "test" in name or email.
                                </p>
                            </div>
                            <Button 
                                type="button" 
                                variant="destructive" 
                                onClick={handleCleanupTestData}
                                disabled={cleanupMutation.isPending}
                            >
                                {cleanupMutation.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : "Run Cleanup"}
                            </Button>
                        </div>
                    </CardContent>
                </Card>

                {/* Save Button */}
                <div className="flex justify-end gap-4">
                    <Button
                        type="submit"
                        disabled={updateMutation.isPending}
                        className="bg-blue-600 hover:bg-blue-700"
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
            </form>
        </div>
    )
}
