/**
 * Dashboard API Service
 * 
 * Provides typed methods to interact with dashboard endpoints.
 * Follows the same pattern as admission-api.ts for consistency.
 */

import { api } from '@/utils/api';
import type {
  PrincipalDashboardData,
  ParentDashboardData,
  StudentDashboardData,
  FacultyDashboardData,
  AnyStaffDashboardData,
  StaffRole,
} from '@/types/dashboard';

const BASE_URL = '/dashboard';

// ============================================================================
// Dashboard APIs
// ============================================================================

export const dashboardApi = {
  /**
   * Get Principal Dashboard data
   * 
   * Requires: PRINCIPAL, ADMIN, or SUPER_ADMIN role
   * Returns: Executive-level metrics and insights
   */
  getPrincipalDashboard: async (): Promise<PrincipalDashboardData> => {
    const response = await api.get(`${BASE_URL}/principal`);
    return response.data;
  },

  /**
   * Get Parent Dashboard data
   * 
   * Requires: PARENT role
   * Returns: Student progress and communication data for logged-in parent's child
   */
  getParentDashboard: async (): Promise<ParentDashboardData> => {
    const response = await api.get(`${BASE_URL}/parent`);
    return response.data;
  },

  /**
   * Get Student Dashboard data
   * 
   * Requires: STUDENT role
   * Returns: Academic planning and execution data for logged-in student
   */
  getStudentDashboard: async (): Promise<StudentDashboardData> => {
    const response = await api.get(`${BASE_URL}/student`);
    return response.data;
  },

  /**
   * Get Staff Dashboard data
   * 
   * Requires: STAFF role
   * Returns: Role-specific operational data based on staff role
   * 
   * @param role - Staff role (librarian, warden, accounts, sse)
   */
  getStaffDashboard: async (role: StaffRole): Promise<AnyStaffDashboardData> => {
    const response = await api.get(`${BASE_URL}/staff`, {
      params: { role },
    });
    return response.data;
  },

  /**
   * Get Faculty Dashboard data
   * 
   * Requires: FACULTY role
   * Returns: Teaching schedule and academic tasks
   */
  getFacultyDashboard: async (): Promise<FacultyDashboardData> => {
    const response = await api.get(`${BASE_URL}/faculty`);
    return response.data;
  },

  /**
   * Refresh dashboard data
   * 
   * Forces a refresh of cached dashboard data
   * Useful for "Refresh" buttons in the UI
   * 
   * @param dashboardType - Type of dashboard to refresh
   */
  refreshDashboard: async (
    dashboardType: 'principal' | 'parent' | 'student' | 'staff'
  ): Promise<{ message: string }> => {
    const response = await api.post(`${BASE_URL}/${dashboardType}/refresh`);
    return response.data;
  },
};

export default dashboardApi;
