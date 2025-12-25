'use client';
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { attendanceService } from '@/utils/attendance-service';
import { useAuthStore } from '@/store/use-auth-store';

export function StudentAttendanceDashboard() {
    const { user } = useAuthStore();
    const { data: stats, isLoading } = useQuery({
        queryKey: ['student-attendance-stats', user?.id],
        queryFn: () => attendanceService.getStudentStats(user!.id),
        enabled: !!user?.id,
    });

    if (isLoading) {
        return <div>Loading attendance stats...</div>;
    }

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold tracking-tight">My Attendance</h2>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Classes</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.total_classes || 0}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Present</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-green-600">{stats?.present || 0}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Absent</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-red-600">{stats?.absent || 0}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Percentage</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.attendance_percentage || 0}%</div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
