import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { LessonPlan, LessonPlanCreate, SyllabusTopic, Question, QuestionBank, PaperGenerateRequest } from "@/types/lesson-plan";

export const lessonService = {
    // Lesson Plans
    useLessonPlans: (subjectId: number) => {
        return useQuery({
            queryKey: ["lesson-plans", subjectId],
            queryFn: async () => {
                const response = await api.get<LessonPlan[]>(`/lesson/plans/subject/${subjectId}`);
                return response.data;
            },
            enabled: !!subjectId
        });
    },

    useCreateLessonPlan: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: LessonPlanCreate) => {
                const response = await api.post<LessonPlan>("/lesson/plans", data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["lesson-plans", data.subject_id] });
            }
        });
    },

    // Syllabus Tracking
    useMarkTopicCompleted: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (topicId: number) => {
                const response = await api.put<SyllabusTopic>(`/lesson/topics/${topicId}/complete`);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["lesson-plans"] });
            }
        });
    },

    // Question Bank
    useQuestionBank: (subjectId: number) => {
        return useQuery({
            queryKey: ["question-bank", subjectId],
            queryFn: async () => {
                const response = await api.get<QuestionBank>(`/lesson/banks/${subjectId}`);
                return response.data;
            },
            enabled: !!subjectId
        });
    },

    useAddQuestion: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: any) => {
                const response = await api.post<Question>("/lesson/questions", data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["question-bank"] });
            }
        });
    },

    // Paper Generation
    useGeneratePaper: () => {
        return useMutation({
            mutationFn: async (data: PaperGenerateRequest) => {
                const response = await api.post("/lesson/generate-paper", data);
                return response.data;
            }
        });
    }
};
