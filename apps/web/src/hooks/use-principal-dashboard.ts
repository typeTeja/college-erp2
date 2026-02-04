/**
 * Principal Dashboard Hook
 * 
 * React Query hook for fetching Principal Dashboard data.
 * Includes auto-refresh every minute for real-time monitoring.
 */

import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '@/services/dashboard-api';

export function usePrincipalDashboard() {
  return useQuery({
    queryKey: ['dashboard', 'principal'],
    queryFn: () => dashboardApi.getPrincipalDashboard(),
    staleTime: 1000 * 60, // 1 minute
    refetchInterval: 1000 * 60, // Auto-refresh every minute
    retry: 2, // Retry failed requests twice
  });
}
