/**
 * Settings and Configuration Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

import { api } from '@/utils/api';

const settingsApi = {
    updateProfile: async (data: any) => {
        const response = await api.post('/settings/profile', data);
        return response.data;
    },
    changePassword: async (data: any) => {
        const response = await api.post('/settings/change-password', data);
        return response.data;
    },
    getSettings: async (type: string) => {
        const response = await api.get('/settings', { params: { group: type } });
        return response.data;
    },
    testConnection: async (gateway: string) => {
        const response = await api.post('/settings/test-connection', null, { params: { gateway } });
        return response.data;
    },
    updateSetting: async (id: number, data: any) => {
        const response = await api.patch(`/settings/${id}`, data);
        return response.data;
    },
    getAuditLogs: async () => {
        const response = await api.get('/settings/audit-logs');
        return response.data;
    }
};

export function useUpdateProfile() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: settingsApi.updateProfile,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['auth', 'user'] });
        }
    });
}

export function useChangePassword() {
    return useMutation({
        mutationFn: settingsApi.changePassword
    });
}

export function useSettings(type: string) {
    return useQuery({
        queryKey: ['settings', type],
        queryFn: () => settingsApi.getSettings(type),
    });
}

export function useTestConnection() {
    return useMutation({
        mutationFn: settingsApi.testConnection
    });
}

export function useUpdateSetting() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: ({ id, data }: { id: number, data: any }) => settingsApi.updateSetting(id, data),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['settings'] })
    });
}

export function useAuditLogs() {
    return useQuery({
        queryKey: ['settings', 'logs'],
        queryFn: () => settingsApi.getAuditLogs(),
    });
}
