import React from 'react';
import { useAuthStore } from '@/store/use-auth-store';
import { Calendar, BookOpen, Clock, FileCheck } from 'lucide-react';
import { KPICard } from '@/components/dashboard/KPICard';

export function StudentDashboard() {
    const { user } = useAuthStore();

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-slate-900 text-2xl font-semibold mb-2">Student Dashboard</h1>
                <p className="text-slate-600">Welcome back, {user?.full_name}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="My Attendance"
                    value="85%"
                    icon={<Calendar size={24} />}
                    trend={{ value: 'Above requirement', isPositive: true }}
                    color="blue"
                />
                <KPICard
                    title="Assignments"
                    value="3 Pending"
                    icon={<BookOpen size={24} />}
                    color="orange"
                />
                <KPICard
                    title="Next Class"
                    value="DBMS - Lab"
                    icon={<Clock size={24} />}
                    trend={{ value: 'In 10 mins', isPositive: true }}
                    color="green"
                />
                <KPICard
                    title="ODC Events"
                    value="2 New"
                    icon={<FileCheck size={24} />}
                    color="purple"
                />
            </div>

            {/* Timetable or Recent Activity could go here */}
            <div className="bg-white rounded-xl border border-slate-200 p-6">
                <h2 className="text-lg font-semibold mb-4">Today's Schedule</h2>
                <div className="text-slate-500 text-sm">No classes scheduled for today.</div>
            </div>
        </div>
    );
}
