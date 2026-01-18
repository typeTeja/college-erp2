/**
 * ODC (Outdoor Catering) Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Placeholder - will need actual API service
const odcApi = {
    getHotels: async () => {
        const response = await fetch('/api/v1/odc/hotels');
        return response.ok ? response.json() : [];
    },
    getRequests: async () => {
        const response = await fetch('/api/v1/odc/requests');
        return response.ok ? response.json() : [];
    },
    getPendingPayouts: async () => {
        const response = await fetch('/api/v1/odc/payouts/pending');
        return response.ok ? response.json() : [];
    },
    getBilling: async () => {
        const response = await fetch('/api/v1/odc/billing');
        return response.ok ? response.json() : [];
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
