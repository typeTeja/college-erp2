'use client';
import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { examService } from '@/utils/exam-service';
import { BulkMarksEntryDTO } from '@/types/exam';

interface StudentMarkEntry {
    student_id: number;
    name: string;
    admission_number: string;
    marks_obtained: number;
    grade?: string;
    remarks?: string;
    is_absent: boolean;
}

export function FacultyMarksEntry() {
    const queryClient = useQueryClient();
    const [selectedExamId, setSelectedExamId] = useState<string>("");
    const [selectedScheduleId, setSelectedScheduleId] = useState<string>("");

    // Local state to hold marks before submission
    const [marksData, setMarksData] = useState<StudentMarkEntry[]>([]);

    const { data: exams } = useQuery({
        queryKey: ['exams'],
        queryFn: () => examService.getExams(),
    });

    const { data: schedules } = useQuery({
        queryKey: ['exam-schedules', selectedExamId],
        queryFn: () => examService.getSchedules(Number(selectedExamId)),
        enabled: !!selectedExamId,
    });

    // Fetch students and populate initial marks data
    const { data: students, isSuccess } = useQuery({
        queryKey: ['exam-students', selectedScheduleId],
        queryFn: () => examService.getEnrolledStudents(Number(selectedScheduleId)),
        enabled: !!selectedScheduleId,
    });

    useEffect(() => {
        if (isSuccess && students) {
            // Initialize form data with 0 marks or fetch existing marks if available (logic simplified here)
            setMarksData(students.map(s => ({
                student_id: s.id,
                name: s.name,
                admission_number: s.admission_number,
                marks_obtained: 0,
                is_absent: false
            })));
        }
    }, [students, isSuccess]);

    const submitMarksMutation = useMutation({
        mutationFn: (data: BulkMarksEntryDTO) => examService.bulkEnterMarks(data),
        onSuccess: () => {
            alert("Marks saved successfully!");
            // Optionally invalidate queries
        },
        onError: () => {
            alert("Failed to save marks.");
        }
    });

    const handleMarkChange = (index: number, field: keyof StudentMarkEntry, value: any) => {
        const newData = [...marksData];
        newData[index] = { ...newData[index], [field]: value };
        setMarksData(newData);
    };

    const handleSubmit = () => {
        if (!selectedScheduleId) return;
        const payload: BulkMarksEntryDTO = {
            exam_schedule_id: Number(selectedScheduleId),
            records: marksData.map(m => ({
                exam_schedule_id: Number(selectedScheduleId),
                student_id: m.student_id,
                marks_obtained: Number(m.marks_obtained),
                is_absent: m.is_absent,
                grade: m.grade,
                remarks: m.remarks
            }))
        };
        submitMarksMutation.mutate(payload);
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold tracking-tight">Enter Marks</h2>
            </div>

            <div className="flex space-x-4">
                <div className="w-[200px]">
                    <Select onValueChange={setSelectedExamId}>
                        <SelectTrigger>
                            <SelectValue placeholder="Select Exam" />
                        </SelectTrigger>
                        <SelectContent>
                            {exams?.map(e => (
                                <SelectItem key={e.id} value={String(e.id)}>{e.name}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>

                <div className="w-[200px]">
                    <Select onValueChange={setSelectedScheduleId} disabled={!selectedExamId}>
                        <SelectTrigger>
                            <SelectValue placeholder="Select Subject" />
                        </SelectTrigger>
                        <SelectContent>
                            {schedules?.map(s => (
                                <SelectItem key={s.id} value={String(s.id)}>{s.subject_name || `Subject ${s.subject_id}`}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Student Marks Entry</CardTitle>
                    <CardDescription>Enter marks for enrolled students</CardDescription>
                </CardHeader>
                <CardContent>
                    {!selectedScheduleId ? (
                        <div className="text-center py-8 text-muted-foreground">
                            Select an exam and subject to enter marks.
                        </div>
                    ) : (
                        <div className="space-y-4">
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Admission No</TableHead>
                                        <TableHead>Student Name</TableHead>
                                        <TableHead>Marks Obtained</TableHead>
                                        <TableHead>Absent?</TableHead>
                                        <TableHead>Remarks</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {marksData.map((student, index) => (
                                        <TableRow key={student.student_id}>
                                            <TableCell>{student.admission_number}</TableCell>
                                            <TableCell>{student.name}</TableCell>
                                            <TableCell>
                                                <Input
                                                    type="number"
                                                    value={student.marks_obtained}
                                                    onChange={(e) => handleMarkChange(index, 'marks_obtained', e.target.value)}
                                                    className="w-24"
                                                />
                                            </TableCell>
                                            <TableCell>
                                                <input
                                                    type="checkbox"
                                                    checked={student.is_absent}
                                                    onChange={(e) => handleMarkChange(index, 'is_absent', e.target.checked)}
                                                    className="h-4 w-4"
                                                />
                                            </TableCell>
                                            <TableCell>
                                                <Input
                                                    value={student.remarks || ''}
                                                    onChange={(e) => handleMarkChange(index, 'remarks', e.target.value)}
                                                    placeholder="Optional"
                                                />
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                    {marksData.length === 0 && (
                                        <TableRow>
                                            <TableCell colSpan={5} className="text-center">No enrolled students found.</TableCell>
                                        </TableRow>
                                    )}
                                </TableBody>
                            </Table>

                            <div className="flex justify-end">
                                <Button onClick={handleSubmit} disabled={submitMarksMutation.isPending || marksData.length === 0}>
                                    {submitMarksMutation.isPending ? 'Saving...' : 'Save Marks'}
                                </Button>
                            </div>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
