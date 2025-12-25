'use client';
import { useAuthStore } from '@/store/use-auth-store';
import { AdminExamPanel } from '@/components/exams/AdminExamPanel';
import { FacultyMarksEntry } from '@/components/exams/FacultyMarksEntry';
import { StudentResultCard } from '@/components/exams/StudentResultCard';

export default function ExamsPage() {
    const { user } = useAuthStore();

    // Safety check
    if (!user) return <div>Access Denied</div>;

    const isAdmin = user.roles.some((r: string) => ['ADMIN', 'SUPER_ADMIN'].includes(r));
    const isFaculty = user.roles.includes('FACULTY');
    const isStudent = user.roles.includes('STUDENT');

    return (
        <div className="flex-1 space-y-4 p-4 pt-6">
            <div className="flex items-center justify-between space-y-2">
                <h2 className="text-3xl font-bold tracking-tight">Examinations</h2>
            </div>

            <div className="space-y-4">
                {isAdmin && (
                    <div className="border-b pb-4 mb-4">
                        <AdminExamPanel />
                    </div>
                )}

                {isFaculty && (
                    <div className="border-b pb-4 mb-4">
                        <FacultyMarksEntry />
                    </div>
                )}

                {isStudent && (
                    <StudentResultCard />
                )}
            </div>
        </div>
    );
}
