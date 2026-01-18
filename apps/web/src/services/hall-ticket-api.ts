/**
 * Hall Ticket API Service
 * 
 * Provides methods to interact with hall ticket endpoints
 */
import axios from 'axios';

const BASE_URL = '/api/v1/hall-tickets';

export const hallTicketApi = {
    /**
     * Create hall ticket configuration
     */
    createConfig: async (data: any): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/configs`, data);
        return response.data;
    },

    /**
     * Get all configurations
     */
    listConfigs: async (filters?: { academic_year?: string }): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/configs`, { params: filters });
        return response.data;
    },

    /**
     * Generate hall tickets for a configuration
     */
    generateTickets: async (configId: number): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/configs/${configId}/generate`);
        return response.data;
    },

    /**
     * Get a specific hall ticket
     */
    get: async (id: number): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/${id}`);
        return response.data;
    },

    /**
     * Download hall ticket PDF
     */
    download: async (id: number): Promise<Blob> => {
        const response = await axios.get(`${BASE_URL}/${id}/download`, {
            responseType: 'blob'
        });
        return response.data;
    },

    /**
     * Get hall ticket by student
     */
    getByStudent: async (studentId: number, configId?: number): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/student/${studentId}`, {
            params: { config_id: configId }
        });
        return response.data;
    },
};

export default hallTicketApi;
