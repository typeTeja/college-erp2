"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Student, StudentListResponse, studentService } from '@/utils/student-service';
import { StudentTable } from '@/components/students/StudentTable';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Plus, Upload } from 'lucide-react';

export default function StudentsPage() {
    const router = useRouter();
    const [data, setData] = useState<StudentListResponse | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Filters
    const [search, setSearch] = useState('');
    const [page, setPage] = useState(1);

    // Debounce search
    useEffect(() => {
        const timer = setTimeout(() => {
            fetchStudents();
        }, 500);
        return () => clearTimeout(timer);
    }, [search, page]);

    const fetchStudents = async () => {
        setIsLoading(true);
        try {
            const result = await studentService.getStudents({
                page,
                limit: 10,
                search: search || undefined
            });
            setData(result);
        } catch (error) {
            console.error('Failed to fetch students', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleVerify = async (id: number) => {
        try {
            await studentService.verifyStudent(id);
            // Refresh list or update local state
            fetchStudents();
        } catch (error) {
            console.error('Failed to verify student', error);
            alert("Failed to verify student. Ensure you have permission.");
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Students</h1>
                    <p className="text-muted-foreground">Manage student records and admissions.</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" onClick={() => router.push('/students/import')}>
                        <Upload className="mr-2 h-4 w-4" />
                        Import Bulk
                    </Button>
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Student
                    </Button>
                </div>
            </div>

            {/* Filters */}
            <div className="flex items-center gap-4">
                <Input
                    placeholder="Search by Name or Admission No..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="max-w-sm"
                />
                {/* Future: Add Program/Batch Dropdowns here */}
            </div>

            {/* Table */}
            <StudentTable
                students={data?.items || []}
                isLoading={isLoading}
                onVerify={handleVerify}
            />

            {/* Pagination Controls */}
            {data && (
                <div className="flex items-center justify-end gap-2">
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setPage(p => Math.max(1, p - 1))}
                        disabled={page === 1 || isLoading}
                    >
                        Previous
                    </Button>
                    <span className="text-sm">
                        Page {data.page} of {Math.ceil(data.total / data.limit)}
                    </span>
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setPage(p => p + 1)}
                        disabled={!data.items.length || page * data.limit >= data.total || isLoading}
                    >
                        Next
                    </Button>
                </div>
            )}
        </div>
    );
}
