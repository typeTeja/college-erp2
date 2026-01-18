/**
 * Role Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const rolesApi = {
    list: async () => {
        const response = await fetch('/api/v1/roles');
        return response.json();
    },
    getPermissions: async () => {
        const response = await fetch('/api/v1/permissions');
        return response.json();
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
