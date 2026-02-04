"use client"

import React from 'react';
import { DashboardShell } from '@/components/dashboard/DashboardShell';
import { WidgetCard } from '@/components/dashboard/widgets/WidgetCard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuthStore } from '@/store/use-auth-store';
import { 
    TrendingUp, TrendingDown, Users, DollarSign, 
    AlertTriangle, CheckCircle, Calendar, Building 
} from 'lucide-react';

/**
 * Principal Dashboard
 * 
 * Purpose: Institutional health & risk (Executive view)
 * Audience: Principal / Management
 * Time Horizon: Month / Semester / Year
 * 
 * Allowed Widgets:
 * - Enrollment trends
 * - Attendance compliance
 * - Detention risk
 * - Fee collection summary
 * - Hostel P&L
 * - High-risk alerts
 * - Pending approvals
 * - Department performance
 * 
 * Mental Model: Boardroom, not Admin Office
 */
export default function PrincipalDashboard() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is Principal or Super Admin
    const isPrincipal = !!user?.roles.some(r => ["SUPER_ADMIN", "PRINCIPAL"].includes(r));

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isPrincipal) {
        return (
            <div className="p-6">
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to view the Principal Dashboard.
                        </p>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <DashboardShell
            title="Principal Dashboard"
            subtitle="Institutional health & strategic overview"
            role="Principal"
        >
            {/* Key Metrics Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard
                    title="Total Enrollment"
                    value="1,234"
                    change="+12%"
                    trend="up"
                    icon={<Users className="h-5 w-5" />}
                />
                <MetricCard
                    title="Fee Collection"
                    value="₹45.2L"
                    change="+8%"
                    trend="up"
                    icon={<DollarSign className="h-5 w-5" />}
                />
                <MetricCard
                    title="Attendance Rate"
                    value="87.5%"
                    change="-2%"
                    trend="down"
                    icon={<CheckCircle className="h-5 w-5" />}
                />
                <MetricCard
                    title="High-Risk Students"
                    value="23"
                    change="+5"
                    trend="down"
                    icon={<AlertTriangle className="h-5 w-5" />}
                />
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Enrollment Trends */}
                <WidgetCard
                    title="Enrollment Trends"
                    description="Year-over-year enrollment by department"
                >
                    <div className="space-y-3">
                        <EnrollmentBar department="Computer Science" current={320} previous={280} />
                        <EnrollmentBar department="Mechanical" current={245} previous={260} />
                        <EnrollmentBar department="Civil" current={180} previous={175} />
                        <EnrollmentBar department="Electrical" current={210} previous={195} />
                    </div>
                </WidgetCard>

                {/* Attendance Compliance */}
                <WidgetCard
                    title="Attendance Compliance"
                    description="Departments meeting 75% threshold"
                >
                    <div className="space-y-3">
                        <ComplianceBar department="Computer Science" percentage={92} />
                        <ComplianceBar department="Mechanical" percentage={78} />
                        <ComplianceBar department="Civil" percentage={85} />
                        <ComplianceBar department="Electrical" percentage={71} status="warning" />
                    </div>
                </WidgetCard>

                {/* Detention Risk */}
                <WidgetCard
                    title="Detention Risk"
                    description="Students at risk of detention (< 75% attendance)"
                >
                    <div className="space-y-2">
                        <RiskItem department="Computer Science" count={8} total={320} />
                        <RiskItem department="Mechanical" count={12} total={245} />
                        <RiskItem department="Civil" count={3} total={180} />
                        <RiskItem department="Electrical" count={15} total={210} />
                    </div>
                </WidgetCard>

                {/* Fee Collection Summary */}
                <WidgetCard
                    title="Fee Collection Summary"
                    description="Current semester collection status"
                >
                    <div className="space-y-4">
                        <div>
                            <div className="flex justify-between text-sm mb-1">
                                <span className="text-slate-600">Collected</span>
                                <span className="font-medium">₹45.2L / ₹60L</span>
                            </div>
                            <div className="w-full bg-slate-200 rounded-full h-2">
                                <div className="bg-green-600 h-2 rounded-full" style={{ width: '75%' }} />
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>
                                <p className="text-slate-600">Pending</p>
                                <p className="text-lg font-semibold">₹14.8L</p>
                            </div>
                            <div>
                                <p className="text-slate-600">Defaulters</p>
                                <p className="text-lg font-semibold text-red-600">45</p>
                            </div>
                        </div>
                    </div>
                </WidgetCard>
            </div>

            {/* Pending Approvals */}
            <WidgetCard
                title="Pending Approvals"
                description="Items requiring your attention"
            >
                <div className="space-y-2">
                    <ApprovalItem type="Leave Request" count={3} priority="low" />
                    <ApprovalItem type="Fee Waiver" count={7} priority="medium" />
                    <ApprovalItem type="Scholarship" count={2} priority="high" />
                    <ApprovalItem type="Admission Appeal" count={1} priority="high" />
                </div>
            </WidgetCard>
        </DashboardShell>
    );
}

