/**
 * Fee Management API Service
 * 
 * Provides methods to interact with fee management endpoints
 */
import axios from '@/lib/axios';
import type {
    FeeStructure,
    FeeStructureCreate,
    StudentFee,
    StudentFeeCreate,
    FeePayment,
    FeePaymentCreate,
    FeeConcession,
    FeeConcessionCreate,
    StudentFeeSummary,
    FeeDefaulter,
    FeeStructureFilters,
    StudentFeeFilters,
    PaymentFilters
} from '@/types/fee';

const BASE_URL = '/api/v1/fees';

// ============================================================================
// Fee Structure APIs
// ============================================================================

export const feeStructureApi = {
    /**
     * Create a new fee structure
     */
    create: async (data: FeeStructureCreate): Promise<FeeStructure> => {
        const response = await axios.post(`${BASE_URL}/structures`, data);
        return response.data;
    },

    /**
     * List fee structures with optional filters
     */
    list: async (filters?: FeeStructureFilters): Promise<FeeStructure[]> => {
        const response = await axios.get(`${BASE_URL}/structures`, { params: filters });
        return response.data;
    },

    /**
     * Get a specific fee structure
     */
    get: async (id: number): Promise<FeeStructure> => {
        const response = await axios.get(`${BASE_URL}/structures/${id}`);
        return response.data;
    },

    /**
     * Update a fee structure
     */
    update: async (id: number, data: Partial<FeeStructureCreate>): Promise<FeeStructure> => {
        const response = await axios.put(`${BASE_URL}/structures/${id}`, data);
        return response.data;
    },

    /**
     * Delete a fee structure
     */
    delete: async (id: number): Promise<void> => {
        await axios.delete(`${BASE_URL}/structures/${id}`);
    },
};

// ============================================================================
// Student Fee APIs
// ============================================================================

export const studentFeeApi = {
    /**
     * Assign fee structure to a student
     */
    assign: async (data: StudentFeeCreate): Promise<StudentFee> => {
        const response = await axios.post(`${BASE_URL}/student-fees`, data);
        return response.data;
    },

    /**
     * List student fees with optional filters
     */
    list: async (filters?: StudentFeeFilters): Promise<StudentFee[]> => {
        const response = await axios.get(`${BASE_URL}/student-fees`, { params: filters });
        return response.data;
    },

    /**
     * Get a specific student fee
     */
    get: async (id: number): Promise<StudentFee> => {
        const response = await axios.get(`${BASE_URL}/student-fees/${id}`);
        return response.data;
    },

    /**
     * Get fee summary for a student
     */
    getSummary: async (studentId: number, academicYear?: string): Promise<StudentFeeSummary> => {
        const params = academicYear ? { academic_year: academicYear } : {};
        const response = await axios.get(`${BASE_URL}/students/${studentId}/fee-summary`, { params });
        return response.data;
    },

    /**
     * Get installments for a student fee
     */
    getInstallments: async (studentFeeId: number): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/student-fees/${studentFeeId}/installments`);
        return response.data;
    },

    /**
     * Generate installments for a student fee
     */
    generateInstallments: async (studentFeeId: number): Promise<any[]> => {
        const response = await axios.post(`${BASE_URL}/student-fees/${studentFeeId}/generate-installments`);
        return response.data;
    },
};

// ============================================================================
// Payment APIs
// ============================================================================

export const paymentApi = {
    /**
     * Record a fee payment
     */
    record: async (data: FeePaymentCreate): Promise<FeePayment> => {
        const response = await axios.post(`${BASE_URL}/payments`, data);
        return response.data;
    },

    /**
     * List payments with optional filters
     */
    list: async (filters?: PaymentFilters): Promise<FeePayment[]> => {
        const response = await axios.get(`${BASE_URL}/payments`, { params: filters });
        return response.data;
    },

    /**
     * Get a specific payment
     */
    get: async (id: number): Promise<FeePayment> => {
        const response = await axios.get(`${BASE_URL}/payments/${id}`);
        return response.data;
    },
};

// ============================================================================
// Concession APIs
// ============================================================================

export const concessionApi = {
    /**
     * Apply a fee concession
     */
    apply: async (data: FeeConcessionCreate): Promise<FeeConcession> => {
        const response = await axios.post(`${BASE_URL}/concessions`, data);
        return response.data;
    },

    /**
     * List concessions
     */
    list: async (studentFeeId?: number): Promise<FeeConcession[]> => {
        const params = studentFeeId ? { student_fee_id: studentFeeId } : {};
        const response = await axios.get(`${BASE_URL}/concessions`, { params });
        return response.data;
    },
};

// ============================================================================
// Fine Management APIs
// ============================================================================

export const fineApi = {
    /**
     * Calculate fine for an installment
     */
    calculate: async (installmentId: number, finePerDay: number = 10): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/installments/${installmentId}/calculate-fine`, null, {
            params: { fine_per_day: finePerDay }
        });
        return response.data;
    },

    /**
     * Waive fine for an installment
     */
    waive: async (installmentId: number, waiverReason: string): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/installments/${installmentId}/waive-fine`, null, {
            params: { waiver_reason: waiverReason }
        });
        return response.data;
    },
};

// ============================================================================
// Reports & Analytics APIs
// ============================================================================

export const feeReportsApi = {
    /**
     * Get list of fee defaulters
     */
    getDefaulters: async (academicYear?: string, minDueAmount: number = 0): Promise<FeeDefaulter[]> => {
        const params: any = { min_due_amount: minDueAmount };
        if (academicYear) params.academic_year = academicYear;

        const response = await axios.get(`${BASE_URL}/reports/defaulters`, { params });
        return response.data;
    },

    /**
     * Get collection summary for an academic year
     */
    getCollectionSummary: async (academicYear: string): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/reports/collection-summary`, {
            params: { academic_year: academicYear }
        });
        return response.data;
    },
};

// ============================================================================
// Unified Fee API Export
// ============================================================================

export const feeApi = {
    structures: feeStructureApi,
    studentFees: studentFeeApi,
    payments: paymentApi,
    concessions: concessionApi,
    fines: fineApi,
    reports: feeReportsApi,
};

export default feeApi;
