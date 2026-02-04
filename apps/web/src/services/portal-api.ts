/**
 * Student Portal API Service
 * 
 * Provides methods to interact with student portal endpoints
 */
import { api } from '@/utils/api';

export const portalApi = {
    /**
     * Get student dashboard data
     */
    getDashboard: async (): Promise<any> => {
        const response = await api.get('/students/portal/dashboard');
        return response.data;
    },

    /**
     * Get student profile
     */
    getProfile: async (): Promise<any> => {
        const response = await api.get('/students/portal/profile');
        return response.data;
    },

    /**
     * Update student profile
     */
    updateProfile: async (data: any): Promise<any> => {
        const response = await api.put('/students/portal/profile', data);
        return response.data;
    },

    /**
     * Get notifications
     */
    getNotifications: async (filters?: { unread?: boolean }): Promise<any[]> => {
        const response = await api.get('/students/portal/notifications', { params: filters });
        return response.data;
    },

    /**
     * Mark notification as read
     */
    markNotificationRead: async (id: number): Promise<any> => {
        const response = await api.post(`/students/portal/notifications/${id}/read`);
        return response.data;
    },

    /**
     * Mark all notifications as read
     */
    markAllNotificationsRead: async (): Promise<any> => {
        const response = await api.post('/students/portal/notifications/read-all');
        return response.data;
    },

    /**
     * Get student activity log
     */
    getActivity: async (filters?: { limit?: number }): Promise<any[]> => {
        const response = await api.get('/students/portal/activity', { params: filters });
        return response.data;
    },

    /**
     * Change password
     */
    changePassword: async (currentPassword: string, newPassword: string): Promise<any> => {
        const response = await api.post('/students/portal/change-password', {
            current_password: currentPassword,
            new_password: newPassword
        });
        return response.data;
    },
};

export default portalApi;
