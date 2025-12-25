// Fee Management Types

export enum FeeCategory {
    GENERAL = "GENERAL",
    MANAGEMENT = "MANAGEMENT",
    NRI = "NRI",
    SCHOLARSHIP = "SCHOLARSHIP"
}

export enum PaymentMode {
    ONLINE = "ONLINE",
    CASH = "CASH",
    CHEQUE = "CHEQUE",
    DD = "DD",
    UPI = "UPI"
}

export enum PaymentStatus {
    PENDING = "PENDING",
    SUCCESS = "SUCCESS",
    FAILED = "FAILED",
    REFUNDED = "REFUNDED"
}

// ============================================================================
// Fee Structure Types
// ============================================================================

export interface FeeComponent {
    id?: number;
    name: string;
    amount: number;
    is_refundable: boolean;
}

export interface FeeInstallment {
    id?: number;
    installment_number: number;
    amount: number;
    due_date: string; // ISO date
}

export interface FeeStructure {
    id: number;
    program_id: number;
    academic_year: string;
    year: number;
    category: FeeCategory;
    total_amount: number;
    components: FeeComponent[];
    installments: FeeInstallment[];
    created_at: string;
    updated_at: string;
}

export interface FeeStructureCreate {
    program_id: number;
    academic_year: string;
    year: number;
    category: FeeCategory;
    components: FeeComponent[];
    installments: FeeInstallment[];
}

// ============================================================================
// Student Fee Types
// ============================================================================

export interface StudentFee {
    id: number;
    student_id: number;
    fee_structure_id: number;
    academic_year: string;
    total_fee: number;
    concession_amount: number;
    fine_amount: number;
    paid_amount: number;
    balance: number;
    is_blocked: boolean;
    created_at: string;
    updated_at: string;
}

export interface StudentFeeCreate {
    student_id: number;
    fee_structure_id: number;
    academic_year: string;
}

export interface StudentFeeSummary {
    student_id: number;
    student_name: string;
    admission_number: string;
    academic_year: string;
    total_fee: number;
    concession_amount: number;
    fine_amount: number;
    paid_amount: number;
    balance: number;
    is_blocked: boolean;
    installments: InstallmentDetail[];
    payments: PaymentDetail[];
}

export interface InstallmentDetail {
    installment_number: number;
    amount: number;
    due_date: string;
    status: "paid" | "pending" | "overdue";
}

export interface PaymentDetail {
    id: number;
    amount: number;
    payment_mode: PaymentMode;
    payment_date: string | null;
    status: PaymentStatus;
}

// ============================================================================
// Payment Types
// ============================================================================

export interface FeePayment {
    id: number;
    student_fee_id: number;
    amount: number;
    payment_mode: PaymentMode;
    payment_status: PaymentStatus;
    transaction_id?: string;
    reference_number?: string;
    bank_name?: string;
    payment_date?: string;
    created_at: string;
    remarks?: string;
}

export interface FeePaymentCreate {
    student_fee_id: number;
    amount: number;
    payment_mode: PaymentMode;
    reference_number?: string;
    bank_name?: string;
    remarks?: string;
}

export interface PaymentInitiateRequest {
    student_fee_id: number;
    amount: number;
}

export interface PaymentInitiateResponse {
    payment_id: number;
    transaction_id: string;
    payment_url: string;
    amount: number;
}

// ============================================================================
// Concession Types
// ============================================================================

export interface FeeConcession {
    id: number;
    student_fee_id: number;
    concession_type: string;
    amount: number;
    percentage?: number;
    approved_by?: string;
    approved_at?: string;
    remarks?: string;
    created_at: string;
}

export interface FeeConcessionCreate {
    student_fee_id: number;
    concession_type: string;
    amount?: number;
    percentage?: number;
    remarks?: string;
}

// ============================================================================
// Fine Types
// ============================================================================

export interface FeeFine {
    id: number;
    student_fee_id: number;
    installment_number: number;
    fine_amount: number;
    reason: string;
    waived: boolean;
    waived_by?: string;
    waived_at?: string;
    created_at: string;
}

export interface FeeFineCreate {
    student_fee_id: number;
    installment_number: number;
    fine_amount: number;
    reason: string;
}

// ============================================================================
// Defaulter Types
// ============================================================================

export interface FeeDefaulter {
    student_id: number;
    student_name: string;
    admission_number: string;
    program: string;
    year: number;
    total_due: number;
    overdue_installments: number;
    last_payment_date?: string;
    days_overdue: number;
}
