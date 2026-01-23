/**
 * Document Management API Service
 * 
 * Provides methods to interact with document management endpoints
 */
import { api } from '@/utils/api';


export const documentApi = {
    /**
     * Upload a document
     */
    upload: async (studentId: number, categoryId: number, file: File, metadata?: any): Promise<any> => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('student_id', studentId.toString());
        formData.append('category_id', categoryId.toString());
        if (metadata) {
            formData.append('metadata', JSON.stringify(metadata));
        }

        const response = await api.post('/documents', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },

    /**
     * Get all documents with filters
     */
    list: async (filters?: {
        student_id?: number;
        category_id?: number;
        verification_status?: string;
    }): Promise<any[]> => {
        const response = await api.get('/documents', { params: filters });
        return response.data;
    },

    /**
     * Get a specific document
     */
    get: async (id: number): Promise<any> => {
        const response = await api.get(`/${id}`);
        return response.data;
    },

    /**
     * Verify a document
     */
    verify: async (id: number, verified: boolean, remarks?: string): Promise<any> => {
        const response = await api.post(`/${id}/verify`, {
            verified,
            remarks
        });
        return response.data;
    },

    /**
     * Reject a document
     */
    reject: async (id: number, reason: string): Promise<any> => {
        const response = await api.post(`/${id}/reject`, { reason });
        return response.data;
    },

    /**
     * Download a document
     */
    download: async (id: number): Promise<Blob> => {
        const response = await api.get(`/${id}/download`, {
            responseType: 'blob'
        });
        return response.data;
    },

    /**
     * Get document categories
     */
    getCategories: async (): Promise<any[]> => {
        const response = await api.get(`/categories`);
        return response.data;
    },
};

export default documentApi;
