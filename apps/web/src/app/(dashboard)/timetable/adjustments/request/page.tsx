"use client";

import { SubstitutionRequestForm } from "@/components/timetable/SubstitutionRequestForm";

export default function RequestAdjustmentPage() {
    // TODO: Get from auth context
    const MOCK_FACULTY_ID = 1;

    return (
        <div className="p-6">
            <div className="mb-6">
                <h1 className="text-3xl font-bold tracking-tight">Request Substitution</h1>
                <p className="text-muted-foreground">Submit a request for class adjustment or substitution.</p>
            </div>

            <SubstitutionRequestForm facultyId={MOCK_FACULTY_ID} />
        </div>
    );
}
