import React from 'react';
import { useAuthStore } from '@/store/use-auth-store';
import { useFacultyDashboard } from '@/hooks/use-faculty-dashboard';
import { Users, ClipboardList, Clock, CheckCircle, AlertCircle, BookOpen } from 'lucide-react';
import { KPICard } from '@/components/dashboard/KPICard';
import { DashboardShell } from '@/components/dashboard/DashboardShell';
import { WidgetCard } from '@/components/dashboard/widgets/WidgetCard';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

export function FacultyDashboard() {
    const { user } = useAuthStore();
    const { data, isLoading } = useFacultyDashboard();

    if (isLoading) {
        return (
            <DashboardShell title="Faculty Dashboard" subtitle="Loading your schedule..." role="Faculty">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    {[1, 2, 3, 4].map(i => (
                        <div key={i} className="h-32 bg-slate-100 animate-pulse rounded-xl" />
                    ))}
                </div>
            </DashboardShell>
        );
    }

    if (!data) return null;

    return (
        <DashboardShell
            title="Faculty Dashboard"
            subtitle={`Welcome back, ${user?.full_name || 'Professor'}`}
            role="Faculty"
        >
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Today's Classes"
                    value={data.kpis.classesToday.toString()}
                    icon={<Users size={24} />}
                    color="blue"
                />
                <KPICard
                    title="Pending Attendance"
                    value={`${data.kpis.pendingAttendance} Class`}
                    icon={<CheckCircle size={24} />}
                    trend={{ value: 'Mark now', isPositive: false }}
                    color="orange"
                />
                <KPICard
                    title="Assignments to Grade"
                    value={data.kpis.assignmentsToGrade.toString()}
                    icon={<ClipboardList size={24} />}
                    color="purple"
                />
                <KPICard
                    title="Next Lecture"
                    value={data.kpis.nextLecture}
                    icon={<Clock size={24} />}
                    trend={{ value: data.kpis.nextLectureDetail, isPositive: true }}
                    color="green"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
                {/* Today's Schedule Widget */}
                <WidgetCard title="Today's Schedule" description="Your upcoming classes">
                    <div className="space-y-4">
                        {data.todaysClasses.map((cls) => (
                            <div key={cls.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100">
                                <div className="flex gap-4 items-center">
                                    <div className={`p-2 rounded-lg ${cls.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'}`}>
                                        <BookOpen size={18} />
                                    </div>
                                    <div>
                                        <p className="font-semibold text-slate-900">{cls.subject}</p>
                                        <div className="flex gap-2 text-xs text-slate-500 mt-1">
                                            <span>{cls.time}</span>
                                            <span>•</span>
                                            <span>{cls.room} ({cls.batch})</span>
                                        </div>
                                    </div>
                                </div>
                                {cls.status === 'upcoming' && (
                                    <Button size="sm" variant="outline" className="text-xs h-8">Start Class</Button>
                                )}
                                {cls.status === 'completed' && (
                                    <Badge variant="success" className="bg-green-100 text-green-700 border-green-200">Completed</Badge>
                                )}
                            </div>
                        ))}
                    </div>
                </WidgetCard>

                {/* Assignments & Actions Widget */}
                <div className="space-y-6">
                    {/* Pending Actions */}
                    <WidgetCard title="Action Required" description="Pending tasks">
                        <div className="space-y-3">
                            {data.attendancePending.map((item) => (
                                <div key={item.id} className="flex items-center justify-between p-3 border-l-4 border-orange-500 bg-orange-50 rounded-r-lg">
                                    <div>
                                        <p className="text-sm font-medium text-orange-900">Attendance Pending</p>
                                        <p className="text-xs text-orange-700">{item.subject} • {item.batch}</p>
                                    </div>
                                    <Button size="sm" className="bg-orange-600 hover:bg-orange-700 text-white h-7 text-xs">Mark Now</Button>
                                </div>
                            ))}
                        </div>
                    </WidgetCard>

                    {/* Grading Queue */}
                    <WidgetCard title="Grading Queue" description="Assignments pending review">
                        <div className="space-y-3">
                            {data.assignmentsToGrade.map((assign) => (
                                <div key={assign.id} className="flex justify-between items-center py-2 border-b last:border-0 border-slate-100">
                                    <div>
                                        <p className="text-sm font-medium text-slate-700">{assign.title}</p>
                                        <p className="text-xs text-slate-500">{assign.subject} • Due: {assign.dueDate}</p>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-sm font-semibold text-purple-600">{assign.submitted}/{assign.total}</p>
                                        <p className="text-[10px] text-slate-400">Submitted</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </WidgetCard>
                </div>
            </div>
        </DashboardShell>
    );
}
