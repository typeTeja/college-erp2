"use client";

import { FacultySchedule } from "@/components/timetable/FacultySchedule";

export default function FacultyTimetablePage() {
    // TODO: Get real faculty ID from Auth Context
    const MOCK_FACULTY_ID = 1;

    return (
        <div className="p-6">
            <div className="mb-6">
                <h1 className="text-3xl font-bold tracking-tight">Faculty Schedule</h1>
                <p className="text-muted-foreground">View your weekly teaching & duty schedule.</p>
            </div>

            <FacultySchedule facultyId={MOCK_FACULTY_ID} />
        </div>
    );
}
