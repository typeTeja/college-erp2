import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Regulation, RegulationCreateData } from "@/types/regulation";

export const regulationService = {
    // Queries
    useRegulations: (programId?: number) => {
        return useQuery({
            queryKey: ["academic", "regulations", programId],
            queryFn: async () => {
                const response = await api.get<Regulation[]>("/academic/regulations", {
                    params: { program_id: programId }
                });
                return response.data;
            }
        });
    },

    useRegulation: (id: number) => {
        return useQuery({
            queryKey: ["academic", "regulation", id],
            queryFn: async () => {
                const response = await api.get<Regulation>(`/academic/regulations/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    // Mutations
    useCreateRegulation: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: RegulationCreateData) => {
                const response = await api.post<Regulation>("/academic/regulations", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "regulations"] });
            }
        });
    },

    useUpdateRegulation: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, data }: { id: number; data: Partial<RegulationCreateData> }) => {
                const response = await api.put<Regulation>(`/academic/regulations/${id}`, data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["academic", "regulations"] });
                queryClient.invalidateQueries({ queryKey: ["academic", "regulation", data.id] });
            }
        });
    },

    useDeleteRegulation: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                await api.delete(`/academic/regulations/${id}`);
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "regulations"] });
            }
        });
    },

    useLockRegulation: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                const response = await api.post<Regulation>(`/academic/regulations/${id}/lock`);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["academic", "regulations"] });
                queryClient.invalidateQueries({ queryKey: ["academic", "regulation", data.id] });
            }
        });
    }
};
