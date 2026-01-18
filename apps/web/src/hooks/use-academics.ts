/**
 * Academic Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const acaApi = {
    getLessonPlans: async (subjectId: number) => {
        const response = await fetch(`/api/v1/academics/lesson-plans?subject_id=${subjectId}`);
        return response.ok ? response.json() : [];
    },
    getQuestions: async (subjectId: number) => {
        const response = await fetch(`/api/v1/academics/questions?subject_id=${subjectId}`);
        return response.ok ? response.json() : { questions: [] };
    },
    markTopicCompleted: async (id: number) => {
        const response = await fetch(`/api/v1/academics/topics/${id}/complete`, { method: 'POST' });
        return response.json();
    },
    createQuestion: async (data: any) => {
        const response = await fetch('/api/v1/academics/questions', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        });
        return response.json();
    }
};

export function useLessonPlans(subjectId: number) {
    return useQuery({
        queryKey: ['academics', 'lesson-plans', subjectId],
        queryFn: () => acaApi.getLessonPlans(subjectId),
        enabled: !!subjectId,
    });
}

export function useQuestionBank(subjectId: number) {
    return useQuery({
        queryKey: ['academics', 'questions', subjectId],
        queryFn: () => acaApi.getQuestions(subjectId),
        enabled: !!subjectId,
    });
}

export function useMarkTopicCompleted() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (id: number) => acaApi.markTopicCompleted(id),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['academics'] }),
    });
}

export function useAddQuestion() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (data: any) => acaApi.createQuestion(data),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['academics'] }),
    });
}
