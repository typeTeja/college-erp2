'use client';
import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { examService } from '@/utils/exam-service';
import { batchService } from '@/utils/batch-service';
import { academicYearService } from '@/utils/academic-year-service';
import { CreateExamDTO, ExamType } from '@/types/exam';
import { toast } from "sonner";
import { formatError } from '@/utils/error-handler';

export function AdminExamPanel() {
    const queryClient = useQueryClient();

    // Selection State
    const [selectedBatchId, setSelectedBatchId] = useState<number | null>(null);

    // Get Active Academic Year
    const { data: currentYear } = academicYearService.useCurrentYear();

    const [newExam, setNewExam] = useState<Partial<CreateExamDTO>>({
        name: '',
        academic_year: currentYear?.year || '',
        batch_semester_id: undefined,
        exam_type: ExamType.MID_TERM,
        start_date: '',
        end_date: '',
    });

    // Queries
    const { data: batches = [] } = batchService.useBatches();

    const { data: semesters = [] } = batchService.useBatchSemesters(selectedBatchId!);

    const { data: exams, isLoading } = useQuery({
        queryKey: ['exams'],
        queryFn: () => examService.getExams(),
    });

    const createExamMutation = useMutation({
        mutationFn: (data: CreateExamDTO) => examService.createExam(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['exams'] });
            toast.success("Exam cycle created successfully");
            setNewExam({
                ...newExam,
                name: '',
                start_date: '',
                end_date: ''
            });
        },
        onError: (err: any) => {
            toast.error(formatError(err));
        }
    });

    const handleCreate = () => {
        if (!newExam.name || !newExam.start_date || !newExam.end_date || !newExam.batch_semester_id) {
            toast.error("Please fill all required fields including Batch Semester");
            return;
        }
        createExamMutation.mutate(newExam as CreateExamDTO);
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold tracking-tight">Exam Management</h2>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Create New Exam Cycle</CardTitle>
                    <CardDescription>Define a new examination period linked to a specific Batch Semester</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                        {/* Selection Controls */}
                        <div className="space-y-2">
                            <Label>Academic Batch</Label>
                            <Select value={selectedBatchId?.toString()} onValueChange={(v) => { setSelectedBatchId(Number(v)); setNewExam({ ...newExam, batch_semester_id: undefined }); }}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Batch" />
                                </SelectTrigger>
                                <SelectContent>
                                    {batches?.map(b => (
                                        <SelectItem key={b.id} value={b.id.toString()}>{b.batch_name} ({b.batch_code})</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="space-y-2">
                            <Label>Semester</Label>
                            <Select
                                value={newExam.batch_semester_id?.toString() || ""}
                                onValueChange={(v) => setNewExam({ ...newExam, batch_semester_id: Number(v) })}
                                disabled={!selectedBatchId}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Semester" />
                                </SelectTrigger>
                                <SelectContent>
                                    {semesters?.map(s => (
                                        <SelectItem key={s.id} value={s.id.toString()}>
                                            Sem {s.semester_number}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="space-y-2">
                            <Label>Exam Name</Label>
                            <Input
                                placeholder="e.g. Fall Mid-Terms"
                                value={newExam.name || ''}
                                onChange={(e) => setNewExam({ ...newExam, name: e.target.value })}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label>Type</Label>
                            <Select
                                value={newExam.exam_type}
                                onValueChange={(v) => setNewExam({ ...newExam, exam_type: v as ExamType })}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Type" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value={ExamType.MID_TERM}>Mid Term</SelectItem>
                                    <SelectItem value={ExamType.FINAL}>Final</SelectItem>
                                    <SelectItem value={ExamType.INTERNAL}>Internal</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="space-y-2">
                            <Label>Start Date</Label>
                            <Input
                                type="date"
                                value={newExam.start_date || ''}
                                onChange={(e) => setNewExam({ ...newExam, start_date: e.target.value })}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label>End Date</Label>
                            <Input
                                type="date"
                                value={newExam.end_date || ''}
                                onChange={(e) => setNewExam({ ...newExam, end_date: e.target.value })}
                            />
                        </div>
                    </div>
                    <Button onClick={handleCreate} disabled={createExamMutation.isPending || !newExam.batch_semester_id}>
                        {createExamMutation.isPending ? 'Creating...' : 'Create Exam'}
                    </Button>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Upcoming Exams</CardTitle>
                </CardHeader>
                <CardContent>
                    {isLoading ? <div>Loading...</div> : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Name</TableHead>
                                    <TableHead>Type</TableHead>
                                    <TableHead>Start Date</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {exams?.map((exam) => (
                                    <TableRow key={exam.id}>
                                        <TableCell>{exam.name}</TableCell>
                                        <TableCell>{exam.exam_type}</TableCell>
                                        <TableCell>{exam.start_date}</TableCell>
                                        <TableCell>{exam.status}</TableCell>
                                        <TableCell>
                                            <Button variant="outline" size="sm">Manage Schedule</Button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
