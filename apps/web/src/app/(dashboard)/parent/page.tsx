"use client"

import React from 'react';
import { DashboardShell } from '@/components/dashboard/DashboardShell';
import { WidgetCard } from '@/components/dashboard/widgets/WidgetCard';
import { Card, CardContent } from '@/components/ui/card';
import { useAuthStore } from '@/store/use-auth-store';
import { 
    User, Calendar, DollarSign, AlertCircle, 
    CheckCircle, BookOpen, TrendingUp, Bell 
} from 'lucide-react';

/**
 * Parent Dashboard
 * 
 * Purpose: Student progress & communication (Parental view)
 * Audience: Parents / Guardians
 * Time Horizon: Today / Week / Month
 * 
 * Allowed Widgets:
 * - Child's attendance
 * - Academic performance
 * - Fee payment status
 * - Upcoming events
 * - Teacher messages
 * - Disciplinary alerts
 * - Hostel updates (if applicable)
 * 
 * Mental Model: Parent-Teacher Meeting, not Admin Panel
 */
export default function ParentDashboard() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is a parent
    const isParent = !!user?.roles.some(r => r === "PARENT");

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isParent) {
        return (
            <div className="p-6">
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to view the Parent Dashboard.
                        </p>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <DashboardShell
            title="Parent Dashboard"
            subtitle="Monitor your child's academic progress and activities"
            role="Parent"
        >
            {/* Student Selector (if multiple children) */}
            <Card className="mb-6">
                <CardContent className="pt-6">
                    <div className="flex items-center gap-4">
                        <User className="h-10 w-10 text-blue-600" />
                        <div>
                            <h3 className="font-semibold text-lg">Rajesh Kumar</h3>
                            <p className="text-sm text-slate-600">B.Tech Computer Science - Semester 3</p>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Key Metrics Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard
                    title="Attendance"
                    value="87.5%"
                    status="good"
                    icon={<CheckCircle className="h-5 w-5" />}
                />
                <MetricCard
                    title="Academic Performance"
                    value="8.2 CGPA"
                    status="good"
                    icon={<TrendingUp className="h-5 w-5" />}
                />
                <MetricCard
                    title="Fee Status"
                    value="Paid"
                    status="good"
                    icon={<DollarSign className="h-5 w-5" />}
                />
                <MetricCard
                    title="Alerts"
                    value="2 New"
                    status="warning"
                    icon={<AlertCircle className="h-5 w-5" />}
                />
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Attendance Overview */}
                <WidgetCard
                    title="Attendance Overview"
                    description="Last 30 days attendance record"
                >
                    <div className="space-y-4">
                        <div>
                            <div className="flex justify-between text-sm mb-1">
                                <span className="text-slate-600">Overall Attendance</span>
                                <span className="font-medium">87.5%</span>
                            </div>
                            <div className="w-full bg-slate-200 rounded-full h-2">
                                <div className="bg-green-600 h-2 rounded-full" style={{ width: '87.5%' }} />
                            </div>
                        </div>
                        <div className="grid grid-cols-3 gap-4 text-sm">
                            <div>
                                <p className="text-slate-600">Present</p>
                                <p className="text-lg font-semibold text-green-600">26 days</p>
                            </div>
                            <div>
                                <p className="text-slate-600">Absent</p>
                                <p className="text-lg font-semibold text-red-600">3 days</p>
                            </div>
                            <div>
                                <p className="text-slate-600">Leave</p>
                                <p className="text-lg font-semibold text-yellow-600">1 day</p>
                            </div>
                        </div>
                    </div>
                </WidgetCard>

                {/* Academic Performance */}
                <WidgetCard
                    title="Academic Performance"
                    description="Current semester subject-wise performance"
                >
                    <div className="space-y-3">
                        <SubjectBar subject="Data Structures" marks={85} total={100} />
                        <SubjectBar subject="Operating Systems" marks={78} total={100} />
                        <SubjectBar subject="Database Management" marks={92} total={100} />
                        <SubjectBar subject="Computer Networks" marks={81} total={100} />
                    </div>
                </WidgetCard>

                {/* Fee Payment Status */}
                <WidgetCard
                    title="Fee Payment Status"
                    description="Current semester fee details"
                >
                    <div className="space-y-4">
                        <div>
                            <div className="flex justify-between text-sm mb-1">
                                <span className="text-slate-600">Paid</span>
                                <span className="font-medium">₹75,000 / ₹75,000</span>
                            </div>
                            <div className="w-full bg-slate-200 rounded-full h-2">
                                <div className="bg-green-600 h-2 rounded-full" style={{ width: '100%' }} />
                            </div>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-green-600">
                            <CheckCircle className="h-4 w-4" />
                            <span>All fees paid for Semester 3</span>
                        </div>
                    </div>
                </WidgetCard>

                {/* Upcoming Events */}
                <WidgetCard
                    title="Upcoming Events"
                    description="Important dates and events"
                >
                    <div className="space-y-2">
                        <EventItem 
                            title="Mid-Semester Exams" 
                            date="15 Feb 2026" 
                            type="exam" 
                        />
                        <EventItem 
                            title="Parent-Teacher Meeting" 
                            date="20 Feb 2026" 
                            type="meeting" 
                        />
                        <EventItem 
                            title="Annual Sports Day" 
                            date="28 Feb 2026" 
                            type="event" 
                        />
                    </div>
                </WidgetCard>
            </div>

            {/* Teacher Messages */}
            <WidgetCard
                title="Recent Messages"
                description="Messages from teachers and administration"
            >
                <div className="space-y-3">
                    <MessageItem 
                        from="Dr. Sharma (HOD CS)"
                        message="Rajesh has shown excellent progress in Data Structures. Keep up the good work!"
                        time="2 days ago"
                    />
                    <MessageItem 
                        from="Prof. Verma (Class Teacher)"
                        message="Please ensure Rajesh completes the pending assignment by Friday."
                        time="5 days ago"
                    />
                </div>
            </WidgetCard>
        </DashboardShell>
    );
}

