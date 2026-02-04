/**
 * Student Dashboard Hook
 * 
 * React Query hook for fetching Student Dashboard data.
 * Refreshes every 5 minutes to show updated academic information.
 */

import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '@/services/dashboard-api';

export function useStudentDashboard() {
  return useQuery({
    queryKey: ['dashboard', 'student'],
    queryFn: () => dashboardApi.getStudentDashboard(),
    staleTime: 1000 * 60 * 5, // 5 minutes
    gcTime: 1000 * 60 * 10, // 10 minutes cache
    refetchOnWindowFocus: false,
    retry: 2, // Retry failed requests twice
  });
}
