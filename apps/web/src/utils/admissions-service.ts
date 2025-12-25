import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Application, QuickApplyData, FullApplicationData, ApplicationStatus } from "@/types/admissions";

export const admissionsService = {
    // Queries
    useApplications: (status?: ApplicationStatus) => {
        return useQuery({
            queryKey: ["applications", status],
            queryFn: async () => {
                const response = await api.get<Application[]>("/admissions/", {
                    params: { status }
                });
                return response.data;
            }
        });
    },

    useApplication: (id: number) => {
        return useQuery({
            queryKey: ["application", id],
            queryFn: async () => {
                const response = await api.get<Application>(`/admissions/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    // Mutations
    useQuickApply: () => {
        return useMutation({
            mutationFn: async (data: QuickApplyData) => {
                const response = await api.post<Application>("/admissions/quick-apply", data);
                return response.data;
            }
        });
    },

    useUpdateApplication: (id: number) => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: FullApplicationData) => {
                const response = await api.put<Application>(`/admissions/${id}`, data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["application", id] });
                queryClient.invalidateQueries({ queryKey: ["applications"] });
            }
        });
    },

    useConfirmAdmission: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                const response = await api.post<Application>(`/admissions/${id}/confirm`);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["application", data.id] });
                queryClient.invalidateQueries({ queryKey: ["applications"] });
                queryClient.invalidateQueries({ queryKey: ["students"] });
            }
        });
    }
};
