'use client';

import { useState } from 'react';
import { toast } from 'sonner';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Users, UserPlus, ArrowRight, CheckCircle2 } from 'lucide-react';
import { studentAssignmentService } from '@/utils/student-assignment-service';
import type { AutoAssignResponse } from '@/types/student-assignment';

interface StudentAssignmentWizardProps {
    batchId: number;
    batchName: string;
    semesterNo: number;
    unassignedCount: number;
    onComplete?: () => void;
}

export function StudentAssignmentWizard({
    batchId,
    batchName,
    semesterNo,
    unassignedCount,
    onComplete
}: StudentAssignmentWizardProps) {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<AutoAssignResponse | null>(null);

    const handleAutoAssign = async () => {
        setLoading(true);
        try {
            const response = await studentAssignmentService.autoAssignToSections({
                batch_id: batchId,
                semester_no: semesterNo
            });

            setResult(response);

            toast.success(
                <div>
                    <div className="font-semibold">{response.message}</div>
                    <div className="text-sm mt-1">
                        Assigned {response.assigned_count} students
                    </div>
                </div>
            );

            if (onComplete) {
                onComplete();
            }
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to assign students');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <Users className="h-5 w-5" />
                    Student Assignment Wizard
                </CardTitle>
                <CardDescription>
                    Automatically assign students to sections for {batchName} - Semester {semesterNo}
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
                {!result ? (
                    <>
                        {/* Status */}
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h4 className="font-semibold text-blue-900">Unassigned Students</h4>
                                    <p className="text-sm text-blue-700 mt-1">
                                        {unassignedCount} students need to be assigned to sections
                                    </p>
                                </div>
                                <Badge variant="secondary" className="text-lg px-4 py-2">
                                    {unassignedCount}
                                </Badge>
                            </div>
                        </div>

                        {/* How it works */}
                        <div className="space-y-3">
                            <h4 className="font-semibold text-gray-700">How Auto-Assignment Works:</h4>
                            <div className="space-y-2 text-sm text-gray-600">
                                <div className="flex items-start gap-2">
                                    <ArrowRight className="h-4 w-4 mt-0.5 text-blue-500" />
                                    <span>Students are sorted by roll number</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <ArrowRight className="h-4 w-4 mt-0.5 text-blue-500" />
                                    <span>Distributed evenly across sections using round-robin</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <ArrowRight className="h-4 w-4 mt-0.5 text-blue-500" />
                                    <span>Section capacity limits are respected</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <ArrowRight className="h-4 w-4 mt-0.5 text-blue-500" />
                                    <span>Complete audit trail is maintained</span>
                                </div>
                            </div>
                        </div>

                        {/* Action */}
                        <div className="flex justify-end gap-3 pt-4 border-t">
                            <Button
                                onClick={handleAutoAssign}
                                disabled={loading || unassignedCount === 0}
                                className="bg-blue-600 hover:bg-blue-700"
                            >
                                <UserPlus className="h-4 w-4 mr-2" />
                                {loading ? 'Assigning...' : 'Auto-Assign Students'}
                            </Button>
                        </div>
                    </>
                ) : (
                    /* Results */
                    <div className="space-y-4">
                        <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
                            <CheckCircle2 className="h-12 w-12 text-green-600 mx-auto mb-3" />
                            <h3 className="text-lg font-semibold text-green-900 mb-2">
                                Assignment Complete!
                            </h3>
                            <p className="text-green-700">
                                {result.message}
                            </p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-white border rounded-lg p-4">
                                <div className="text-2xl font-bold text-green-600">
                                    {result.assigned_count}
                                </div>
                                <div className="text-sm text-gray-600">Students Assigned</div>
                            </div>
                            <div className="bg-white border rounded-lg p-4">
                                <div className="text-2xl font-bold text-gray-600">
                                    {result.unassigned_count}
                                </div>
                                <div className="text-sm text-gray-600">Remaining</div>
                            </div>
                        </div>

                        <div className="flex justify-end">
                            <Button onClick={() => setResult(null)} variant="outline">
                                Assign More
                            </Button>
                        </div>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