// Helper Components

function MetricCard({ title, value, status, icon }: {
    title: string;
    value: string;
    status: 'good' | 'warning' | 'danger';
    icon: React.ReactNode;
}) {
    const colors = {
        good: 'text-green-600',
        warning: 'text-yellow-600',
        danger: 'text-red-600'
    };
    
    return (
        <Card>
            <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-sm text-slate-600">{title}</p>
                        <p className={`text-2xl font-bold mt-1 ${colors[status]}`}>{value}</p>
                    </div>
                    <div className={colors[status]}>
                        {icon}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}

function SubjectBar({ subject, marks, total }: {
    subject: string;
    marks: number;
    total: number;
}) {
    const percentage = (marks / total) * 100;
    const color = percentage >= 75 ? 'bg-green-600' : percentage >= 50 ? 'bg-yellow-600' : 'bg-red-600';
    
    return (
        <div>
            <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-700">{subject}</span>
                <span className="font-medium">{marks}/{total}</span>
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

function EventItem({ title, date, type }: {
    title: string;
    date: string;
    type: 'exam' | 'meeting' | 'event';
}) {
    const icons = {
        exam: <BookOpen className="h-4 w-4" />,
        meeting: <User className="h-4 w-4" />,
        event: <Calendar className="h-4 w-4" />
    };
    
    return (
        <div className="flex items-center justify-between py-2 border-b last:border-0">
            <div className="flex items-center gap-2">
                <div className="text-blue-600">
                    {icons[type]}
                </div>
                <span className="text-sm text-slate-700">{title}</span>
            </div>
            <span className="text-xs text-slate-500">{date}</span>
        </div>
    );
}

function MessageItem({ from, message, time }: {
    from: string;
    message: string;
    time: string;
}) {
    return (
        <div className="p-3 bg-slate-50 rounded-lg">
            <div className="flex items-start justify-between mb-1">
                <span className="text-sm font-medium text-slate-900">{from}</span>
                <span className="text-xs text-slate-500">{time}</span>
            </div>
            <p className="text-sm text-slate-600">{message}</p>
        </div>
    );
}
