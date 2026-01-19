'use client'

import { useState } from 'react'
import {
    Shield, ShieldCheck, ShieldAlert, Lock,
    Plus, Search, Info, History, Save, X,
    ChevronRight, AlertCircle
} from 'lucide-react'
import { useRoles, usePermissions, useAuditLogs, useUpdateRole } from '@/hooks/use-roles'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Role, Permission, PermissionGroup, PermissionAuditLog } from '@/types/role'

export default function RoleManagementPage() {
    const [selectedRoleId, setSelectedRoleId] = useState<number | null>(null)
    const [isEditing, setIsEditing] = useState(false)
    const [activeTab, setActiveTab] = useState<'permissions' | 'audit'>('permissions')

    const { data: roles, isLoading: rolesLoading, error: rolesError } = useRoles()
    const { data: permissionGroups, isLoading: permsLoading } = usePermissions()
    const { data: auditLogs } = useAuditLogs()

    const selectedRole = roles?.find((r: Role) => r.id === selectedRoleId)
    const [editedPermissionIds, setEditedPermissionIds] = useState<number[]>([])

    const updateRoleMutation = useUpdateRole(selectedRoleId || 0)

    const handleRoleSelect = (role: Role) => {
        setSelectedRoleId(role.id)
        setEditedPermissionIds(role.permissions.map(p => p.id))
        setIsEditing(false)
    }

    const togglePermission = (id: number) => {
        if (!isEditing) return
        setEditedPermissionIds(prev =>
            prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id]
        )
    }

    const handleSave = async () => {
        if (!selectedRoleId) return
        try {
            await updateRoleMutation.mutateAsync({
                permission_ids: editedPermissionIds
            })
            setIsEditing(false)
        } catch (err) {
            console.error(err)
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 font-outfit">Role Management</h1>
                    <p className="text-slate-500 mt-1">Define access levels and granular permissions for all system users</p>
                </div>
                <Button>
                    <Plus className="w-4 h-4 mr-2" />
                    Create New Role
                </Button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-200px)]">
                {/* Left: Role List */}
                <div className="lg:col-span-4 space-y-4 overflow-y-auto pr-2 scrollbar-hide">
                    <Card>
                        <CardHeader className="pb-3">
                            <CardTitle className="text-lg">System Roles</CardTitle>
                            <CardDescription>Click a role to manage its permissions</CardDescription>
                        </CardHeader>
                        <CardContent className="p-2">
                            <div className="space-y-1">
                                {rolesLoading ? (
                                    [1, 2, 3].map(i => <div key={i} className="h-14 bg-slate-50 animate-pulse rounded-lg" />)
                                ) : roles?.map((role: Role) => (
                                    <button
                                        key={role.id}
                                        onClick={() => handleRoleSelect(role)}
                                        className={`w-full flex items-center justify-between p-3 rounded-lg transition-all ${selectedRoleId === role.id
                                            ? 'bg-blue-50 text-blue-700 border border-blue-100'
                                            : 'hover:bg-slate-50 text-slate-600'
                                            }`}
                                    >
                                        <div className="flex items-center gap-3">
                                            {role.is_system ? <ShieldCheck className="text-blue-600" size={18} /> : <Shield size={18} />}
                                            <div className="text-left">
                                                <p className="text-sm font-semibold">{role.name}</p>
                                                <p className="text-[10px] opacity-70">{role.permissions.length} Permissions</p>
                                            </div>
                                        </div>
                                        {role.is_system && <Lock size={12} className="text-slate-400" />}
                                        <ChevronRight size={16} className={selectedRoleId === role.id ? 'opacity-100' : 'opacity-0'} />
                                    </button>
                                ))}
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-blue-50/50 border-blue-100">
                        <CardContent className="p-4 flex gap-3 text-blue-700">
                            <Info size={20} className="shrink-0" />
                            <p className="text-xs leading-relaxed">
                                <strong>System Roles (🔒)</strong> are core to the ERP and cannot be deleted. Permissions for these roles can be adjusted but with caution.
                            </p>
                        </CardContent>
                    </Card>
                </div>

                {/* Right: Detailed View */}
                <div className="lg:col-span-8 overflow-y-auto">
                    {!selectedRole ? (
                        <Card className="h-full flex items-center justify-center text-center p-12 bg-slate-50/30 border-dashed border-2">
                            <div>
                                <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <Shield className="text-slate-300" size={32} />
                                </div>
                                <h3 className="text-lg font-medium text-slate-900">No Role Selected</h3>
                                <p className="text-slate-500 max-w-[280px]">Select a role from the left panel to view and manage its permissions.</p>
                            </div>
                        </Card>
                    ) : (
                        <div className="space-y-6">
                            {/* Tabs Header */}
                            <div className="flex border-b">
                                <button
                                    onClick={() => setActiveTab('permissions')}
                                    className={`px-6 py-3 text-sm font-medium transition-colors border-b-2 ${activeTab === 'permissions' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
                                >
                                    Permissions Matrix
                                </button>
                                <button
                                    onClick={() => setActiveTab('audit')}
                                    className={`px-6 py-3 text-sm font-medium transition-colors border-b-2 ${activeTab === 'audit' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
                                >
                                    Audit Logs
                                </button>
                            </div>

                            {activeTab === 'permissions' ? (
                                <div className="space-y-6">
                                    <div className="flex justify-between items-center bg-white p-4 rounded-xl border">
                                        <div>
                                            <h2 className="text-xl font-bold text-slate-900 leading-none">{selectedRole.name}</h2>
                                            <p className="text-sm text-slate-500 mt-2">{selectedRole.description || 'System access role'}</p>
                                        </div>
                                        <div className="flex gap-2">
                                            {isEditing ? (
                                                <>
                                                    <Button variant="outline" onClick={() => {
                                                        setIsEditing(false)
                                                        setEditedPermissionIds(selectedRole.permissions.map((p: Permission) => p.id))
                                                    }}>
                                                        <X className="w-4 h-4 mr-2" />
                                                        Cancel
                                                    </Button>
                                                    <Button onClick={handleSave} disabled={updateRoleMutation.isPending}>
                                                        <Save className="w-4 h-4 mr-2" />
                                                        {updateRoleMutation.isPending ? 'Saving...' : 'Save Changes'}
                                                    </Button>
                                                </>
                                            ) : (
                                                <Button variant="outline" onClick={() => setIsEditing(true)}>
                                                    Modify Permissions
                                                </Button>
                                            )}
                                        </div>
                                    </div>

                                    {/* Permission Matrix */}
                                    <div className="space-y-4">
                                        {permissionGroups?.map((group: PermissionGroup) => (
                                            <Card key={group.module} className="overflow-hidden">
                                                <CardHeader className="bg-slate-50/50 py-3">
                                                    <CardTitle className="text-sm font-bold uppercase tracking-wider text-slate-600">
                                                        {group.module} Module
                                                    </CardTitle>
                                                </CardHeader>
                                                <CardContent className="p-0">
                                                    <div className="divide-y">
                                                        {group.permissions.map((perm: Permission) => (
                                                            <div
                                                                key={perm.id}
                                                                className={`flex items-center justify-between p-4 transition-colors ${editedPermissionIds.includes(perm.id) ? 'bg-blue-50/20' : ''
                                                                    }`}
                                                            >
                                                                <div className="flex-1">
                                                                    <p className="text-sm font-medium text-slate-700">{perm.name.split(':')[1].toUpperCase()}</p>
                                                                    <p className="text-xs text-slate-500">{perm.description || `Allows ${perm.name} access`}</p>
                                                                </div>
                                                                <div className="flex items-center gap-4">
                                                                    <div
                                                                        onClick={() => togglePermission(perm.id)}
                                                                        className={`w-12 h-6 rounded-full p-1 cursor-pointer transition-colors duration-200 ease-in-out ${editedPermissionIds.includes(perm.id) ? 'bg-blue-600' : 'bg-slate-200'
                                                                            } ${!isEditing ? 'opacity-50 cursor-not-allowed' : ''}`}
                                                                    >
                                                                        <div className={`w-4 h-4 bg-white rounded-full transition-transform duration-200 ease-in-out ${editedPermissionIds.includes(perm.id) ? 'translate-x-6' : 'translate-x-0'
                                                                            }`} />
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        ))}
                                                    </div>
                                                </CardContent>
                                            </Card>
                                        ))}
                                    </div>
                                </div>
                            ) : (
                                <Card>
                                    <CardContent className="p-0">
                                        <div className="divide-y">
                                            {auditLogs?.filter((l: PermissionAuditLog) => l.role_id === selectedRoleId).map((log: PermissionAuditLog) => (
                                                <div key={log.id} className="p-4 flex gap-4">
                                                    <div className={`p-2 rounded-full h-fit ${log.action === 'ADD_PERMISSION' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                                                        {log.action === 'ADD_PERMISSION' ? <Plus size={16} /> : <X size={16} />}
                                                    </div>
                                                    <div className="flex-1">
                                                        <p className="text-sm text-slate-700">
                                                            <span className="font-bold">{log.actor_name}</span> {log.action === 'ADD_PERMISSION' ? 'added' : 'removed'}{' '}
                                                            <span className="font-mono bg-slate-100 px-1 rounded text-xs">{log.permission_name}</span>
                                                        </p>
                                                        <p className="text-xs text-slate-400 mt-1">{new Date(log.timestamp).toLocaleString()}</p>
                                                    </div>
                                                </div>
                                            ))}
                                            {(!auditLogs || auditLogs.filter((l: PermissionAuditLog) => l.role_id === selectedRoleId).length === 0) && (
                                                <div className="p-12 text-center text-slate-400">
                                                    <History size={32} className="mx-auto mb-2 opacity-20" />
                                                    <p className="text-sm">No audit logs found for this role.</p>
                                                </div>
                                            )}
                                        </div>
                                    </CardContent>
                                </Card>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
