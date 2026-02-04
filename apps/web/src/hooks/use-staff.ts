/**
 * Staff Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/utils/api';

const staffApi = {
    list: async () => {
        const response = await api.get('/hr/staff');
        return response.data;
    },
    getShifts: async () => {
        const response = await api.get('/hr/shifts');
        return response.data;
    },
    create: async (data: any) => {
        const response = await api.post('/hr/staff', data);
        return response.data;
    },
    update: async (id: number, data: any) => {
        const response = await api.put(`/hr/staff/${id}`, data);
        return response.data;
    },
    delete: async (id: number) => {
        const response = await api.delete(`/hr/staff/${id}`);
        return response.data;
    }
};

export function useStaff() {
    return useQuery({
        queryKey: ['staff', 'list'],
        queryFn: () => staffApi.list(),
    });
}

export function useShifts() {
    return useQuery({
        queryKey: ['staff', 'shifts'],
        queryFn: () => staffApi.getShifts(),
    });
}

export function useCreateStaff() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: any) => staffApi.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['staff'] });
        },
    });
}

export function useUpdateStaff() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: any }) => staffApi.update(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['staff'] });
        },
    });
}

export function useDeleteStaff() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => staffApi.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['staff'] });
        },
    });
}
