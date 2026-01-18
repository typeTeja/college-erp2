/**
 * Admission Management API Service
 * 
 * Provides methods to interact with admission/application endpoints
 */
import axios from 'axios';

const BASE_URL = '/api/v1/admissions';

// ============================================================================
// Application APIs
// ============================================================================

export const admissionApi = {
    /**
     * Create a new application
     */
    create: async (data: any): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/applications`, data);
        return response.data;
    },

    /**
     * Get all applications with filters
     */
    list: async (filters?: {
        status?: string;
        program_id?: number;
        academic_year?: string;
        search?: string;
    }): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/applications`, { params: filters });
        return response.data;
    },

    /**
     * Get a specific application
     */
    get: async (id: number): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/applications/${id}`);
        return response.data;
    },

    /**
     * Update an application
     */
    update: async (id: number, data: any): Promise<any> => {
        const response = await axios.put(`${BASE_URL}/applications/${id}`, data);
        return response.data;
    },

    /**
     * Upload application document
     */
    uploadDocument: async (id: number, file: File, documentType: string): Promise<any> => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('document_type', documentType);

        const response = await axios.post(`${BASE_URL}/applications/${id}/documents`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },

    /**
     * Verify a document
     */
    verifyDocument: async (applicationId: number, documentId: number, verified: boolean, remarks?: string): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/applications/${applicationId}/documents/${documentId}/verify`, {
            verified,
            remarks
        });
        return response.data;
    },

    /**
     * Generate hall ticket
     */
    generateHallTicket: async (id: number): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/applications/${id}/hall-ticket`);
        return response.data;
    },

    /**
     * Generate offer letter
     */
    generateOfferLetter: async (id: number): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/applications/${id}/offer-letter`);
        return response.data;
    },

    /**
     * Initiate payment
     */
    initiatePayment: async (id: number, amount: number): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/applications/${id}/payment`, { amount });
        return response.data;
    },

    /**
     * Verify payment
     */
    verifyPayment: async (id: number, paymentId: string, signature: string): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/applications/${id}/payment/verify`, {
            payment_id: paymentId,
            signature
        });
        return response.data;
    },

    /**
     * Get application activity log
     */
    getActivity: async (id: number): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/applications/${id}/activity`);
        return response.data;
    },
};

export default admissionApi;