// Helper Components

function MetricCard({ title, value, change, trend, icon }: {
    title: string;
    value: string;
    change: string;
    trend: 'up' | 'down';
    icon: React.ReactNode;
}) {
    const isPositive = trend === 'up';
    const TrendIcon = isPositive ? TrendingUp : TrendingDown;
    
    return (
        <Card>
            <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-sm text-slate-600">{title}</p>
                        <p className="text-2xl font-bold mt-1">{value}</p>
                        <div className={`flex items-center gap-1 mt-1 text-sm ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                            <TrendIcon className="h-4 w-4" />
                            <span>{change}</span>
                        </div>
                    </div>
                    <div className="text-slate-400">
                        {icon}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}

function EnrollmentBar({ department, current, previous }: {
    department: string;
    current: number;
    previous: number;
}) {
    const change = current - previous;
    const isPositive = change > 0;
    
    return (
        <div>
            <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-700">{department}</span>
                <span className={`font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                    {current} ({isPositive ? '+' : ''}{change})
                </span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2">
                <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ width: `${(current / 350) * 100}%` }} 
                />
            </div>
        </div>
    );
}

function ComplianceBar({ department, percentage, status = 'good' }: {
    department: string;
    percentage: number;
    status?: 'good' | 'warning';
}) {
    const color = status === 'good' ? 'bg-green-600' : 'bg-yellow-600';
    
    return (
        <div>
            <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-700">{department}</span>
                <span className="font-medium">{percentage}%</span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2">
                <div 
                    className={`${color} h-2 rounded-full`} 
                    style={{ width: `${percentage}%` }} 
                />
            </div>
        </div>
    );
}

function RiskItem({ department, count, total }: {
    department: string;
    count: number;
    total: number;
}) {
    const percentage = ((count / total) * 100).toFixed(1);
    
    return (
        <div className="flex justify-between items-center py-2 border-b last:border-0">
            <span className="text-sm text-slate-700">{department}</span>
            <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-red-600">{count}</span>
                <span className="text-xs text-slate-500">({percentage}%)</span>
            </div>
        </div>
    );
}

function ApprovalItem({ type, count, priority }: {
    type: string;
    count: number;
    priority: 'low' | 'medium' | 'high';
}) {
    const colors = {
        low: 'bg-slate-100 text-slate-700',
        medium: 'bg-yellow-100 text-yellow-700',
        high: 'bg-red-100 text-red-700'
    };
    
    return (
        <div className="flex justify-between items-center py-2 border-b last:border-0">
            <span className="text-sm text-slate-700">{type}</span>
            <div className="flex items-center gap-2">
                <span className={`text-xs px-2 py-1 rounded-full ${colors[priority]}`}>
                    {count} pending
                </span>
            </div>
        </div>
    );
}
