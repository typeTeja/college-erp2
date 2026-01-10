'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Users, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import { StudentAssignmentWizard } from '@/components/academics/StudentAssignmentWizard';
import { SectionRosterCard } from '@/components/academics/SectionRosterCard';
import { studentAssignmentService } from '@/utils/student-assignment-service';
import { academicDashboardService } from '@/utils/academic-dashboard-service';
import type { AcademicDashboardResponse } from '@/types/academic-dashboard';

export default function StudentAssignmentPage() {
    const [dashboard, setDashboard] = useState<AcademicDashboardResponse | null>(null);
    const [selectedBatchId, setSelectedBatchId] = useState<number | null>(null);
    const [selectedSemesterNo, setSelectedSemesterNo] = useState<number>(1);
    const [unassignedCount, setUnassignedCount] = useState<number>(0);
    const [loading, setLoading] = useState(true);
    const [showWizard, setShowWizard] = useState(false);

    useEffect(() => {
        fetchDashboard();
    }, []);

    useEffect(() => {
        if (selectedBatchId && selectedSemesterNo) {
            fetchUnassignedCount();
        }
    }, [selectedBatchId, selectedSemesterNo]);

    const fetchDashboard = async () => {
        try {
            const data = await academicDashboardService.getDashboard();
            setDashboard(data);
            if (data.batches.length > 0) {
                setSelectedBatchId(data.batches[0].id);
            }
        } catch (error) {
            toast.error('Failed to load batches');
        } finally {
            setLoading(false);
        }
    };

    const fetchUnassignedCount = async () => {
        if (!selectedBatchId) return;

        try {
            const data = await studentAssignmentService.getUnassignedStudents(
                selectedBatchId,
                selectedSemesterNo
            );
            setUnassignedCount(data.count);
        } catch (error) {
            console.error('Failed to fetch unassigned count:', error);
        }
    };

    const selectedBatch = dashboard?.batches.find(b => b.id === selectedBatchId);
    const selectedYear = selectedBatch?.years.find(y =>
        y.semesters.some(s => s.semester_no === selectedSemesterNo)
    );
    const selectedSemester = selectedYear?.semesters.find(s => s.semester_no === selectedSemesterNo);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="text-lg font-semibold">Loading...</div>
                </div>
            </div>
        );
    }

    if (!dashboard || dashboard.batches.length === 0) {
        return (
            <div className="max-w-4xl mx-auto p-6">
                <Card>
                    <CardContent className="p-12 text-center">
                        <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                            No Batches Found
                        </h3>
                        <p className="text-gray-600">
                            Create a batch first using the Bulk Setup wizard
                        </p>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto p-6 space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold flex items-center gap-2">
                    <Users className="h-8 w-8" />
                    Student Assignment
                </h1>
                <p className="text-gray-600 mt-2">
                    Assign students to sections and manage section rosters
                </p>
            </div>

            {/* Batch & Semester Selection */}
            <Card>
                <CardHeader>
                    <CardTitle>Select Batch & Semester</CardTitle>
                    <CardDescription>
                        Choose the batch and semester to manage student assignments
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <Label htmlFor="batch">Batch</Label>
                            <select
                                id="batch"
                                className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md"
                                value={selectedBatchId || ''}
                                onChange={(e) => setSelectedBatchId(parseInt(e.target.value))}
                            >
                                {dashboard.batches.map((batch) => (
                                    <option key={batch.id} value={batch.id}>
                                        {batch.batch_name} ({batch.batch_code})
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <Label htmlFor="semester">Semester</Label>
                            <select
                                id="semester"
                                className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md"
                                value={selectedSemesterNo}
                                onChange={(e) => setSelectedSemesterNo(parseInt(e.target.value))}
                            >
                                {selectedBatch?.years.flatMap(year =>
                                    year.semesters.map(sem => (
                                        <option key={sem.id} value={sem.semester_no}>
                                            {sem.semester_name}
                                        </option>
                                    ))
                                )}
                            </select>
                        </div>
                    </div>

                    {unassignedCount > 0 && (
                        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <AlertCircle className="h-5 w-5 text-yellow-600" />
                                <span className="text-yellow-900">
                                    <strong>{unassignedCount}</strong> students need to be assigned
                                </span>
                            </div>
                            <Button
                                onClick={() => setShowWizard(!showWizard)}
                                variant={showWizard ? "outline" : "default"}
                            >
                                {showWizard ? 'Hide Wizard' : 'Show Assignment Wizard'}
                            </Button>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Assignment Wizard */}
            {showWizard && selectedBatch && (
                <StudentAssignmentWizard
                    batchId={selectedBatch.id}
                    batchName={selectedBatch.batch_name}
                    semesterNo={selectedSemesterNo}
                    unassignedCount={unassignedCount}
                    onComplete={() => {
                        fetchUnassignedCount();
                        setShowWizard(false);
                    }}
                />
            )}

            {/* Section Rosters */}
            {selectedSemester && (
                <div>
                    <h2 className="text-xl font-semibold mb-4">
                        Section Rosters - {selectedSemester.semester_name}
                    </h2>
                    {selectedSemester.sections.length === 0 ? (
                        <Card>
                            <CardContent className="p-8 text-center text-gray-500">
                                No sections found for this semester
                            </CardContent>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {selectedSemester.sections.map((section) => (
                                <SectionRosterCard
                                    key={section.id}
                                    sectionId={section.id}
                                    onUpdate={fetchUnassignedCount}
                                />
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
