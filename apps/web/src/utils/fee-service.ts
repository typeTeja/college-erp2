import { api } from './api';
import type {
    FeeStructureRead,
    FeeStructureCreate,
    StudentFee,
    StudentFeeCreate,
    StudentFeeSummary,
    FeePaymentRead,
    FeePaymentCreate,
    PaymentInitiateRequest,
    PaymentInitiateResponse,
    FeeConcession,
    FeeConcessionCreate,
    FeeFine,
    FeeFineCreate,
    FeeDefaulter,
} from '@/types/fee';

// ============================================================================
// Fee Structure API
// ============================================================================

export const feeStructureApi = {
    /**
     * Create a new fee structure
     */
    create: async (data: FeeStructureCreate): Promise<FeeStructureRead> => {
        const response = await api.post<FeeStructureRead>('/fees/structures', data);
        return response.data;
    },

    /**
     * Get all fee structures with optional filters
     */
    list: async (params?: {
        program_id?: number;
        academic_year?: string;
    }): Promise<FeeStructureRead[]> => {
        const response = await api.get<FeeStructureRead[]>('/fees/structures', { params });
        return response.data;
    },

    /**
     * Get a specific fee structure by ID
     */
    get: async (structureId: number): Promise<FeeStructureRead> => {
        const response = await api.get<FeeStructureRead>(`/fees/structures/${structureId}`);
        return response.data;
    },
};

// ============================================================================
// Student Fee API
// ============================================================================

export const studentFeeApi = {
    /**
     * Assign a fee structure to a student
     */
    assign: async (data: StudentFeeCreate): Promise<StudentFee> => {
        const response = await api.post<StudentFee>('/fees/student-fees', data);
        return response.data;
    },

    /**
     * Get detailed fee summary for a student
     */
    getSummary: async (
        studentId: number,
        academicYear?: string
    ): Promise<StudentFeeSummary> => {
        const params = academicYear ? { academic_year: academicYear } : {};
        const response = await api.get<StudentFeeSummary>(
            `/fees/student/${studentId}`,
            { params }
        );
        return response.data;
    },
};

// ============================================================================
// Payment API
// ============================================================================

export const paymentApi = {
    /**
     * Record an offline/manual fee payment
     */
    recordPayment: async (data: FeePaymentCreate): Promise<FeePaymentRead> => {
        const response = await api.post<FeePaymentRead>('/fees/payments', data);
        return response.data;
    },

    /**
     * Initiate an online payment via payment gateway
     */
    initiatePayment: async (
        data: PaymentInitiateRequest
    ): Promise<PaymentInitiateResponse> => {
        const response = await api.post<PaymentInitiateResponse>(
            '/fees/payments/initiate',
            data
        );
        return response.data;
    },

    /**
     * Handle payment webhook (typically called by payment gateway)
     */
    handleWebhook: async (data: {
        transaction_id: string;
        status: string;
        amount: number;
    }): Promise<{ message: string }> => {
        const response = await api.post<{ message: string }>(
            '/fees/payments/webhook',
            data
        );
        return response.data;
    },
};

// ============================================================================
// Concession API
// ============================================================================

export const concessionApi = {
    /**
     * Apply a fee concession to a student
     */
    apply: async (data: FeeConcessionCreate): Promise<FeeConcession> => {
        const response = await api.post<FeeConcession>('/fees/concessions', data);
        return response.data;
    },
};

// ============================================================================
// Fine API
// ============================================================================

export const fineApi = {
    /**
     * Apply a late payment fine to a student
     */
    apply: async (data: FeeFineCreate): Promise<FeeFine> => {
        const response = await api.post<FeeFine>('/fees/fines', data);
        return response.data;
    },
};

// ============================================================================
// Defaulters API
// ============================================================================

export const defaultersApi = {
    /**
     * Get list of fee defaulters
     */
    list: async (academicYear?: string): Promise<FeeDefaulter[]> => {
        const params = academicYear ? { academic_year: academicYear } : {};
        const response = await api.get<FeeDefaulter[]>('/fees/defaulters', { params });
        return response.data;
    },
};

// ============================================================================
// Combined Export
// ============================================================================

export const feeService = {
    structures: feeStructureApi,
    studentFees: studentFeeApi,
    payments: paymentApi,
    concessions: concessionApi,
    fines: fineApi,
    defaulters: defaultersApi,
};
