/**
 * Staff Dashboard Hook
 * 
 * React Query hook for fetching Staff Dashboard data based on role.
 * Supports librarian, warden, accounts, and SSE roles.
 */

import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '@/services/dashboard-api';
import type { StaffRole } from '@/types/dashboard';

export function useStaffDashboard(role: StaffRole) {
  return useQuery({
    queryKey: ['dashboard', 'staff', role],
    queryFn: () => dashboardApi.getStaffDashboard(role),
    staleTime: 1000 * 60 * 5, // 5 minutes
    enabled: !!role, // Only fetch if role is provided
    retry: 2, // Retry failed requests twice
  });
}
