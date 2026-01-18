/**
 * Placement & Training API Service
 * 
 * Provides methods to interact with placement endpoints
 */
import axios from 'axios';

const BASE_URL = '/api/v1/placement';

export const placementApi = {
    /**
     * Get all companies
     */
    listCompanies: async (): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/companies`);
        return response.data;
    },

    /**
     * Get all placement drives
     */
    listDrives: async (filters?: { status?: string }): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/drives`, { params: filters });
        return response.data;
    },

    /**
     * Apply for placement drive
     */
    applyForDrive: async (data: {
        drive_id: number;
        student_id: number;
    }): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/applications`, data);
        return response.data;
    },

    /**
     * Get training programs
     */
    listTrainingPrograms: async (): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/training`);
        return response.data;
    },

    /**
     * Get internships
     */
    listInternships: async (filters?: { status?: string }): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/internships`, { params: filters });
        return response.data;
    },

    /**
     * Get placement statistics
     */
    getStatistics: async (): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/statistics`);
        return response.data;
    },
};

export default placementApi;
