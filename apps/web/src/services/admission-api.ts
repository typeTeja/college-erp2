/**
 * Admission Management API Service
 * 
 * Provides methods to interact with admission/application endpoints
 */
import { api } from '@/utils/api';

const BASE_URL = '/admissions';

// ============================================================================
// Application APIs
// ============================================================================

export const admissionApi = {
    /**
     * Create a new application
     */
    create: async (data: any): Promise<any> => {
        const response = await api.post(`${BASE_URL}/applications`, data);
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
        show_deleted?: boolean;
    }): Promise<any[]> => {
        const response = await api.get(`${BASE_URL}/applications`, { params: filters });
        return response.data;
    },

    /**
     * Get a specific application
     */
    get: async (id: number): Promise<any> => {
        const response = await api.get(`${BASE_URL}/applications/${id}`);
        return response.data;
    },

    /**
     * Update an application
     */
    update: async (id: number, data: any): Promise<any> => {
        const response = await api.put(`${BASE_URL}/applications/${id}`, data);
        return response.data;
    },

    /**
     * Soft delete an application
     */
    delete: async (id: number, reason: string): Promise<any> => {
        const response = await api.delete(`${BASE_URL}/v2/applications/${id}`, { params: { reason } });
        return response.data;
    },

    /**
     * Restore a deleted application
     */
    restore: async (id: number): Promise<any> => {
        const response = await api.post(`${BASE_URL}/v2/applications/${id}/restore`);
        return response.data;
    },

    /**
     * Bulk cleanup of test data
     */
    cleanupTestData: async (): Promise<any> => {
        const response = await api.post(`${BASE_URL}/v2/applications/cleanup/test-data`);
        return response.data;
    },

    /**
     * Upload application document
     */
    uploadDocument: async (id: number, file: File, documentType: string): Promise<any> => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('document_type', documentType);

        const response = await api.post(`${BASE_URL}/applications/${id}/documents`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },

    /**
     * Verify a document
     */
    verifyDocument: async (applicationId: number, documentId: number, verified: boolean, remarks?: string): Promise<any> => {
        const response = await api.post(`${BASE_URL}/applications/${applicationId}/documents/${documentId}/verify`, {
            verified,
            remarks
        });
        return response.data;
    },

    /**
     * Generate hall ticket
     */
    generateHallTicket: async (id: number): Promise<any> => {
        const response = await api.post(`${BASE_URL}/applications/${id}/hall-ticket`);
        return response.data;
    },

    /**
     * Generate offer letter
     */
    generateOfferLetter: async (id: number): Promise<any> => {
        const response = await api.post(`${BASE_URL}/applications/${id}/offer-letter`);
        return response.data;
    },



    /**
     * Verify payment
     */
    verifyPayment: async (id: number, paymentId: string, signature: string): Promise<any> => {
        const response = await api.post(`${BASE_URL}/applications/${id}/payment/verify`, {
            payment_id: paymentId,
            signature
        });
        return response.data;
    },

    /**
     * Verify offline payment (Admin)
     */
    verifyOfflinePayment: async (id: number, verified: boolean, proofUrl?: string, mode: 'CASH' | 'ONLINE' = 'CASH', transactionId?: string): Promise<any> => {
        const response = await api.post(`${BASE_URL}/${id}/payment/offline-verify`, {
            verified,
            payment_proof_url: proofUrl,
            mode,
            transaction_id: transactionId
        });
        return response.data;
    },

    /**
     * Get application activity log
     */
    getActivity: async (id: number): Promise<any[]> => {
        const response = await api.get(`${BASE_URL}/applications/${id}/activity`);
        return response.data;
    },

    // ============================================================================
    // Enhanced Admission Workflow APIs
    // ============================================================================

    /**
     * Quick Apply v2 - Creates application with auto-account creation
     */
    quickApplyV2: async (data: {
        name: string;
        email: string;
        phone: string;
        gender: string;
        program_id: number;
        state: string;
        board: string;
        group_of_study: string;
    }): Promise<{
        application_number: string;
        portal_username?: string;
        portal_password?: string;
        message: string;
    }> => {
        const response = await api.post(`${BASE_URL}/v2/quick-apply`, data);
        return response.data;
    },

    /**
     * Get payment configuration
     */
    getPaymentConfig: async (): Promise<{
        fee_enabled: boolean;
        fee_amount: number;
        online_enabled: boolean;
        offline_enabled: boolean;
        payment_gateway: string;
    }> => {
        const response = await api.get(`${BASE_URL}/payment-config`);
        return response.data;
    },

    /**
     * Get my application (student portal)
     */
    getMyApplication: async (): Promise<any> => {
        const response = await api.get(`${BASE_URL}/my-application`);
        return response.data;
    },

    /**
     * Complete my application (student portal)
     */
    completeMyApplication: async (data: {
        aadhaar_number?: string;
        father_name?: string;
        father_phone?: string;
        address?: string;
        previous_marks_percentage?: number;
        applied_for_scholarship?: boolean;
        hostel_required?: boolean;
    }): Promise<any> => {
        const response = await api.put(`${BASE_URL}/my-application/complete`, data);
        return response.data;
    },

    /**
     * Get admission settings (admin only)
     */
    getSettings: async (): Promise<any> => {
        const response = await api.get(`${BASE_URL}/settings`);
        return response.data;
    },

    /**
     * Update admission settings (admin only)
     */
    updateSettings: async (data: {
        application_fee_enabled?: boolean;
        application_fee_amount?: number;
        online_payment_enabled?: boolean;
        offline_payment_enabled?: boolean;
        send_credentials_email?: boolean;
        send_credentials_sms?: boolean;
        auto_create_student_account?: boolean;
        portal_base_url?: string;
    }): Promise<any> => {
        const response = await api.put(`${BASE_URL}/settings`, data);
        return response.data;
    },

    /**
     * Initiate payment for an application
     */
    initiatePayment: async (id: number, amount: number): Promise<{
        status: string;
        payment_url: string;
        txnid: string;
    }> => {
        const response = await api.post(`/payment/initiate`, {
            application_id: id,
            amount: amount
            // Removed surl/furl to use backend defaults which point to api/v1/payment/response
        });
        return response.data;
    },

    /**
     * Download receipt (Public)
     */
    downloadReceiptPublic: async (applicationNumber: string): Promise<{ url: string }> => {
        const response = await api.get(`${BASE_URL}/v2/public/receipt/${applicationNumber}`);
        return response.data;
    },
};

export default admissionApi;

