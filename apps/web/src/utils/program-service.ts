import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Program, ProgramCreateData } from "@/types/program";
import { ProgramType, ProgramStatus } from "@/types/academic-base";

export const programService = {
    // Queries
    usePrograms: (type?: ProgramType, status?: ProgramStatus) => {
        return useQuery({
            queryKey: ["academic", "programs", type, status],
            queryFn: async () => {
                const response = await api.get<Program[]>("/academic/programs", {
                    params: { type, status }
                });
                return response.data;
            }
        });
    },

    useProgram: (id: number) => {
        return useQuery({
            queryKey: ["academic", "program", id],
            queryFn: async () => {
                const response = await api.get<Program>(`/academic/programs/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    // Mutations
    useCreateProgram: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: ProgramCreateData) => {
                const response = await api.post<Program>("/academic/programs", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "programs"] });
            }
        });
    },

    useUpdateProgram: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, data }: { id: number; data: Partial<ProgramCreateData> }) => {
                const response = await api.put<Program>(`/academic/programs/${id}`, data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["academic", "programs"] });
                queryClient.invalidateQueries({ queryKey: ["academic", "program", data.id] });
            }
        });
    },

    useDeleteProgram: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                await api.delete(`/academic/programs/${id}`);
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "programs"] });
            }
        });
    }
};
