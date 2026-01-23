/**
 * Role Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/utils/api';

const rolesApi = {
    list: async () => {
        const response = await api.get('/roles');
        return response.data;
    },
    getPermissions: async () => {
        const response = await api.get('/permissions');
        return response.data;
    },
};

export function useRoles() {
    return useQuery({
        queryKey: ['roles', 'list'],
        queryFn: () => rolesApi.list(),
    });
}

export function usePermissions() {
    return useQuery({
        queryKey: ['permissions', 'list'],
        queryFn: () => rolesApi.getPermissions(),
    });
}

export function useAuditLogs() {
    return useQuery({
        queryKey: ['roles', 'audit'],
        queryFn: () => rolesApi.list(),
    });
}

export function useUpdateRole(roleId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: any) => rolesApi.list(),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['roles'] });
        },
    });
}
