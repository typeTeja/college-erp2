/**
 * Hall Ticket API Service
 * 
 * Provides methods to interact with hall ticket endpoints
 */
import { api } from '@/utils/api';


export const hallTicketApi = {
    /**
     * Create hall ticket configuration
     */
    createConfig: async (data: any): Promise<any> => {
        const response = await api.post(`/configs`, data);
        return response.data;
    },

    /**
     * Get all configurations
     */
    listConfigs: async (filters?: { academic_year?: string }): Promise<any[]> => {
        const response = await api.get(`/configs`, { params: filters });
        return response.data;
    },

    /**
     * Generate hall tickets for a configuration
     */
    generateTickets: async (configId: number): Promise<any> => {
        const response = await api.post(`/configs/${configId}/generate`);
        return response.data;
    },

    /**
     * Get a specific hall ticket
     */
    get: async (id: number): Promise<any> => {
        const response = await api.get(`/${id}`);
        return response.data;
    },

    /**
     * Download hall ticket PDF
     */
    download: async (id: number): Promise<Blob> => {
        const response = await api.get(`/${id}/download`, {
            responseType: 'blob'
        });
        return response.data;
    },

    /**
     * Get hall ticket by student
     */
    getByStudent: async (studentId: number, configId?: number): Promise<any> => {
        const response = await api.get(`/student/${studentId}`, {
            params: { config_id: configId }
        });
        return response.data;
    },
};

export default hallTicketApi;
