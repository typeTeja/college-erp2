import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
    Asset, AssetCreateDTO,
    AssetAllocation, AllocationCreateDTO,
    AssetAudit, AuditCreateDTO,
    UniformAllocation, UniformAllocationCreateDTO
} from "@/types/inventory";

export const inventoryService = {
    // Assets
    useAssets: (filters?: { category?: string; query?: string }) => {
        return useQuery({
            queryKey: ["assets", filters],
            queryFn: async () => {
                const response = await api.get<Asset[]>("/inventory/assets", { params: filters });
                return response.data;
            }
        });
    },

    useAsset: (id: number) => {
        return useQuery({
            queryKey: ["asset", id],
            queryFn: async () => {
                const response = await api.get<Asset>(`/inventory/assets/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    useCreateAsset: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: AssetCreateDTO) => {
                const response = await api.post<Asset>("/inventory/assets", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["assets"] });
            }
        });
    },

    // Allocations
    useAllocateAsset: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: AllocationCreateDTO) => {
                const response = await api.post<AssetAllocation>("/inventory/allocate", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["assets"] });
                queryClient.invalidateQueries({ queryKey: ["allocations"] });
            }
        });
    },

    useReturnAsset: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, status }: { id: number; status: string }) => {
                const response = await api.put<AssetAllocation>(`/inventory/return/${id}`, null, { params: { status } });
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["assets"] });
                queryClient.invalidateQueries({ queryKey: ["allocations"] });
            }
        });
    },

    // Audits
    usePerformAudit: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: AuditCreateDTO) => {
                const response = await api.post<AssetAudit>("/inventory/audit", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["assets"] });
            }
        });
    },

    // Uniforms
    useStudentUniforms: (studentId: number) => {
        return useQuery({
            queryKey: ["student-uniforms", studentId],
            queryFn: async () => {
                const response = await api.get<UniformAllocation[]>(`/inventory/uniforms/student/${studentId}`);
                return response.data;
            },
            enabled: !!studentId
        });
    },

    useIssueUniform: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: UniformAllocationCreateDTO) => {
                const response = await api.post<UniformAllocation>("/inventory/uniforms", data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["student-uniforms", data.student_id] });
            }
        });
    }
};
