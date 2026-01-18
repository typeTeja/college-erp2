/**
 * Portal Hooks
 * 
 * Custom React Query hooks for student portal operations
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import portalApi from '@/services/portal-api';
import { queryKeys } from '@/config/react-query';

// ============================================================================
// Dashboard Hooks
// ============================================================================

export function usePortalDashboard() {
    return useQuery({
        queryKey: queryKeys.portal.dashboard,
        queryFn: () => portalApi.getDashboard(),
        staleTime: 2 * 60 * 1000, // 2 minutes
    });
}

// ============================================================================
// Profile Hooks
// ============================================================================

export function usePortalProfile() {
    return useQuery({
        queryKey: queryKeys.portal.profile,
        queryFn: () => portalApi.getProfile(),
    });
}

export function useUpdateProfile() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: portalApi.updateProfile,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.portal.profile });
        },
    });
}

// ============================================================================
// Notification Hooks
// ============================================================================

export function useNotifications(filters?: { unread?: boolean }) {
    return useQuery({
        queryKey: [...queryKeys.portal.notifications, filters],
        queryFn: () => portalApi.getNotifications(filters),
        refetchInterval: 30000, // Refetch every 30 seconds
    });
}

export function useMarkNotificationRead() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => portalApi.markNotificationRead(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.portal.notifications });
        },
    });
}

export function useMarkAllNotificationsRead() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: () => portalApi.markAllNotificationsRead(),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.portal.notifications });
        },
    });
}

// ============================================================================
// Activity Hooks
// ============================================================================

export function useActivity(limit?: number) {
    return useQuery({
        queryKey: [...queryKeys.portal.all, 'activity', { limit }],
        queryFn: () => portalApi.getActivity({ limit }),
    });
}

// ============================================================================
// Password Hooks
// ============================================================================

export function useChangePassword() {
    return useMutation({
        mutationFn: ({ currentPassword, newPassword }: {
            currentPassword: string;
            newPassword: string;
        }) => portalApi.changePassword(currentPassword, newPassword),
    });
}
