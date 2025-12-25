'use client';

import React from 'react';
import { useAuthStore } from '@/store/use-auth-store';
import { FacultyAttendancePanel } from '@/components/attendance/FacultyAttendancePanel';
import { StudentAttendanceDashboard } from '@/components/attendance/StudentAttendanceDashboard';
import { Card, CardContent } from "@/components/ui/card";

export default function AttendancePage() {
    const { user } = useAuthStore();

    if (!user) return null;

    if (user.roles.includes('STUDENT')) {
        return <StudentAttendanceDashboard />;
    }

    if (user.roles.some(role => ['FACULTY', 'ADMIN', 'SUPER_ADMIN'].includes(role))) {
        return <FacultyAttendancePanel />;
    }

    return (
        <Card>
            <CardContent className="p-6">
                <div>Access Denied. You do not have permission to view this page.</div>
            </CardContent>
        </Card>
    );
}
