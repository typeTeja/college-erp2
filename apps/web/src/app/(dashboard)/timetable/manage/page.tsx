"use client";

import { TimetableBuilder } from "@/components/timetable/TimetableBuilder";

export default function TimetableManagePage() {
    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Manage Timetable</h1>
                    <p className="text-muted-foreground">Schedule classes, assign faculty, and manage rooms.</p>
                </div>
            </div>

            <TimetableBuilder />
        </div>
    );
}
