import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '@/services/dashboard-api';

export const useFacultyDashboard = () => {
  return useQuery({
    queryKey: ['dashboard', 'faculty'],
    queryFn: () => dashboardApi.getFacultyDashboard(),
    staleTime: 1000 * 60 * 5, // 5 minutes
    gcTime: 1000 * 60 * 10,  // 10 minutes
    refetchOnWindowFocus: false,
    retry: 2,
  });
};
