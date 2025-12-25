export enum ApplicationStatus {
    PENDING_PAYMENT = "PENDING_PAYMENT",
    PAYMENT_FAILED = "PAYMENT_FAILED",
    PAID = "PAID",
    FORM_COMPLETED = "FORM_COMPLETED",
    UNDER_REVIEW = "UNDER_REVIEW",
    APPROVED = "APPROVED",
    ADMITTED = "ADMITTED",
    REJECTED = "REJECTED",
    WITHDRAWN = "WITHDRAWN"
}

export enum ApplicationPaymentStatus {
    PENDING = "PENDING",
    SUCCESS = "SUCCESS",
    FAILED = "FAILED"
}

export interface Application {
    id: number;
    application_number: string;
    name: string;
    email: string;
    phone: string;
    gender: string;
    program_id: number;
    state: string;
    board: string;
    group_of_study: string;
    status: ApplicationStatus;
    created_at: string;
    updated_at: string;

    // Full fields (optional)
    aadhaar_number?: string;
    father_name?: string;
    father_phone?: string;
    address?: string;
    previous_marks_percentage?: number;
    applied_for_scholarship: boolean;
    hostel_required: boolean;

    student_id?: number;
}

export interface QuickApplyData {
    name: string;
    email: string;
    phone: string;
    gender: string;
    program_id: number;
    state: string;
    board: string;
    group_of_study: string;
}

export interface FullApplicationData {
    aadhaar_number?: string;
    father_name?: string;
    father_phone?: string;
    address?: string;
    previous_marks_percentage?: number;
    applied_for_scholarship?: boolean;
    hostel_required?: boolean;
}
