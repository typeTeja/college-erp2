import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Section, PracticalBatch } from "@/types/academic-batch";

export const sectionService = {
    // Queries
    useSections: (batchId?: number, semesterNo?: number) => {
        return useQuery({
            queryKey: ["academic", "sections", batchId, semesterNo],
            queryFn: async () => {
                const response = await api.get<Section[]>("/academic/sections", {
                    params: { batch_id: batchId, semester_no: semesterNo }
                });
                return response.data;
            }
        });
    },

    useSection: (id: number) => {
        return useQuery({
            queryKey: ["academic", "section", id],
            queryFn: async () => {
                const response = await api.get<Section>(`/academic/sections/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    // Mutations
    useCreateSection: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: any) => {
                const response = await api.post<Section>("/academic/sections", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "sections"] });
            }
        });
    },

    /**
     * Update section details
     */
    useUpdateSection: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, data }: { id: number; data: any }) => {
                const response = await api.put<Section>(`/academic/sections/${id}`, data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["academic", "sections"] });
                queryClient.invalidateQueries({ queryKey: ["academic", "section", data.id] });
            }
        });
    },

    useDeleteSection: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                await api.delete(`/academic/sections/${id}`);
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "sections"] });
            }
        });
    },

    // Practical Batches
    usePracticalBatches: (batchId?: number, semesterNo?: number) => {
        return useQuery({
            queryKey: ["academic", "practical-batches", batchId, semesterNo],
            queryFn: async () => {
                const response = await api.get<PracticalBatch[]>("/academic/practical-batches", {
                    params: { batch_id: batchId, semester_no: semesterNo }
                });
                return response.data;
            }
        });
    },

    usePracticalBatch: (id: number) => {
        return useQuery({
            queryKey: ["academic", "practical-batch", id],
            queryFn: async () => {
                const response = await api.get<PracticalBatch>(`/academic/practical-batches/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    useCreatePracticalBatch: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: any) => {
                const response = await api.post<PracticalBatch>("/academic/practical-batches", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "practical-batches"] });
            }
        });
    }
};
