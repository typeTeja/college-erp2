/**
 * Placement & Training API Service
 * 
 * Provides methods to interact with placement endpoints
 */
import { api } from '@/utils/api';


export const placementApi = {
    /**
     * Get all companies
     */
    listCompanies: async (): Promise<any[]> => {
        const response = await api.get(`/companies`);
        return response.data;
    },

    /**
     * Get all placement drives
     */
    listDrives: async (filters?: { status?: string }): Promise<any[]> => {
        const response = await api.get(`/drives`, { params: filters });
        return response.data;
    },

    /**
     * Apply for placement drive
     */
    applyForDrive: async (data: {
        drive_id: number;
        student_id: number;
    }): Promise<any> => {
        const response = await api.post(`/applications`, data);
        return response.data;
    },

    /**
     * Get training programs
     */
    listTrainingPrograms: async (): Promise<any[]> => {
        const response = await api.get(`/training`);
        return response.data;
    },

    /**
     * Get internships
     */
    listInternships: async (filters?: { status?: string }): Promise<any[]> => {
        const response = await api.get(`/internships`, { params: filters });
        return response.data;
    },

    /**
     * Get placement statistics
     */
    getStatistics: async (): Promise<any> => {
        const response = await api.get(`/statistics`);
        return response.data;
    },
};

export default placementApi;
