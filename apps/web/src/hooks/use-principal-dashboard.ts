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
    staleTime: 1000 * 60 * 5, // 5 minutes (increased from 1 minute)
    gcTime: 1000 * 60 * 10, // 10 minutes cache
    refetchInterval: 1000 * 60 * 5, // Auto-refresh every 5 minutes
    refetchOnWindowFocus: false,
    retry: 2,
  });
}
