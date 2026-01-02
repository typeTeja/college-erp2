import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Program, ProgramCreateData, ProgramType, ProgramStatus } from "@/types/program";

export const programService = {
    // Queries
    usePrograms: (type?: ProgramType, status?: ProgramStatus) => {
        return useQuery({
            queryKey: ["programs", type, status],
            queryFn: async () => {
                const response = await api.get<Program[]>("/programs/", {
                    params: { type, status }
                });
                return response.data;
            }
        });
    },

    useProgram: (id: number) => {
        return useQuery({
            queryKey: ["program", id],
            queryFn: async () => {
                const response = await api.get<Program>(`/programs/${id}`);
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
                const response = await api.post<Program>("/programs/", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["programs"] });
            }
        });
    },

    useUpdateStructure: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, data }: { id: number; data: any }) => {
                const response = await api.put<Program>(`/programs/${id}/structure`, data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["program", data.id] });
            }
        });
    },

    useDeleteProgram: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                await api.delete(`/programs/${id}`);
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["programs"] });
            }
        });
    }
};
