/**
 * ODC (Outdoor Catering) Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/utils/api';

// Placeholder - will need actual API service
const odcApi = {
    getHotels: async () => {
        const response = await api.get('/odc/hotels');
        return response.data;
    },
    getRequests: async () => {
        const response = await api.get('/odc/requests');
        return response.data;
    },
    getPendingPayouts: async () => {
        const response = await api.get('/odc/payouts/pending');
        return response.data;
    },
    getBilling: async () => {
        const response = await api.get('/odc/billing');
        return response.data;
    }
};

export function useODCHotels() {
    return useQuery({
        queryKey: ['odc', 'hotels'],
        queryFn: () => odcApi.getHotels(),
    });
}

export function useODCRequests() {
    return useQuery({
        queryKey: ['odc', 'requests'],
        queryFn: () => odcApi.getRequests(),
    });
}

export function useODCPendingPayouts() {
    return useQuery({
        queryKey: ['odc', 'payouts', 'pending'],
        queryFn: () => odcApi.getPendingPayouts(),
    });
}

export function useODCBilling() {
    return useQuery({
        queryKey: ['odc', 'billing'],
        queryFn: () => odcApi.getBilling(),
    });
}
