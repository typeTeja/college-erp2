/**
 * Academic Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/utils/api';

const acaApi = {
    getLessonPlans: async (subjectId: number) => {
        const response = await api.get('/academics/lesson-plans', { params: { subject_id: subjectId } });
        return response.data;
    },
    getQuestions: async (subjectId: number) => {
        const response = await api.get('/academics/questions', { params: { subject_id: subjectId } });
        return response.data;
    },
    markTopicCompleted: async (id: number) => {
        const response = await api.post(`/academics/topics/${id}/complete`);
        return response.data;
    },
    createQuestion: async (data: any) => {
        const response = await api.post('/academics/questions', data);
        return response.data;
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
