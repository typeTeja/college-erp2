/**
 * Payment Gateway API Service
 * 
 * Provides methods to interact with payment gateway endpoints
 */
import { api } from '@/utils/api';


export const paymentApi = {
    /**
     * Initiate a payment
     */
    initiate: async (data: {
        student_id: number;
        amount: number;
        purpose: string;
        description?: string;
    }): Promise<any> => {
        const response = await api.post(`/initiate`, data);
        return response.data;
    },

    /**
     * Verify payment
     */
    verify: async (paymentId: string, signature: string): Promise<any> => {
        const response = await api.post(`/verify`, {
            payment_id: paymentId,
            signature
        });
        return response.data;
    },

    /**
     * Get payment status
     */
    getStatus: async (paymentId: string): Promise<any> => {
        const response = await api.get(`/${paymentId}/status`);
        return response.data;
    },

    /**
     * Get payment history
     */
    getHistory: async (studentId: number, filters?: {
        status?: string;
        from_date?: string;
        to_date?: string;
    }): Promise<any[]> => {
        const response = await api.get(`/history/${studentId}`, { params: filters });
        return response.data;
    },

    /**
     * Generate payment receipt
     */
    generateReceipt: async (paymentId: string): Promise<any> => {
        const response = await api.post(`/${paymentId}/receipt`);
        return response.data;
    },

    /**
     * Download payment receipt
     */
    downloadReceipt: async (paymentId: string): Promise<Blob> => {
        const response = await api.get(`/${paymentId}/receipt/download`, {
            responseType: 'blob'
        });
        return response.data;
    },
};

export default paymentApi;
