/**
 * Exam Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import internalExamApi from '@/services/internal-exam-api';
import { queryKeys } from '@/config/react-query';

export function useInternalExams(filters?: {
    program_id?: number;
    year?: number;
    semester?: number;
    exam_type?: string;
    academic_year?: string;
}) {
    return useQuery({
        queryKey: queryKeys.exams.internal.list(filters),
        queryFn: () => internalExamApi.list(filters),
    });
}

export function useInternalExam(id: number, enabled = true) {
    return useQuery({
        queryKey: queryKeys.exams.internal.detail(id),
        queryFn: () => internalExamApi.get(id),
        enabled: enabled && !!id,
    });
}

export function useCreateInternalExam() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: internalExamApi.create,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.exams.internal.all });
        },
    });
}

export function useEnterMarks() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ examId, marks }: { examId: number; marks: any[] }) =>
            internalExamApi.enterMarks(examId, marks),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({
                queryKey: queryKeys.exams.internal.marks(variables.examId)
            });
        },
    });
}

export function usePublishResults() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (examId: number) => internalExamApi.publishResults(examId),
        onSuccess: (_, examId) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.exams.internal.detail(examId) });
        },
    });
}
