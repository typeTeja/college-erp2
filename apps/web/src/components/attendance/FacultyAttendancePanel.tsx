'use client';
import React, { useState } from 'react';
import { toast } from 'sonner';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { attendanceService } from '@/utils/attendance-service';
import { CreateSessionDTO } from '@/types/attendance';
import { useAuthStore } from '@/store/use-auth-store';

import { CreateSessionDialog } from './CreateSessionDialog';

export function FacultyAttendancePanel() {
    const { user } = useAuthStore();
    const queryClient = useQueryClient();
    const [createOpen, setCreateOpen] = useState(false);

    const { data: sessions, isLoading } = useQuery({
        queryKey: ['attendance-sessions'],
        queryFn: () => attendanceService.getSessions(),
    });

    const handleCreateSession = async (data: CreateSessionDTO) => {
        try {
            await attendanceService.createSession(data);
            queryClient.invalidateQueries({ queryKey: ['attendance-sessions'] });
            toast.success("Session created successfully");
        } catch (error) {
            console.error(error);
            toast.error("Failed to create session");
            throw error;
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold tracking-tight">Class Attendance</h2>
                <Button onClick={() => setCreateOpen(true)}>Create New Session</Button>
            </div>

            <CreateSessionDialog
                open={createOpen}
                onClose={() => setCreateOpen(false)}
                onSubmit={handleCreateSession}
            />

            <Card>
                <CardHeader>
                    <CardTitle>Recent Sessions</CardTitle>
                    <CardDescription>View and manage your recent class sessions</CardDescription>
                </CardHeader>
                <CardContent>
                    {isLoading ? (
                        <div className="text-center py-4">Loading sessions...</div>
                    ) : !sessions || sessions.length === 0 ? (
                        <div className="text-center py-8 text-muted-foreground">
                            No sessions found. Create a session to start marking attendance.
                        </div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Date</TableHead>
                                    <TableHead>Subject</TableHead>
                                    <TableHead>Time</TableHead>
                                    <TableHead>Section</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {sessions.map((session) => (
                                    <TableRow key={session.id}>
                                        <TableCell>{session.session_date}</TableCell>
                                        <TableCell>{session.subject?.name || `Subject #${session.subject_id}`}</TableCell>
                                        <TableCell>{session.start_time} - {session.end_time}</TableCell>
                                        <TableCell>{session.section}</TableCell>
                                        <TableCell>{session.status}</TableCell>
                                        <TableCell>
                                            <Button variant="outline" size="sm">
                                                Mark Attendance
                                            </Button>
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
