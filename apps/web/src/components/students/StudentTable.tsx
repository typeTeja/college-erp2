import React from 'react';
import {
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge'; // Assuming this exists
import { Button } from '@/components/ui/button';
import { Student } from '@/utils/student-service';
import { Edit2, Eye, CheckCircle } from 'lucide-react';

interface StudentTableProps {
    students: Student[];
    isLoading: boolean;
    onVerify?: (id: number) => void;
}

const getStatusColor = (status: string) => {
    switch (status) {
        case 'ACTIVE': return 'default'; // primary
        case 'INACTIVE': return 'destructive';
        case 'ALUMNI': return 'secondary';
        case 'IMPORTED_PENDING_VERIFICATION': return 'outline'; // or warning color if custom
        default: return 'secondary';
    }
};

export const StudentTable: React.FC<StudentTableProps> = ({ students, isLoading, onVerify }) => {
    if (isLoading) {
        return <div className="p-4 text-center">Loading students...</div>;
    }

    if (students.length === 0) {
        return <div className="p-4 text-center text-muted-foreground">No students found.</div>;
    }

    return (
        <div className="rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Admission No</TableHead>
                        <TableHead>Name</TableHead>
                        <TableHead>Program</TableHead>
                        <TableHead>Batch</TableHead>
                        <TableHead>Section</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {students.map((student) => (
                        <TableRow key={student.id}>
                            <TableCell className="font-medium">{student.admission_number}</TableCell>
                            <TableCell>
                                <div>{student.name}</div>
                                <div className="text-xs text-muted-foreground">{student.email}</div>
                            </TableCell>
                            <TableCell>{student.program_code}</TableCell>
                            <TableCell>{student.batch}</TableCell>
                            <TableCell>{student.section}</TableCell>
                            <TableCell>
                                <Badge variant={getStatusColor(student.status) as any}>
                                    {student.status.replace(/_/g, ' ')}
                                </Badge>
                            </TableCell>
                            <TableCell className="text-right flex items-center justify-end gap-1">
                                {student.status === 'IMPORTED_PENDING_VERIFICATION' && onVerify && (
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        onClick={() => onVerify(student.id)}
                                        className="text-green-600 hover:text-green-700 hover:bg-green-50"
                                        title="Verify Student"
                                    >
                                        <CheckCircle className="h-4 w-4" />
                                    </Button>
                                )}
                                <Button variant="ghost" size="icon">
                                    <Eye className="h-4 w-4" />
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
};
