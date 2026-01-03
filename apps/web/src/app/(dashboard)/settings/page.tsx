"use client"

import React, { useState } from 'react'
import {
    Settings, User, Shield, Building2, Globe,
    Bell, Lock, History, ExternalLink, Save,
    CheckCircle2, AlertCircle, RefreshCcw,
    Calendar, DollarSign, BookOpen, Award, Users, Briefcase, Building, GraduationCap
} from 'lucide-react'
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { InstituteTab } from "./InstituteTab";
import {
    AcademicYearTab,
    AcademicBatchTab,
    FeeHeadTab,
    BoardTab,
    ReservationCategoryTab,
    LeadSourceTab,
    DesignationTab,
    PlacementCompanyTab
} from "./MasterDataTabs";
import { useAuthStore } from "@/store/use-auth-store"
import { settingsService } from "@/utils/settings-service"
import { toast } from "sonner"

export default function SettingsPage() {
    const { user, hasHydrated, setUser } = useAuthStore()
    const [activeTab, setActiveTab] = useState("profile")

    if (!hasHydrated) return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;

    // Role checks
    const isAdmin = !!user?.roles.some(r => ["SUPER_ADMIN", "ADMIN"].includes(r))
    const isSuperAdmin = !!user?.roles.some(r => r === "SUPER_ADMIN")

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6">
            <div className="flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
                        <Settings className="text-slate-600" />
                        Settings & Configuration
                    </h1>
                    <p className="text-slate-500 mt-1">Manage your account and institutional preferences</p>
                </div>
            </div>

            <div className="flex flex-col md:flex-row gap-8">
                {/* Sidebar Navigation */}
                <aside className="w-full md:w-64 space-y-2">
                    <nav className="flex flex-col gap-1">
                        <SettingNavItem
                            icon={<User size={18} />}
                            label="Profile & Account"
                            active={activeTab === 'profile'}
                            onClick={() => setActiveTab('profile')}
                        />
                        <SettingNavItem
                            icon={<Shield size={18} />}
                            label="Security"
                            active={activeTab === 'security'}
                            onClick={() => setActiveTab('security')}
                        />
                        <SettingNavItem
                            icon={<Bell size={18} />}
                            label="Notifications"
                            active={activeTab === 'notifications'}
                            onClick={() => setActiveTab('notifications')}
                        />

                        {(isAdmin || isSuperAdmin) && (
                            <>
                                <div className="pt-4 pb-2 px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                                    Institution Setup
                                </div>
                                <SettingNavItem
                                    icon={<Building2 size={18} />}
                                    label="College Details"
                                    active={activeTab === 'institute'}
                                    onClick={() => setActiveTab('institute')}
                                />

                                <div className="pt-4 pb-2 px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                                    Academic Setup
                                </div>
                                <SettingNavItem
                                    icon={<Calendar size={18} />}
                                    label="Academic Years"
                                    active={activeTab === 'academic-years'}
                                    onClick={() => setActiveTab('academic-years')}
                                />
                                <SettingNavItem
                                    icon={<GraduationCap size={18} />}
                                    label="Academic Batches"
                                    active={activeTab === 'academic-batches'}
                                    onClick={() => setActiveTab('academic-batches')}
                                />

                                <div className="pt-4 pb-2 px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                                    Fee Configuration
                                </div>
                                <SettingNavItem
                                    icon={<DollarSign size={18} />}
                                    label="Fee Heads"
                                    active={activeTab === 'fee-heads'}
                                    onClick={() => setActiveTab('fee-heads')}
                                />

                                <div className="pt-4 pb-2 px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                                    Admission Setup
                                </div>
                                <SettingNavItem
                                    icon={<BookOpen size={18} />}
                                    label="Boards/Universities"
                                    active={activeTab === 'boards'}
                                    onClick={() => setActiveTab('boards')}
                                />
                                <SettingNavItem
                                    icon={<Award size={18} />}
                                    label="Reservation Categories"
                                    active={activeTab === 'reservations'}
                                    onClick={() => setActiveTab('reservations')}
                                />
                                <SettingNavItem
                                    icon={<Users size={18} />}
                                    label="Lead Sources"
                                    active={activeTab === 'lead-sources'}
                                    onClick={() => setActiveTab('lead-sources')}
                                />

                                <div className="pt-4 pb-2 px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                                    Infrastructure
                                </div>
                                <SettingNavItem
                                    icon={<Briefcase size={18} />}
                                    label="Designations"
                                    active={activeTab === 'designations'}
                                    onClick={() => setActiveTab('designations')}
                                />
                                <SettingNavItem
                                    icon={<Building size={18} />}
                                    label="Companies/Hotels"
                                    active={activeTab === 'companies'}
                                    onClick={() => setActiveTab('companies')}
                                />
                            </>
                        )}

                        {isSuperAdmin && (
                            <>
                                <div className="pt-4 pb-2 px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                                    System
                                </div>
                                <SettingNavItem
                                    icon={<Globe size={18} />}
                                    label="Integrations"
                                    active={activeTab === 'integrations'}
                                    onClick={() => setActiveTab('integrations')}
                                />
                                <SettingNavItem
                                    icon={<History size={18} />}
                                    label="Audit Logs"
                                    active={activeTab === 'logs'}
                                    onClick={() => setActiveTab('logs')}
                                />
                            </>
                        )}
                    </nav>
                </aside>

                {/* Main Content Area */}
                <main className="flex-1">
                    {activeTab === 'profile' && <ProfileTab user={user} setUser={setUser} />}
                    {activeTab === 'security' && <SecurityTab />}
                    {activeTab === 'notifications' && <NotificationsTab user={user} setUser={setUser} />}
                    {activeTab === 'institute' && <InstituteTab isAdmin={isAdmin} />}
                    {activeTab === 'academic-years' && <AcademicYearTab />}
                    {activeTab === 'academic-batches' && <AcademicBatchTab />}
                    {activeTab === 'fee-heads' && <FeeHeadTab />}
                    {activeTab === 'boards' && <BoardTab />}
                    {activeTab === 'reservations' && <ReservationCategoryTab />}
                    {activeTab === 'lead-sources' && <LeadSourceTab />}
                    {activeTab === 'designations' && <DesignationTab />}
                    {activeTab === 'companies' && <PlacementCompanyTab />}
                    {activeTab === 'integrations' && <IntegrationsTab isSuperAdmin={isSuperAdmin} />}
                    {activeTab === 'logs' && <AuditLogsTab />}
                </main>
            </div>
        </div>
    )
}

