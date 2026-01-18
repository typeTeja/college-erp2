/**
 * Analytics & Dashboard Hooks
 */
import { useQuery } from '@tanstack/react-query';
import analyticsApi from '@/services/analytics-api';
import { queryKeys } from '@/config/react-query';

export function useDashboardSummary() {
    return useQuery({
        queryKey: queryKeys.analytics.dashboard,
        queryFn: () => analyticsApi.getDashboardSummary(),
        staleTime: 5 * 60 * 1000, // 5 minutes
    });
}

export function useEnrollmentTrends(filters?: {
    from_year?: string;
    to_year?: string;
}) {
    return useQuery({
        queryKey: queryKeys.analytics.trends('enrollment', filters),
        queryFn: () => analyticsApi.getEnrollmentTrends(filters),
    });
}

export function useFeeAnalytics(filters?: {
    academic_year?: string;
}) {
    return useQuery({
        queryKey: queryKeys.analytics.trends('fees', filters),
        queryFn: () => analyticsApi.getFeeAnalytics(filters),
    });
}

export function useExamPerformance(filters?: {
    program_id?: number;
    semester?: number;
}) {
    return useQuery({
        queryKey: queryKeys.analytics.trends('performance', filters),
        queryFn: () => analyticsApi.getExamPerformance(filters),
    });
}
