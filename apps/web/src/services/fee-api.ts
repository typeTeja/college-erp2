/**
 * Finance Domain API Service - v1.0.0
 * 
 * Provides typed methods to interact with finance/fee endpoints.
 * 
 * CONTRACT VERSION: v1.0.0
 * STATUS: FROZEN (2026-02-03)
 */

import { api } from '@/utils/api';
import type {
  FeeStructureCreate,
  FeeStructureRead,
  FeeStructureFilters,
  FeePaymentCreate,
  FeePaymentRead,
  PaymentInitiateRequest,
  PaymentInitiateResponse,
  PaymentCallbackData,
  OnlinePaymentRead,
  StudentFee,
  StudentFeeCreate,
  StudentFeeSummary,
  StudentFeeFilters,
  FeeConcession,
  FeeConcessionCreate,
  FeeFine,
  FeeFineCreate,
  FeeDefaulter,
  PaymentFilters,
  ScholarshipSlabCreate,
  ScholarshipSlabRead,
} from '@/types/fee';

const BASE_URL = '/finance';

// ============================================================================
// Fee Structure APIs
// ============================================================================

export const feeApi = {
  /**
   * Create fee structure
   */
  createFeeStructure: async (data: FeeStructureCreate): Promise<FeeStructureRead> => {
    const response = await api.post(`${BASE_URL}/fee-structures`, data);
    return response.data;
  },

  /**
   * List fee structures with filters
   */
  listFeeStructures: async (filters?: FeeStructureFilters): Promise<FeeStructureRead[]> => {
    const response = await api.get(`${BASE_URL}/fee-structures`, { params: filters });
    return response.data;
  },

  /**
   * Get fee structure by ID
   */
  getFeeStructure: async (id: number): Promise<FeeStructureRead> => {
    const response = await api.get(`${BASE_URL}/fee-structures/${id}`);
    return response.data;
  },

  /**
   * Update fee structure
   */
  updateFeeStructure: async (
    id: number,
    data: Partial<FeeStructureCreate>
  ): Promise<FeeStructureRead> => {
    const response = await api.put(`${BASE_URL}/fee-structures/${id}`, data);
    return response.data;
  },

  /**
   * Delete fee structure
   */
  deleteFeeStructure: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete(`${BASE_URL}/fee-structures/${id}`);
    return response.data;
  },

  // ============================================================================
  // Student Fee APIs
  // ============================================================================

  /**
   * Create student fee
   */
  createStudentFee: async (data: StudentFeeCreate): Promise<StudentFee> => {
    const response = await api.post(`${BASE_URL}/student-fees`, data);
    return response.data;
  },

  /**
   * List student fees with filters
   */
  listStudentFees: async (filters?: StudentFeeFilters): Promise<StudentFee[]> => {
    const response = await api.get(`${BASE_URL}/student-fees`, { params: filters });
    return response.data;
  },

  /**
   * Get student fee summary
   */
  getStudentFeeSummary: async (studentId: number): Promise<StudentFeeSummary> => {
    const response = await api.get(`${BASE_URL}/student-fees/${studentId}/summary`);
    return response.data;
  },

  /**
   * Get student fee by ID
   */
  getStudentFee: async (id: number): Promise<StudentFee> => {
    const response = await api.get(`${BASE_URL}/student-fees/${id}`);
    return response.data;
  },

  // ============================================================================
  // Payment APIs
  // ============================================================================

  /**
   * Create fee payment
   */
  createPayment: async (data: FeePaymentCreate): Promise<FeePaymentRead> => {
    const response = await api.post(`${BASE_URL}/payments`, data);
    return response.data;
  },

  /**
   * List payments with filters
   */
  listPayments: async (filters?: PaymentFilters): Promise<FeePaymentRead[]> => {
    const response = await api.get(`${BASE_URL}/payments`, { params: filters });
    return response.data;
  },

  /**
   * Get payment by ID
   */
  getPayment: async (id: number): Promise<FeePaymentRead> => {
    const response = await api.get(`${BASE_URL}/payments/${id}`);
    return response.data;
  },

  // ============================================================================
  // Online Payment APIs
  // ============================================================================

  /**
   * Initiate online payment
   */
  initiatePayment: async (data: PaymentInitiateRequest): Promise<PaymentInitiateResponse> => {
    const response = await api.post(`${BASE_URL}/payments/initiate`, data);
    return response.data;
  },

  /**
   * Handle payment callback (webhook)
   */
  handlePaymentCallback: async (data: PaymentCallbackData): Promise<{ status: string }> => {
    const response = await api.post(`${BASE_URL}/payments/callback`, data);
    return response.data;
  },

  /**
   * Get payment status
   */
  getPaymentStatus: async (paymentId: number): Promise<OnlinePaymentRead> => {
    const response = await api.get(`${BASE_URL}/payments/${paymentId}`);
    return response.data;
  },

  /**
   * List student payments
   */
  listStudentPayments: async (
    studentId: number,
    params?: { skip?: number; limit?: number }
  ): Promise<OnlinePaymentRead[]> => {
    const response = await api.get(`${BASE_URL}/payments/student/${studentId}`, { params });
    return response.data;
  },

  // ============================================================================
  // Concession APIs
  // ============================================================================

  /**
   * Create fee concession
   */
  createConcession: async (data: FeeConcessionCreate): Promise<FeeConcession> => {
    const response = await api.post(`${BASE_URL}/concessions`, data);
    return response.data;
  },

  /**
   * List concessions for a student fee
   */
  listConcessions: async (studentFeeId: number): Promise<FeeConcession[]> => {
    const response = await api.get(`${BASE_URL}/concessions`, {
      params: { student_fee_id: studentFeeId },
    });
    return response.data;
  },

  /**
   * Delete concession
   */
  deleteConcession: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete(`${BASE_URL}/concessions/${id}`);
    return response.data;
  },

  // ============================================================================
  // Fine APIs
  // ============================================================================

  /**
   * Create fee fine
   */
  createFine: async (data: FeeFineCreate): Promise<FeeFine> => {
    const response = await api.post(`${BASE_URL}/fines`, data);
    return response.data;
  },

  /**
   * List fines for a student fee
   */
  listFines: async (studentFeeId: number): Promise<FeeFine[]> => {
    const response = await api.get(`${BASE_URL}/fines`, {
      params: { student_fee_id: studentFeeId },
    });
    return response.data;
  },

  /**
   * Waive fine
   */
  waiveFine: async (id: number): Promise<FeeFine> => {
    const response = await api.post(`${BASE_URL}/fines/${id}/waive`);
    return response.data;
  },

  // ============================================================================
  // Scholarship APIs
  // ============================================================================

  /**
   * Create scholarship slab
   */
  createScholarshipSlab: async (data: ScholarshipSlabCreate): Promise<ScholarshipSlabRead> => {
    const response = await api.post(`${BASE_URL}/scholarships`, data);
    return response.data;
  },

  /**
   * List scholarship slabs
   */
  listScholarshipSlabs: async (): Promise<ScholarshipSlabRead[]> => {
    const response = await api.get(`${BASE_URL}/scholarships`);
    return response.data;
  },

  /**
   * Get scholarship slab by ID
   */
  getScholarshipSlab: async (id: number): Promise<ScholarshipSlabRead> => {
    const response = await api.get(`${BASE_URL}/scholarships/${id}`);
    return response.data;
  },

  // ============================================================================
  // Defaulter APIs
  // ============================================================================

  /**
   * Get fee defaulters list
   */
  getDefaulters: async (params?: {
    program_id?: number;
    year?: number;
    min_due_amount?: number;
  }): Promise<FeeDefaulter[]> => {
    const response = await api.get(`${BASE_URL}/defaulters`, { params });
    return response.data;
  },

  // ============================================================================
  // Reports APIs
  // ============================================================================

  /**
   * Get fee collection report
   */
  getCollectionReport: async (params: {
    from_date: string;
    to_date: string;
    program_id?: number;
  }): Promise<{
    total_collected: number;
    total_pending: number;
    payment_mode_breakdown: Record<string, number>;
  }> => {
    const response = await api.get(`${BASE_URL}/reports/collection`, { params });
    return response.data;
  },

  /**
   * Get outstanding fees report
   */
  getOutstandingReport: async (params?: {
    program_id?: number;
    academic_year?: string;
  }): Promise<{
    total_outstanding: number;
    student_count: number;
    breakdown_by_year: Record<string, number>;
  }> => {
    const response = await api.get(`${BASE_URL}/reports/outstanding`, { params });
    return response.data;
  },
};

export default feeApi;
