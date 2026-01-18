/**
 * Settings and Configuration Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const settingsApi = {
    updateProfile: async (data: any) => {
        const response = await fetch('/api/v1/settings/profile', {
            method: 'PUT',
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) throw new Error('Failed to update profile');
        return response.json();
    },
    changePassword: async (data: any) => {
        const response = await fetch('/api/v1/auth/change-password', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) throw new Error(await response.text());
        return response.json();
    },
    getSettings: async (type: string) => {
        // Mock
        return [];
    },
    testConnection: async (gateway: string) => {
        // Mock
        return { message: 'Connection successful' };
    },
    updateSetting: async (id: number, data: any) => {
        // Mock
        return {};
    },
    getAuditLogs: async () => {
        // Mock
        return [];
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
