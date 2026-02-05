import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Subject, SubjectCreateData, RegulationSubject } from "@/types/subject";

export const subjectService = {
    // Queries
    useSubjects: () => {
        return useQuery({
            queryKey: ["academic", "subjects"],
            queryFn: async () => {
                const response = await api.get<Subject[]>("/academic/subjects");
                return response.data;
            }
        });
    },

    useSubject: (id: number) => {
        return useQuery({
            queryKey: ["academic", "subject", id],
            queryFn: async () => {
                const response = await api.get<Subject>(`/academic/subjects/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    useRegulationSubjects: (regulationId: number) => {
        return useQuery({
            queryKey: ["academic", "regulation-subjects", regulationId],
            queryFn: async () => {
                const response = await api.get<RegulationSubject[]>(`/academic/regulations/${regulationId}/subjects`);
                return response.data;
            },
            enabled: !!regulationId
        });
    },

    // Mutations
    useCreateSubject: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: SubjectCreateData) => {
                const response = await api.post<Subject>("/academic/subjects", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "subjects"] });
            }
        });
    },

    useUpdateSubject: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, data }: { id: number; data: Partial<SubjectCreateData> }) => {
                const response = await api.put<Subject>(`/academic/subjects/${id}`, data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["academic", "subjects"] });
                queryClient.invalidateQueries({ queryKey: ["academic", "subject", data.id] });
            }
        });
    },

    useDeleteSubject: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                await api.delete(`/academic/subjects/${id}`);
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "subjects"] });
            }
        });
    }
};
