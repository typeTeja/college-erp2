"use client";

import { SubstitutionManager } from "@/components/timetable/SubstitutionManager";

export default function ManageAdjustmentsPage() {
    return (
        <div className="p-6">
            <div className="mb-6">
                <h1 className="text-3xl font-bold tracking-tight">Manage Substitutions</h1>
                <p className="text-muted-foreground">Approve or reject faculty substitution requests.</p>
            </div>

            <SubstitutionManager />
        </div>
    );
}
