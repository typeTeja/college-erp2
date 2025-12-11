import React from 'react';
import { useAuthStore } from '@/store/use-auth-store';
import { Users, ClipboardList, Clock, CheckCircle } from 'lucide-react';
import { KPICard } from '@/components/dashboard/KPICard';

export function FacultyDashboard() {
    const { user } = useAuthStore();

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-slate-900 text-2xl font-semibold mb-2">Faculty Dashboard</h1>
                <p className="text-slate-600">Welcome back, {user?.full_name}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Today's Classes"
                    value="4"
                    icon={<Users size={24} />}
                    color="blue"
                />
                <KPICard
                    title="Pending Attendance"
                    value="1 Class"
                    icon={<CheckCircle size={24} />}
                    trend={{ value: 'Mark now', isPositive: false }}
                    color="orange"
                />
                <KPICard
                    title="Assignments to Grade"
                    value="12"
                    icon={<ClipboardList size={24} />}
                    color="purple"
                />
                <KPICard
                    title="Next Lecture"
                    value="10:00 AM"
                    icon={<Clock size={24} />}
                    trend={{ value: 'B.Tech CS - Year 2', isPositive: true }}
                    color="green"
                />
            </div>

            <div className="bg-white rounded-xl border border-slate-200 p-6">
                <h2 className="text-lg font-semibold mb-4">Upcoming Lectures</h2>
                <div className="text-slate-500 text-sm">No lectures scheduled for the rest of the day.</div>
            </div>
        </div>
    );
}
