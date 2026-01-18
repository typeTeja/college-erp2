/**
 * Staff Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Placeholder - will need actual API service or reuse existing one appropriately
// Assuming we need a specific staff service
const staffApi = {
    list: async () => {
        // In a real app, this would be a fetch call to /api/v1/staff
        // For now, we simulate or assume the endpoint exists
        const response = await fetch('/api/v1/staff');
        if (!response.ok) throw new Error('Failed to fetch staff');
        return response.json();
    },
    getShifts: async () => {
        const response = await fetch('/api/v1/staff/shifts');
        if (!response.ok) throw new Error('Failed to fetch shifts');
        return response.json();
    },
    create: async (data: any) => {
        const response = await fetch('/api/v1/staff', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) throw new Error('Failed to create staff');
        return response.json();
    },
    update: async (id: number, data: any) => {
        const response = await fetch(`/api/v1/staff/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) throw new Error('Failed to update staff');
        return response.json();
    },
    delete: async (id: number) => {
        const response = await fetch(`/api/v1/staff/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Failed to delete staff');
        return response.json();
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
