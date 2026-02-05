import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AcademicYear, AcademicYearCreateData, AcademicYearStatus } from "@/types/academic-base";

export const academicYearService = {
    // Queries
    useAcademicYears: (status?: AcademicYearStatus) => {
        return useQuery({
            queryKey: ["academic", "years", status],
            queryFn: async () => {
                const response = await api.get<AcademicYear[]>("/academic/academic-years", {
                    params: { status }
                });
                return response.data;
            }
        });
    },

    useAcademicYear: (id: number) => {
        return useQuery({
            queryKey: ["academic", "year", id],
            queryFn: async () => {
                const response = await api.get<AcademicYear>(`/academic/academic-years/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    useCurrentYear: () => {
        return useQuery({
            queryKey: ["academic", "year", "current"],
            queryFn: async () => {
                const response = await api.get<AcademicYear[]>("/academic/academic-years", {
                    params: { is_current: true }
                });
                return response.data[0] || null;
            }
        });
    },

    // Mutations
    useCreateAcademicYear: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: AcademicYearCreateData) => {
                const response = await api.post<AcademicYear>("/academic/academic-years", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "years"] });
            }
        });
    },

    useUpdateAcademicYear: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, data }: { id: number; data: Partial<AcademicYearCreateData> }) => {
                const response = await api.put<AcademicYear>(`/academic/academic-years/${id}`, data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["academic", "years"] });
                queryClient.invalidateQueries({ queryKey: ["academic", "year", data.id] });
                if (data.is_current) {
                    queryClient.invalidateQueries({ queryKey: ["academic", "year", "current"] });
                }
            }
        });
    },

    useDeleteAcademicYear: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                await api.delete(`/academic/academic-years/${id}`);
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["academic", "years"] });
                queryClient.invalidateQueries({ queryKey: ["academic", "year", "current"] });
            }
        });
    }
};
