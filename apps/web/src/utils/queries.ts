import { useQuery } from '@tanstack/react-query';
import { api } from './api';

export function useDashboardStats() {
    return useQuery({
        queryKey: ['dashboardStats'],
        queryFn: async () => {
            const response = await api.get('/dashboard/stats');
            return response.data;
        },
    });
}

export function useRecentAdmissions() {
    return useQuery({
        queryKey: ['recentAdmissions'],
        queryFn: async () => {
            const response = await api.get('/admissions/recent');
            return response.data;
        },
    });
}
