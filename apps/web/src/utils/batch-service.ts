import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AcademicBatch, BatchSemester } from "@/types/academic-batch";

export const batchService = {
    // Queries
    useBatches: (programId?: number) => {
        return useQuery({
            queryKey: ["academic", "batches", programId],
            queryFn: async () => {
                const response = await api.get<AcademicBatch[]>("/academic/batches", {
                    params: { program_id: programId }
                });
                return response.data;
            }
        });
    },

    useBatch: (id: number) => {
        return useQuery({
            queryKey: ["academic", "batch", id],
            queryFn: async () => {
                const response = await api.get<AcademicBatch>(`/academic/batches/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    useBatchSemesters: (batchId: number) => {
        return useQuery({
            queryKey: ["academic", "batch-semesters", batchId],
            queryFn: async () => {
                const response = await api.get<BatchSemester[]>(`/academic/batches/${batchId}/semesters`);
                return response.data;
            },
            enabled: !!batchId
        });
    },

    // Mutations
    useCreateBatch: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: any) => {
                const response = await api.post<AcademicBatch>("/academic/batches", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "batches"] });
            }
        });
    },

    useUpdateBatch: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, data }: { id: number; data: any }) => {
                const response = await api.put<AcademicBatch>(`/academic/batches/${id}`, data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["academic", "batches"] });
                queryClient.invalidateQueries({ queryKey: ["academic", "batch", data.id] });
            }
        });
    },

    useDeleteBatch: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                await api.delete(`/academic/batches/${id}`);
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "batches"] });
            }
        });
    },

    useCreateBatchSemester: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: any) => {
                const response = await api.post<BatchSemester>("/academic/batch-semesters", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "batch-semesters"] });
            }
        });
    }
};
