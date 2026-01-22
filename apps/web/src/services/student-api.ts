/**
 * Student Management API Service
 * 
 * Provides methods to interact with student management endpoints
 */
import { api } from '@/utils/api';

const BASE_URL = '/students';

// ============================================================================
// Student APIs
// ============================================================================

export const studentApi = {
    /**
     * Get all students with optional filters
     */
    list: async (filters?: {
        program_id?: number;
        year?: number;
        semester?: number;
        status?: string;
        search?: string;
    }): Promise<any[]> => {
        const response = await api.get(BASE_URL, { params: filters });
        return response.data;
    },

    /**
     * Get a specific student by ID
     */
    get: async (id: number): Promise<any> => {
        const response = await api.get(`${BASE_URL}/${id}`);
        return response.data;
    },

    /**
     * Create a new student
     */
    create: async (data: any): Promise<any> => {
        const response = await api.post(BASE_URL, data);
        return response.data;
    },

    /**
     * Update a student
     */
    update: async (id: number, data: any): Promise<any> => {
        const response = await api.put(`${BASE_URL}/${id}`, data);
        return response.data;
    },

    /**
     * Delete a student
     */
    delete: async (id: number): Promise<void> => {
        await api.delete(`${BASE_URL}/${id}`);
    },

    /**
     * Upload student document
     */
    uploadDocument: async (id: number, file: File, documentType: string): Promise<any> => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('document_type', documentType);

        const response = await api.post(`${BASE_URL}/${id}/documents`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },

    /**
     * Get student activity history
     */
    getActivity: async (id: number): Promise<any[]> => {
        const response = await api.get(`${BASE_URL}/${id}/activity`);
        return response.data;
    },

    /**
     * Deactivate a student
     */
    deactivate: async (id: number, reason: string): Promise<any> => {
        const response = await api.post(`${BASE_URL}/${id}/deactivate`, { reason });
        return response.data;
    },

    /**
     * Reactivate a student
     */
    reactivate: async (id: number): Promise<any> => {
        const response = await api.post(`${BASE_URL}/${id}/reactivate`);
        return response.data;
    },
};

export default studentApi;
