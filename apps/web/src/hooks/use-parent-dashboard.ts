/**
 * Parent Dashboard Hook
 * 
 * React Query hook for fetching Parent Dashboard data.
 * Refreshes every 5 minutes to show updated student progress.
 */

import { useQuery } from '@tanstack/react-query';

const useParentDashboard = () => {
  return useQuery({
    queryKey: ['parentDashboard'],
    queryFn: async () => {
      // Replace with actual data fetching logic
      const response = await fetch('/api/parent-dashboard');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
    gcTime: 1000 * 60 * 10, // 10 minutes cache
    refetchOnWindowFocus: false,
    retry: 2, // Retry failed requests twice
  });
};

export default useParentDashboard;
