/**
 * Communication/Circulars Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const circularsApi = {
    list: async () => {
        const response = await fetch('/api/v1/circulars');
        return response.json();
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
