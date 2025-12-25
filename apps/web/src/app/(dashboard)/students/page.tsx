'use client';

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Search, Plus } from 'lucide-react';
import { studentService } from '@/utils/student-service';

export default function StudentsPage() {
    const [searchTerm, setSearchTerm] = useState('');

    const { data: students, isLoading } = useQuery({
        queryKey: ['students', searchTerm],
        queryFn: () => studentService.getAll({ search: searchTerm }),
    });

    return (
        <div className="flex-1 space-y-4 p-4 pt-6">
            <div className="flex items-center justify-between space-y-2">
                <h2 className="text-3xl font-bold tracking-tight">Students</h2>
                <div className="flex items-center space-x-2">
                    <Link href="/students/import">
                        <Button>
                            <Plus className="mr-2 h-4 w-4" /> Import Students
                        </Button>
                    </Link>
                </div>
            </div>

            <div className="flex items-center space-x-2">
                <Input
                    placeholder="Search by name or admission no..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="max-w-sm"
                />
                <Button variant="outline" size="sm" className="h-8 w-8 p-0">
                    <Search className="h-4 w-4" />
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Students</CardTitle>
                    <CardDescription>Manage and view student records</CardDescription>
                </CardHeader>
                <CardContent>
                    {isLoading ? (
                        <div className="text-center py-4">Loading students...</div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Admission No</TableHead>
                                    <TableHead>Name</TableHead>
                                    <TableHead>Program</TableHead>
                                    <TableHead>Current Year</TableHead>
                                    <TableHead>Email</TableHead>
                                    <TableHead>Status</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {students?.map((student) => (
                                    <TableRow key={student.id}>
                                        <TableCell className="font-medium">{student.admission_number}</TableCell>
                                        <TableCell>{student.name}</TableCell>
                                        <TableCell>{student.program_name || '-'}</TableCell>
                                        <TableCell>{student.current_year || '-'}</TableCell>
                                        <TableCell>{student.email || '-'}</TableCell>
                                        <TableCell>
                                            <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${student.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                                }`}>
                                                {student.status}
                                            </span>
                                        </TableCell>
                                    </TableRow>
                                ))}
                                {students?.length === 0 && (
                                    <TableRow>
                                        <TableCell colSpan={6} className="text-center py-6 text-muted-foreground">
                                            No students found.
                                        </TableCell>
                                    </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