function SettingNavItem({ icon, label, active, onClick }: { icon: any, label: string, active: boolean, onClick: () => void }) {
    return (
        <button
            onClick={onClick}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${active
                ? 'bg-blue-50 text-blue-700 shadow-sm'
                : 'text-slate-600 hover:bg-slate-50'
                }`}
        >
            {icon}
            {label}
        </button>
    )
}

function ProfileTab({ user, setUser }: { user: any, setUser: any }) {
    const [fullName, setFullName] = useState(user?.full_name || "")
    const updateProfile = settingsService.useUpdateProfile()

    const handleSave = async () => {
        try {
            await updateProfile.mutateAsync({ full_name: fullName })
            setUser({ ...user, full_name: fullName })
            toast.success("Profile updated successfully")
        } catch (error) {
            toast.error("Failed to update profile")
        }
    }

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-300">
            <Card>
                <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                        <User className="text-blue-600" size={18} />
                        Personal Information
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center gap-6 pb-6 border-bottom">
                        <div className="w-20 h-20 rounded-full bg-slate-100 flex items-center justify-center border-2 border-dashed border-slate-300">
                            <User size={32} className="text-slate-400" />
                        </div>
                        <div>
                            <Button variant="outline" size="sm" onClick={() => toast.info("Profile picture upload coming soon")}>Change Photo</Button>
                            <p className="text-xs text-slate-500 mt-2">JPG, GIF or PNG. Max size 2MB.</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>Full Name</Label>
                            <Input value={fullName} onChange={(e) => setFullName(e.target.value)} />
                        </div>
                        <div className="space-y-2">
                            <Label>Email Address</Label>
                            <Input defaultValue={user?.email} disabled />
                        </div>
                        <div className="space-y-2">
                            <Label>Employee ID</Label>
                            <Input defaultValue={user?.id} disabled />
                        </div>
                        <div className="space-y-2">
                            <Label>Designated Role</Label>
                            <div className="flex flex-wrap gap-2 mt-1">
                                {user?.roles.map((r: string) => (
                                    <span key={r} className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-[10px] font-bold uppercase tracking-wider">
                                        {r}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="flex justify-end pt-4">
                        <Button
                            className="bg-blue-600 hover:bg-blue-700 gap-2"
                            onClick={handleSave}
                            disabled={updateProfile.isPending}
                        >
                            <Save size={16} />
                            {updateProfile.isPending ? "Saving..." : "Save Profile"}
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

function SecurityTab() {
    const [passwords, setPasswords] = useState({ current: "", new: "", confirm: "" })
    const changePassword = settingsService.useChangePassword()

    const handleUpdate = async () => {
        if (passwords.new !== passwords.confirm) {
            toast.error("New passwords do not match")
            return
        }
        if (passwords.new.length < 8) {
            toast.error("Password must be at least 8 characters")
            return
        }

        try {
            await changePassword.mutateAsync({
                current_password: passwords.current,
                new_password: passwords.new
            })
            toast.success("Password updated successfully")
            setPasswords({ current: "", new: "", confirm: "" })
        } catch (error: any) {
            toast.error(error.response?.data?.detail || "Failed to update password")
        }
    }

    return (
        <Card className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                    <Lock className="text-red-600" size={18} />
                    Password & Security
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="space-y-4">
                    <div className="space-y-2">
                        <Label>Current Password</Label>
                        <Input
                            type="password"
                            placeholder="••••••••"
                            value={passwords.current}
                            onChange={(e) => setPasswords({ ...passwords, current: e.target.value })}
                        />
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>New Password</Label>
                            <Input
                                type="password"
                                placeholder="••••••••"
                                value={passwords.new}
                                onChange={(e) => setPasswords({ ...passwords, new: e.target.value })}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label>Confirm New Password</Label>
                            <Input
                                type="password"
                                placeholder="••••••••"
                                value={passwords.confirm}
                                onChange={(e) => setPasswords({ ...passwords, confirm: e.target.value })}
                            />
                        </div>
                    </div>
                </div>

                <div className="bg-slate-50 p-4 rounded-lg border border-slate-100">
                    <h4 className="text-sm font-semibold flex items-center gap-2 mb-2">
                        <RefreshCcw size={14} />
                        Active Sessions
                    </h4>
                    <p className="text-xs text-slate-500 mb-4">You are currently logged in on this device. You can log out from all other active sessions for security.</p>
                    <Button
                        variant="outline"
                        size="sm"
                        className="text-red-600 border-red-200 hover:bg-red-50"
                        onClick={() => toast.success("Logged out from other devices")}
                    >
                        Log out from all devices
                    </Button>
                </div>

                <div className="flex justify-end pt-2">
                    <Button
                        className="bg-blue-600 hover:bg-blue-700"
                        onClick={handleUpdate}
                        disabled={changePassword.isPending}
                    >
                        {changePassword.isPending ? "Updating..." : "Update Password"}
                    </Button>
                </div>
            </CardContent>
        </Card>
    )
}

function NotificationsTab({ user, setUser }: { user: any, setUser: any }) {
    const [prefs, setPrefs] = useState({
        inApp: user?.preferences?.notifications?.inApp ?? true,
        email: user?.preferences?.notifications?.email ?? true,
        sms: user?.preferences?.notifications?.sms ?? false,
    })
    const updateProfile = settingsService.useUpdateProfile()

    const handleSave = async () => {
        try {
            await updateProfile.mutateAsync({
                preferences: { notifications: prefs }
            })
            setUser({ ...user, preferences: { ...user.preferences, notifications: prefs } })
            toast.success("Preferences saved")
        } catch (error) {
            toast.error("Failed to save preferences")
        }
    }

    return (
        <Card className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                    <Bell className="text-orange-600" size={18} />
                    Notification Preferences
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
                        <div>
                            <p className="text-sm font-semibold">In-App Notifications</p>
                            <p className="text-xs text-slate-500">Enable badges and the notification bell in the top navigation.</p>
                        </div>
                        <Switch
                            checked={prefs.inApp}
                            onCheckedChange={(checked) => setPrefs({ ...prefs, inApp: checked })}
                        />
                    </div>

                    <div className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
                        <div>
                            <p className="text-sm font-semibold">Email Alerts</p>
                            <p className="text-xs text-slate-500">Receive important updates like Fee receipts or Salary slips via email.</p>
                        </div>
                        <Switch
                            checked={prefs.email}
                            onCheckedChange={(checked) => setPrefs({ ...prefs, email: checked })}
                        />
                    </div>

                    <div className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
                        <div>
                            <p className="text-sm font-semibold">SMS Alerts</p>
                            <p className="text-xs text-slate-500">Receive critical notices and attendance alerts via SMS.</p>
                        </div>
                        <Switch
                            checked={prefs.sms}
                            onCheckedChange={(checked) => setPrefs({ ...prefs, sms: checked })}
                        />
                    </div>
                </div>

                <div className="flex justify-end pt-2">
                    <Button
                        className="bg-blue-600 hover:bg-blue-700"
                        onClick={handleSave}
                        disabled={updateProfile.isPending}
                    >
                        {updateProfile.isPending ? "Saving..." : "Save Preferences"}
                    </Button>
                </div>
            </CardContent>
        </Card>
    )
}








function IntegrationsTab({ isSuperAdmin }: { isSuperAdmin: boolean }) {
    const { data: settings } = settingsService.useSettings('INTEGRATION')
    const testMutation = settingsService.useTestConnection()
    const updateSetting = settingsService.useUpdateSetting()
    const [editValues, setEditValues] = useState<Record<number, string>>({})

    if (!isSuperAdmin) return null

    const handleTest = (gateway: string) => {
        toast.promise(testMutation.mutateAsync(gateway), {
            loading: `Testing ${gateway} connection...`,
            success: (data) => data.message,
            error: "Connection failed"
        })
    }

    const handleUpdate = async (id: number, value: string) => {
        try {
            await updateSetting.mutateAsync({ id, data: { value } })
            toast.success("Identity key updated")
            setEditValues({ ...editValues, [id]: "" }) // Clear edit state
        } catch (error) {
            toast.error("Failed to update key")
        }
    }

    return (
        <Card className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                    <Globe className="text-purple-600" size={18} />
                    Third-Party Integrations
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="space-y-6">
                    {/* SMS Gateway */}
                    <div className="p-4 border rounded-lg space-y-4">
                        <div className="flex items-center justify-between">
                            <h4 className="font-semibold flex items-center gap-2">
                                <span className="p-1 px-2 bg-slate-100 rounded text-xs">SMS</span>
                                Msg91 Connection
                            </h4>
                            <Button size="sm" variant="ghost" onClick={() => handleTest('msg91')} className="h-8 text-[10px] font-bold uppercase tracking-wider text-blue-600">
                                Test Connection
                            </Button>
                        </div>
                        <div className="grid grid-cols-1 gap-4">
                            {settings?.filter(s => s.key.includes('msg91')).map(s => (
                                <div key={s.id} className="space-y-2">
                                    <Label className="text-xs text-slate-500">{s.key.split('.').pop()?.replace('_', ' ')}</Label>
                                    <div className="flex gap-2">
                                        <Input
                                            type={editValues[s.id] !== undefined ? "text" : "password"}
                                            value={editValues[s.id] !== undefined ? editValues[s.id] : s.value}
                                            onChange={(e) => setEditValues({ ...editValues, [s.id]: e.target.value })}
                                            className="bg-slate-50"
                                        />
                                        {editValues[s.id] !== undefined ? (
                                            <Button size="sm" onClick={() => handleUpdate(s.id, editValues[s.id])}>Save</Button>
                                        ) : (
                                            <Button variant="outline" size="sm" onClick={() => setEditValues({ ...editValues, [s.id]: s.value })}>Edit</Button>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Email Gateway */}
                    <div className="p-4 border rounded-lg space-y-4">
                        <div className="flex items-center justify-between">
                            <h4 className="font-semibold flex items-center gap-2">
                                <span className="p-1 px-2 bg-slate-100 rounded text-xs">Email</span>
                                Gmail API (Google OAuth)
                            </h4>
                            <Button size="sm" variant="ghost" onClick={() => handleTest('gmail')} className="h-8 text-[10px] font-bold uppercase tracking-wider text-blue-600">
                                Test Connection
                            </Button>
                        </div>
                        <p className="text-xs text-slate-500">Connect your Google workspace account to send notifications, fee reminders, and institutional circulars.</p>
                        <Button variant="outline" size="sm" className="w-full gap-2" onClick={() => toast.info("OAuth redirect coming soon")}>
                            <Globe size={14} />
                            Re-authorize with Google
                        </Button>
                    </div>

                    {/* Payment Gateway */}
                    <div className="p-4 border rounded-lg space-y-4">
                        <div className="flex items-center justify-between">
                            <h4 className="font-semibold flex items-center gap-2">
                                <span className="p-1 px-2 bg-slate-100 rounded text-xs">Payments</span>
                                Easebuzz Integration
                            </h4>
                            <Button size="sm" variant="ghost" onClick={() => handleTest('easebuzz')} className="h-8 text-[10px] font-bold uppercase tracking-wider text-blue-600">
                                Test Connection
                            </Button>
                        </div>
                        <div className="flex gap-4">
                            <div className="flex-1 space-y-2">
                                <Label className="text-[10px] font-bold uppercase text-slate-400">Environment</Label>
                                <Input value="Sandbox (Test)" disabled className="bg-slate-50" />
                            </div>
                            <div className="flex-1 space-y-2">
                                <Label className="text-[10px] font-bold uppercase text-slate-400">Merchant Logo</Label>
                                <div className="h-10 px-3 flex items-center bg-slate-50 rounded border text-xs text-slate-500 italic">Connected</div>
                            </div>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}

function AuditLogsTab() {
    const { data: logs } = settingsService.useAuditLogs()

    return (
        <Card className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-lg flex items-center gap-2">
                    <History className="text-slate-600" size={18} />
                    System Audit Trail
                </CardTitle>
                <Button size="sm" variant="outline" className="h-8 text-xs">Export CSV</Button>
            </CardHeader>
            <CardContent>
                <div className="relative overflow-x-auto rounded-lg border">
                    <table className="w-full text-sm text-left text-slate-500">
                        <thead className="text-xs text-slate-700 uppercase bg-slate-50 border-b">
                            <tr>
                                <th className="px-4 py-3">Timestamp</th>
                                <th className="px-4 py-3">Action</th>
                                <th className="px-4 py-3">Module</th>
                                <th className="px-4 py-3">Description</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y">
                            {logs?.map(log => (
                                <tr key={log.id} className="bg-white hover:bg-slate-50 transition-colors">
                                    <td className="px-4 py-3 text-[10px] whitespace-nowrap">
                                        {new Date(log.timestamp).toLocaleString()}
                                    </td>
                                    <td className="px-4 py-3">
                                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${log.action === 'SETTING_CHANGE' ? 'bg-orange-100 text-orange-700' :
                                            log.action === 'LOGIN' ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-700'
                                            }`}>
                                            {log.action.replace('_', ' ')}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3 font-semibold text-slate-700">{log.module}</td>
                                    <td className="px-4 py-3 line-clamp-1 max-w-[200px]">{log.description}</td>
                                </tr>
                            ))}
                            {(!logs || logs.length === 0) && (
                                <tr>
                                    <td colSpan={4} className="px-4 py-8 text-center text-slate-400 italic">No audit events recorded recently.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </CardContent>
        </Card>
    )
}
