import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api';
import { Role, RoleCreateDTO, RoleUpdateDTO, PermissionGroup, PermissionAuditLog } from '@/types/role';

export const roleService = {
    useRoles: () => {
        return useQuery({
            queryKey: ['roles'],
            queryFn: async () => {
                const response = await api.get<Role[]>('/roles/');
                return response.data;
            }
        });
    },

    usePermissions: () => {
        return useQuery({
            queryKey: ['permissions'],
            queryFn: async () => {
                const response = await api.get<PermissionGroup[]>('/roles/permissions');
                return response.data;
            }
        });
    },

    useAuditLogs: () => {
        return useQuery({
            queryKey: ['roles-audit'],
            queryFn: async () => {
                const response = await api.get<PermissionAuditLog[]>('/roles/audit');
                return response.data;
            }
        });
    },

    useCreateRole: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: RoleCreateDTO) => {
                const response = await api.post<Role>('/roles/', data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['roles'] });
                queryClient.invalidateQueries({ queryKey: ['roles-audit'] });
            }
        });
    },

    useUpdateRole: (id: number) => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: RoleUpdateDTO) => {
                const response = await api.patch<Role>(`/roles/${id}`, data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['roles'] });
                queryClient.invalidateQueries({ queryKey: ['roles-audit'] });
            }
        });
    }
};
