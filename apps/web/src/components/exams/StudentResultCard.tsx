'use client';
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { examService } from '@/utils/exam-service';
import { useAuthStore } from '@/store/use-auth-store';

export function StudentResultCard() {
    const { user } = useAuthStore();
    const { data: results, isLoading } = useQuery({
        queryKey: ['student-results', user?.id],
        queryFn: () => examService.getStudentResults(user!.id),
        enabled: !!user?.id,
    });

    if (isLoading) return <div>Loading results...</div>;

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold tracking-tight">My Results</h2>
            <Card>
                <CardHeader>
                    <CardTitle>Exam Performance</CardTitle>
                    <CardDescription>View your grades and marks across all exams</CardDescription>
                </CardHeader>
                <CardContent>
                    {!results || results.length === 0 ? (
                        <div className="text-center py-8 text-muted-foreground">
                            No results published yet.
                        </div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Exam</TableHead>
                                    <TableHead>Subject</TableHead>
                                    <TableHead>Marks</TableHead>
                                    <TableHead>Grade</TableHead>
                                    <TableHead>Remarks</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {results.map((res) => (
                                    <TableRow key={res.id}>
                                        <TableCell>{res.exam_name}</TableCell>
                                        <TableCell>{res.subject_name}</TableCell>
                                        <TableCell>{res.marks_obtained}</TableCell>
                                        <TableCell className="font-bold">{res.grade}</TableCell>
                                        <TableCell>{res.remarks || '-'}</TableCell>
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
