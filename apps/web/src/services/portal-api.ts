/**
 * Student Portal API Service
 * 
 * Provides methods to interact with student portal endpoints
 */
import axios from 'axios';

const BASE_URL = '/api/v1/portal';

export const portalApi = {
    /**
     * Get student dashboard data
     */
    getDashboard: async (): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/dashboard`);
        return response.data;
    },

    /**
     * Get student profile
     */
    getProfile: async (): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/profile`);
        return response.data;
    },

    /**
     * Update student profile
     */
    updateProfile: async (data: any): Promise<any> => {
        const response = await axios.put(`${BASE_URL}/profile`, data);
        return response.data;
    },

    /**
     * Get notifications
     */
    getNotifications: async (filters?: { unread?: boolean }): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/notifications`, { params: filters });
        return response.data;
    },

    /**
     * Mark notification as read
     */
    markNotificationRead: async (id: number): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/notifications/${id}/read`);
        return response.data;
    },

    /**
     * Mark all notifications as read
     */
    markAllNotificationsRead: async (): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/notifications/read-all`);
        return response.data;
    },

    /**
     * Get student activity log
     */
    getActivity: async (filters?: { limit?: number }): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/activity`, { params: filters });
        return response.data;
    },

    /**
     * Change password
     */
    changePassword: async (currentPassword: string, newPassword: string): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/change-password`, {
            current_password: currentPassword,
            new_password: newPassword
        });
        return response.data;
    },
};

export default portalApi;
