/**
 * Inventory Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const inventoryApi = {
    list: async (filters?: any) => {
        const response = await fetch('/api/v1/inventory');
        return response.json();
    },
};

export function useAssets(filters?: {
    category?: string;
    query?: string;
}) {
    return useQuery({
        queryKey: ['inventory', 'assets', filters],
        queryFn: () => inventoryApi.list(filters),
    });
}

export function useCreateAsset() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: any) => inventoryApi.list(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['inventory'] });
        },
    });
}
