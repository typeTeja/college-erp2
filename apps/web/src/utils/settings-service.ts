import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "./api";

export interface SystemSetting {
    id: number;
    key: string;
    value: any;
    group: string;
    is_secret: boolean;
    description: string;
    updated_at: string;
}

export interface AuditLog {
    id: number;
    timestamp: string;
    user_id: number;
    action: string;
    module: string;
    description: string;
    from_value: any;
    to_value: any;
}

export const settingsService = {
    useSettings: (group?: string) => {
        return useQuery({
            queryKey: ["settings", group],
            queryFn: async () => {
                const response = await api.get("/settings", {
                    params: { group }
                });
                return response.data as SystemSetting[];
            }
        });
    },

    useUpdateSetting: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, data }: { id: number; data: any }) => {
                const response = await api.patch(`/settings/${id}`, data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["settings"] });
            }
        });
    },

    useAuditLogs: (module?: string) => {
        return useQuery({
            queryKey: ["audit-logs", module],
            queryFn: async () => {
                const response = await api.get("/settings/audit-logs", {
                    params: { module }
                });
                return response.data as AuditLog[];
            }
        });
    },

    useTestConnection: () => {
        return useMutation({
            mutationFn: async (gateway: string) => {
                const response = await api.post("/settings/test-connection", null, {
                    params: { gateway }
                });
                return response.data;
            }
        });
    },

    useChangePassword: () => {
        return useMutation({
            mutationFn: async (data: any) => {
                const response = await api.post("/settings/change-password", data);
                return response.data;
            }
        });
    },

    useUpdateProfile: () => {
        return useMutation({
            mutationFn: async (data: any) => {
                const response = await api.post("/settings/profile", data);
                return response.data;
            }
        });
    },

    useBulkUpdateSettings: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: Record<string, any>) => {
                const response = await api.post("/settings/bulk", { settings: data });
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["settings"] });
            }
        });
    }
};
