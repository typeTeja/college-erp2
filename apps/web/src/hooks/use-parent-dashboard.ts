/**
 * Parent Dashboard Hook
 * 
 * React Query hook for fetching Parent Dashboard data.
 * Refreshes every 5 minutes to show updated student progress.
 */

import { dashboardApi } from '@/services/dashboard-api';

export const useParentDashboard = () => {
  return useQuery({
    queryKey: ['dashboard', 'parent'],
    queryFn: () => dashboardApi.getParentDashboard(),
    staleTime: 1000 * 60 * 5, // 5 minutes
    gcTime: 1000 * 60 * 10, // 10 minutes cache
    refetchOnWindowFocus: false,
    retry: 2,
  });
};

export default useParentDashboard;
