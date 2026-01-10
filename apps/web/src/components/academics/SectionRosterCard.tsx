'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Users, UserMinus } from 'lucide-react';
import { toast } from 'sonner';
import { studentAssignmentService } from '@/utils/student-assignment-service';
import type { SectionRosterResponse } from '@/types/student-assignment';

interface SectionRosterCardProps {
    sectionId: number;
    onUpdate?: () => void;
}

export function SectionRosterCard({ sectionId, onUpdate }: SectionRosterCardProps) {
    const [roster, setRoster] = useState<SectionRosterResponse | null>(null);
    const [loading, setLoading] = useState(true);

    const fetchRoster = async () => {
        try {
            const data = await studentAssignmentService.getSectionRoster(sectionId);
            setRoster(data);
        } catch (error) {
            toast.error('Failed to load section roster');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRoster();
    }, [sectionId]);

    const handleRemoveStudent = async (assignmentId: number) => {
        if (!confirm('Remove this student from the section?')) return;

        try {
            await studentAssignmentService.deleteAssignment(assignmentId);
            toast.success('Student removed from section');
            fetchRoster();
            if (onUpdate) onUpdate();
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to remove student');
        }
    };

    if (loading) {
        return (
            <Card>
                <CardContent className="p-6">
                    <div className="text-center text-gray-500">Loading roster...</div>
                </CardContent>
            </Card>
        );
    }

    if (!roster) return null;

    const utilizationPercentage = (roster.current_strength / roster.max_strength) * 100;
    const utilizationColor =
        utilizationPercentage >= 90 ? 'text-red-600' :
            utilizationPercentage >= 75 ? 'text-yellow-600' :
                'text-green-600';

    return (
        <Card>
            <CardHeader>
                <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center gap-2">
                        <Users className="h-5 w-5" />
                        Section {roster.section_code} - {roster.section_name}
                    </CardTitle>
                    <div className="flex items-center gap-2">
                        <Badge variant="outline">
                            <span className={utilizationColor}>
                                {roster.current_strength}/{roster.max_strength}
                            </span>
                        </Badge>
                        <Badge variant="secondary">
                            {utilizationPercentage.toFixed(0)}% Full
                        </Badge>
                    </div>
                </div>
            </CardHeader>
            <CardContent>
                {roster.students.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                        No students assigned yet
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th scope="col" className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Student Name
                                    </th>
                                    <th scope="col" className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Admission No.
                                    </th>
                                    <th scope="col" className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Type
                                    </th>
                                    <th scope="col" className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Assigned On
                                    </th>
                                    <th scope="col" className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {roster.students.map((student) => (
                                    <tr key={student.assignment_id}>
                                        <td className="px-4 py-3 text-sm text-gray-900">
                                            {student.student_name}
                                        </td>
                                        <td className="px-4 py-3 text-sm text-gray-600">
                                            {student.admission_number}
                                        </td>
                                        <td className="px-4 py-3">
                                            <span className={`px-2 py-1 text-xs rounded-full ${student.assignment_type === 'AUTO'
                                                    ? 'bg-blue-100 text-blue-700'
                                                    : 'bg-green-100 text-green-700'
                                                }`}>
                                                {student.assignment_type}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3 text-sm text-gray-600">
                                            {new Date(student.assigned_at).toLocaleDateString()}
                                        </td>
                                        <td className="px-4 py-3">
                                            <Button
                                                size="sm"
                                                variant="ghost"
                                                onClick={() => handleRemoveStudent(student.assignment_id)}
                                                className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                            >
                                                <UserMinus className="h-4 w-4" />
                                            </Button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
