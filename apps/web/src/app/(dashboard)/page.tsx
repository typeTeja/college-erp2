'use client';

import { useDashboardStats, useRecentAdmissions } from '@/lib/queries';
import { useAuthStore } from '@/store/use-auth-store';
import { Users, GraduationCap, FileText, UserCheck } from 'lucide-react';

export default function DashboardPage() {
    const { user } = useAuthStore();
    const { data: stats, isLoading: statsLoading } = useDashboardStats();
    const { data: admissions, isLoading: admissionsLoading } = useRecentAdmissions();

    const statCards = [
        {
            title: 'Total Students',
            value: stats?.totalStudents || 0,
            icon: Users,
            color: 'bg-blue-500',
        },
        {
            title: 'Active Students',
            value: stats?.activeStudents || 0,
            icon: UserCheck,
            color: 'bg-green-500',
        },
        {
            title: 'Total Faculty',
            value: stats?.totalFaculty || 0,
            icon: GraduationCap,
            color: 'bg-purple-500',
        },
        {
            title: 'Pending Admissions',
            value: stats?.pendingAdmissions || 0,
            icon: FileText,
            color: 'bg-orange-500',
        },
    ];

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                <p className="mt-2 text-sm text-gray-600">
                    Welcome back, {user?.email}
                </p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
                {statCards.map((stat) => {
                    const Icon = stat.icon;
                    return (
                        <div
                            key={stat.title}
                            className="relative overflow-hidden rounded-lg bg-white px-4 pb-12 pt-5 shadow sm:px-6 sm:pt-6"
                        >
                            <dt>
                                <div className={`absolute rounded-md ${stat.color} p-3`}>
                                    <Icon className="h-6 w-6 text-white" aria-hidden="true" />
                                </div>
                                <p className="ml-16 truncate text-sm font-medium text-gray-500">
                                    {stat.title}
                                </p>
                            </dt>
                            <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
                                <p className="text-2xl font-semibold text-gray-900">
                                    {statsLoading ? '...' : stat.value}
                                </p>
                            </dd>
                        </div>
                    );
                })}
            </div>

            {/* Recent Admissions */}
            <div className="bg-white shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:px-6">
                    <h3 className="text-lg font-medium leading-6 text-gray-900">
                        Recent Admission Applications
                    </h3>
                    <p className="mt-1 max-w-2xl text-sm text-gray-500">
                        Latest applications submitted to the system
                    </p>
                </div>
                <div className="border-t border-gray-200">
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                                        Name
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                                        Course
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                                        Contact
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                                        Status
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                                        Date
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200 bg-white">
                                {admissionsLoading ? (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-4 text-center text-sm text-gray-500">
                                            Loading...
                                        </td>
                                    </tr>
                                ) : admissions && admissions.length > 0 ? (
                                    admissions.map((admission) => (
                                        <tr key={admission.id}>
                                            <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
                                                {admission.fullName}
                                            </td>
                                            <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
                                                {admission.course.name}
                                            </td>
                                            <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
                                                {admission.email}
                                            </td>
                                            <td className="whitespace-nowrap px-6 py-4 text-sm">
                                                <span
                                                    className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${admission.status === 'PENDING'
                                                        ? 'bg-yellow-100 text-yellow-800'
                                                        : admission.status === 'APPROVED'
                                                            ? 'bg-green-100 text-green-800'
                                                            : 'bg-red-100 text-red-800'
                                                        }`}
                                                >
                                                    {admission.status}
                                                </span>
                                            </td>
                                            <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
                                                {new Date(admission.createdAt).toLocaleDateString()}
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-4 text-center text-sm text-gray-500">
                                            No recent admissions
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}
