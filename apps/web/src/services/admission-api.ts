/**
 * Admission Management API Service - v1.0.0
 * 
 * Provides typed methods to interact with admission/application endpoints.
 * 
 * CONTRACT VERSION: v1.0.0
 * STATUS: FROZEN (2026-02-03)
 */

import { api } from '@/utils/api';
import type {
  ApplicationCreate,
  ApplicationRead,
  ApplicationUpdate,
  ApplicationPaymentCreate,
  ApplicationPaymentRead,
  ApplicationDocument,
  ActivityLog,
  QuickApplyRequest,
  QuickApplyResponse,
  PaymentConfigResponse,
  OfflinePaymentVerifyRequest,
  DocumentVerifyRequest,
  PaymentInitiateRequest,
  PaymentInitiateResponse,
} from '@/types/admissions';

const BASE_URL = '/admissions';

// ============================================================================
// Application APIs
// ============================================================================

export const admissionApi = {
  /**
   * Create a new application
   */
  create: async (data: ApplicationCreate): Promise<ApplicationRead> => {
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
  }): Promise<ApplicationRead[]> => {
    const response = await api.get(`${BASE_URL}/applications`, { params: filters });
    return response.data;
  },

  /**
   * Get a specific application
   */
  get: async (id: number): Promise<ApplicationRead> => {
    const response = await api.get(`${BASE_URL}/${id}`);
    return response.data;
  },

  /**
   * Update an application
   */
  update: async (id: number, data: ApplicationUpdate): Promise<ApplicationRead> => {
    const response = await api.put(`${BASE_URL}/${id}`, data);
    return response.data;
  },

  /**
   * Soft delete an application
   */
  delete: async (id: number, reason: string): Promise<{ message: string }> => {
    const response = await api.delete(`${BASE_URL}/v2/applications/${id}`, { params: { reason } });
    return response.data;
  },

  /**
   * Restore a deleted application
   */
  restore: async (id: number): Promise<ApplicationRead> => {
    const response = await api.post(`${BASE_URL}/v2/applications/${id}/restore`);
    return response.data;
  },

  /**
   * Bulk cleanup of test data
   */
  cleanupTestData: async (): Promise<{ deleted_count: number; message: string }> => {
    const response = await api.post(`${BASE_URL}/v2/applications/cleanup/test-data`);
    return response.data;
  },

  // ============================================================================
  // Document APIs
  // ============================================================================

  /**
   * Upload application document
   */
  uploadDocument: async (
    id: number,
    file: File,
    documentType: string
  ): Promise<ApplicationDocument> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);

    const response = await api.post(`${BASE_URL}/applications/${id}/documents`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  /**
   * Verify a document
   */
  verifyDocument: async (
    applicationId: number,
    documentId: number,
    data: DocumentVerifyRequest
  ): Promise<ApplicationDocument> => {
    const response = await api.post(
      `${BASE_URL}/applications/${applicationId}/documents/${documentId}/verify`,
      data
    );
    return response.data;
  },

  // ============================================================================
  // Generation APIs
  // ============================================================================

  /**
   * Generate hall ticket
   */
  generateHallTicket: async (id: number): Promise<{ url: string }> => {
    const response = await api.post(`${BASE_URL}/applications/${id}/hall-ticket`);
    return response.data;
  },

  /**
   * Generate offer letter
   */
  generateOfferLetter: async (id: number): Promise<{ url: string }> => {
    const response = await api.post(`${BASE_URL}/applications/${id}/offer-letter`);
    return response.data;
  },

  // ============================================================================
  // Payment APIs
  // ============================================================================

  /**
   * Verify payment
   */
  verifyPayment: async (
    id: number,
    paymentId: string,
    signature: string
  ): Promise<ApplicationPaymentRead> => {
    const response = await api.post(`${BASE_URL}/applications/${id}/payment/verify`, {
      payment_id: paymentId,
      signature,
    });
    return response.data;
  },

  /**
   * Verify offline payment (Admin)
   */
  verifyOfflinePayment: async (
    id: number,
    data: OfflinePaymentVerifyRequest
  ): Promise<ApplicationRead> => {
    const response = await api.post(`${BASE_URL}/${id}/payment/offline-verify`, data);
    return response.data;
  },

  /**
   * Initiate payment for an application
   */
  initiatePayment: async (
    id: number
  ): Promise<PaymentInitiateResponse> => {
    const response = await api.post(`${BASE_URL}/applications/${id}/payment/initiate`);
    return response.data;
  },

  // ============================================================================
  // Activity APIs
  // ============================================================================

  /**
   * Get application activity log
   */
  getActivity: async (id: number): Promise<ActivityLog[]> => {
    const response = await api.get(`${BASE_URL}/applications/${id}/activity`);
    return response.data;
  },

  // ============================================================================
  // Enhanced Admission Workflow APIs
  // ============================================================================

  /**
   * Quick Apply v2 - Creates application with auto-account creation
   */
  quickApplyV2: async (data: QuickApplyRequest): Promise<QuickApplyResponse> => {
    const response = await api.post(`${BASE_URL}/v2/quick-apply`, data);
    return response.data;
  },

  /**
   * Get payment configuration
   */
  getPaymentConfig: async (): Promise<PaymentConfigResponse> => {
    const response = await api.get(`${BASE_URL}/payment/config`);
    return response.data;
  },

  /**
   * Get my application (student portal)
   */
  getMyApplication: async (): Promise<ApplicationRead> => {
    const response = await api.get(`${BASE_URL}/my-application`);
    return response.data;
  },

  /**
   * Complete my application (student portal)
   */
  completeMyApplication: async (data: ApplicationUpdate): Promise<ApplicationRead> => {
    const response = await api.put(`${BASE_URL}/my-application/complete`, data);
    return response.data;
  },

  /**
   * Get admission settings (admin only)
   */
  getSettings: async (): Promise<{
    application_fee_enabled: boolean;
    application_fee_amount: number;
    online_payment_enabled: boolean;
    offline_payment_enabled: boolean;
    send_credentials_email: boolean;
    send_credentials_sms: boolean;
    auto_create_student_account: boolean;
    portal_base_url: string;
  }> => {
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
  }): Promise<{ message: string }> => {
    const response = await api.put(`${BASE_URL}/settings`, data);
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
