import React from 'react';
import { useDashboardStats, useRecentAdmissions } from '@/utils/queries';
import { useAuthStore } from '@/store/use-auth-store';
import { Users, GraduationCap, FileText, UserCheck } from 'lucide-react';
import { KPICard } from '@/components/dashboard/KPICard';

export function AdminDashboard() {
    const { user } = useAuthStore();
    const { data: stats, isLoading: statsLoading } = useDashboardStats();
    const { data: admissions, isLoading: admissionsLoading } = useRecentAdmissions();

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-slate-900 text-2xl font-semibold mb-2">Admin Dashboard</h1>
                <p className="text-slate-600">Welcome back, {user?.full_name}</p>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Total Students"
                    value={statsLoading ? '...' : (stats?.totalStudents || 0)}
                    icon={<Users size={24} />}
                    trend={{ value: '+5.2% from last month', isPositive: true }}
                    color="blue"
                />
                <KPICard
                    title="Active Students"
                    value={statsLoading ? '...' : (stats?.activeStudents || 0)}
                    icon={<UserCheck size={24} />}
                    trend={{ value: '+2.3% this week', isPositive: true }}
                    color="green"
                />
                <KPICard
                    title="Total Faculty"
                    value={statsLoading ? '...' : (stats?.totalFaculty || 0)}
                    icon={<GraduationCap size={24} />}
                    trend={{ value: '+2 new this month', isPositive: true }}
                    color="purple"
                />
                <KPICard
                    title="Pending Admissions"
                    value={statsLoading ? '...' : (stats?.pendingAdmissions || 0)}
                    icon={<FileText size={24} />}
                    trend={{ value: '12 pending review', isPositive: false }}
                    color="orange"
                />
            </div>

            {/* Recent Admissions Table */}
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
                <div className="px-6 py-5 border-b border-slate-200">
                    <h3 className="text-lg font-semibold text-slate-900">
                        Recent Admission Applications
                    </h3>
                    <p className="mt-1 text-sm text-slate-600">
                        Latest applications submitted to the system
                    </p>
                </div>
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-slate-200">
                        <thead className="bg-slate-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">
                                    Name
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">
                                    Course
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">
                                    Contact
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">
                                    Status
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">
                                    Date
                                </th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-200 bg-white">
                            {admissionsLoading ? (
                                <tr>
                                    <td colSpan={5} className="px-6 py-4 text-center text-sm text-slate-500">
                                        Loading...
                                    </td>
                                </tr>
                            ) : admissions && admissions.length > 0 ? (
                                admissions.map((admission: any) => (
                                    <tr key={admission.id} className="hover:bg-slate-50 transition-colors">
                                        <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-slate-900">
                                            {admission.fullName}
                                        </td>
                                        <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-600">
                                            {admission.course?.name || 'N/A'}
                                        </td>
                                        <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-600">
                                            {admission.email}
                                        </td>
                                        <td className="whitespace-nowrap px-6 py-4 text-sm">
                                            <span
                                                className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${admission.status === 'PENDING'
                                                    ? 'bg-yellow-100 text-yellow-800'
                                                    : admission.status === 'APPROVED'
                                                        ? 'bg-green-100 text-green-800'
                                                        : 'bg-red-100 text-red-800'
                                                    }`}
                                            >
                                                {admission.status}
                                            </span>
                                        </td>
                                        <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-600">
                                            {new Date(admission.createdAt).toLocaleDateString()}
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={5} className="px-6 py-4 text-center text-sm text-slate-500">
                                        No recent admissions
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
