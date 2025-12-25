import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
    Circular, CircularCreateDTO,
    Notification
} from "@/types/communication";

export const communicationService = {
    // Circulars
    useCirculars: (params?: { offset?: number; limit?: number }) => {
        return useQuery({
            queryKey: ["circulars", params],
            queryFn: async () => {
                const response = await api.get<Circular[]>("/communication/circulars", { params });
                return response.data;
            }
        });
    },

    useCreateCircular: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: CircularCreateDTO) => {
                const response = await api.post<Circular>("/communication/circulars", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["circulars"] });
            }
        });
    },

    // Notifications
    useNotifications: (params?: { unread_only?: boolean; limit?: number }) => {
        return useQuery({
            queryKey: ["notifications", params],
            queryFn: async () => {
                const response = await api.get<Notification[]>("/communication/notifications", { params });
                return response.data;
            }
        });
    },

    useMarkAsRead: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                const response = await api.patch<Notification>(`/communication/notifications/${id}/read`);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["notifications"] });
            }
        });
    },

    useMarkAllAsRead: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async () => {
                const response = await api.patch("/communication/notifications/read-all");
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["notifications"] });
            }
        });
    }
};
