/**
 * Communication/Circulars Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/utils/api';

const circularsApi = {
    list: async () => {
        const response = await api.get('/circulars');
        return response.data;
    },
};

export function useCirculars(filters?: { search?: string }) {
    return useQuery({
        queryKey: ['circulars', 'list', filters],
        queryFn: () => circularsApi.list(),
    });
}

export function useCreateCircular() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: any) => circularsApi.list(),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['circulars'] });
        },
    });
}
