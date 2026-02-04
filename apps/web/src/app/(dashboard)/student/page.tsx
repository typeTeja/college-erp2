"use client"

import React from 'react';
import { DashboardShell } from '@/components/dashboard/DashboardShell';
import { WidgetCard } from '@/components/dashboard/widgets/WidgetCard';
import { Card, CardContent } from '@/components/ui/card';
import { useAuthStore } from '@/store/use-auth-store';
import { 
    Calendar, BookOpen, CheckCircle, AlertCircle, 
    DollarSign, TrendingUp, Clock, FileText 
} from 'lucide-react';

/**
 * Enrolled Student Dashboard
 * 
 * Purpose: Academic execution & personal progress (Student view)
 * Audience: Enrolled Students
 * Time Horizon: Today / This Week
 * 
 * Allowed Widgets:
 * - Today's timetable
 * - Attendance summary
 * - Internal marks
 * - Assignment status
 * - Exam schedule
 * - Fee alerts
 * - Hostel info (if applicable)
 * 
 * Mental Model: Student Planner, not Admin Panel
 */
export default function EnrolledStudentDashboard() {
    const { user, hasHydrated } = useAuthStore();

    // Check if user is an enrolled student
    const isEnrolledStudent = !!user?.roles.some(r => r === "ENROLLED_STUDENT");

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isEnrolledStudent) {
        return (
            <div className="p-6">
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to view the Student Dashboard.
                        </p>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <DashboardShell
            title="Student Dashboard"
            subtitle="Track your academic progress and stay organized"
            role="Enrolled Student"
        >
            {/* Key Metrics Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard
                    title="Attendance"
                    value="87.5%"
                    status="good"
                    icon={<CheckCircle className="h-5 w-5" />}
                />
                <MetricCard
                    title="Current CGPA"
                    value="8.2"
                    status="good"
                    icon={<TrendingUp className="h-5 w-5" />}
                />
                <MetricCard
                    title="Pending Assignments"
                    value="3"
                    status="warning"
                    icon={<FileText className="h-5 w-5" />}
                />
                <MetricCard
                    title="Fee Status"
                    value="Paid"
                    status="good"
                    icon={<DollarSign className="h-5 w-5" />}
                />
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Today's Timetable */}
                <WidgetCard
                    title="Today's Timetable"
                    description="Tuesday, 4 February 2026"
                >
                    <div className="space-y-2">
                        <ClassItem 
                            time="9:00 - 10:00 AM"
                            subject="Data Structures"
                            faculty="Dr. Sharma"
                            room="Lab 101"
                            status="upcoming"
                        />
                        <ClassItem 
                            time="10:00 - 11:00 AM"
                            subject="Operating Systems"
                            faculty="Prof. Verma"
                            room="Room 205"
                            status="upcoming"
                        />
                        <ClassItem 
                            time="11:30 - 12:30 PM"
                            subject="Database Management"
                            faculty="Dr. Patel"
                            room="Room 301"
                            status="upcoming"
                        />
                        <ClassItem 
                            time="2:00 - 3:00 PM"
                            subject="Computer Networks"
                            faculty="Prof. Singh"
                            room="Room 210"
                            status="upcoming"
                        />
                    </div>
                </WidgetCard>

                {/* Attendance Summary */}
                <WidgetCard
                    title="Attendance Summary"
                    description="Current semester attendance by subject"
                >
                    <div className="space-y-3">
                        <AttendanceBar subject="Data Structures" percentage={92} />
                        <AttendanceBar subject="Operating Systems" percentage={85} />
                        <AttendanceBar subject="Database Management" percentage={88} />
                        <AttendanceBar subject="Computer Networks" percentage={81} status="warning" />
                    </div>
                </WidgetCard>

                {/* Internal Marks */}
                <WidgetCard
                    title="Internal Marks"
                    description="Mid-semester assessment scores"
                >
                    <div className="space-y-3">
                        <MarksBar subject="Data Structures" marks={38} total={40} />
                        <MarksBar subject="Operating Systems" marks={32} total={40} />
                        <MarksBar subject="Database Management" marks={37} total={40} />
                        <MarksBar subject="Computer Networks" marks={35} total={40} />
                    </div>
                </WidgetCard>

                {/* Assignment Status */}
                <WidgetCard
                    title="Assignment Status"
                    description="Pending and upcoming assignments"
                >
                    <div className="space-y-2">
                        <AssignmentItem 
                            title="Data Structures - Binary Trees"
                            dueDate="6 Feb 2026"
                            status="pending"
                        />
                        <AssignmentItem 
                            title="OS - Process Scheduling"
                            dueDate="8 Feb 2026"
                            status="pending"
                        />
                        <AssignmentItem 
                            title="DBMS - SQL Queries"
                            dueDate="10 Feb 2026"
                            status="pending"
                        />
                        <AssignmentItem 
                            title="Networks - TCP/IP Analysis"
                            dueDate="3 Feb 2026"
                            status="submitted"
                        />
                    </div>
                </WidgetCard>
            </div>

            {/* Exam Schedule */}
            <WidgetCard
                title="Upcoming Exams"
                description="Mid-semester and end-semester exam schedule"
            >
                <div className="space-y-2">
                    <ExamItem 
                        subject="Data Structures"
                        date="15 Feb 2026"
                        time="10:00 AM"
                        type="Mid-Sem"
                    />
                    <ExamItem 
                        subject="Operating Systems"
                        date="17 Feb 2026"
                        time="2:00 PM"
                        type="Mid-Sem"
                    />
                    <ExamItem 
                        subject="Database Management"
                        date="19 Feb 2026"
                        time="10:00 AM"
                        type="Mid-Sem"
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

function ClassItem({ time, subject, faculty, room, status }: {
    time: string;
    subject: string;
    faculty: string;
    room: string;
    status: 'completed' | 'ongoing' | 'upcoming';
}) {
    const colors = {
        completed: 'bg-slate-50 border-slate-200',
        ongoing: 'bg-blue-50 border-blue-200',
        upcoming: 'bg-white border-slate-200'
    };
    
    return (
        <div className={`p-3 border rounded-lg ${colors[status]}`}>
            <div className="flex items-start justify-between">
                <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                        <Clock className="h-4 w-4 text-slate-500" />
                        <span className="text-sm font-medium text-slate-900">{time}</span>
                    </div>
                    <h4 className="font-semibold text-slate-900">{subject}</h4>
                    <p className="text-sm text-slate-600">{faculty} • {room}</p>
                </div>
            </div>
        </div>
    );
}

function AttendanceBar({ subject, percentage, status = 'good' }: {
    subject: string;
    percentage: number;
    status?: 'good' | 'warning';
}) {
    const color = status === 'good' ? 'bg-green-600' : 'bg-yellow-600';
    
    return (
        <div>
            <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-700">{subject}</span>
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

function MarksBar({ subject, marks, total }: {
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

function AssignmentItem({ title, dueDate, status }: {
    title: string;
    dueDate: string;
    status: 'pending' | 'submitted' | 'graded';
}) {
    const colors = {
        pending: 'bg-yellow-100 text-yellow-700',
        submitted: 'bg-blue-100 text-blue-700',
        graded: 'bg-green-100 text-green-700'
    };
    
    return (
        <div className="flex items-center justify-between py-2 border-b last:border-0">
            <div className="flex-1">
                <p className="text-sm font-medium text-slate-900">{title}</p>
                <p className="text-xs text-slate-500">Due: {dueDate}</p>
            </div>
            <span className={`text-xs px-2 py-1 rounded-full ${colors[status]}`}>
                {status.charAt(0).toUpperCase() + status.slice(1)}
            </span>
        </div>
    );
}

function ExamItem({ subject, date, time, type }: {
    subject: string;
    date: string;
    time: string;
    type: string;
}) {
    return (
        <div className="flex items-center justify-between py-2 border-b last:border-0">
            <div className="flex items-center gap-3">
                <div className="text-blue-600">
                    <BookOpen className="h-4 w-4" />
                </div>
                <div>
                    <p className="text-sm font-medium text-slate-900">{subject}</p>
                    <p className="text-xs text-slate-500">{type}</p>
                </div>
            </div>
            <div className="text-right">
                <p className="text-sm font-medium text-slate-900">{date}</p>
                <p className="text-xs text-slate-500">{time}</p>
            </div>
        </div>
    );
}
