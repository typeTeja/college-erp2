// Extended types for admissions module
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

export enum FeeMode {
    ONLINE = "ONLINE",
    OFFLINE = "OFFLINE"
}

export enum DocumentType {
    PHOTO = "PHOTO",
    AADHAAR = "AADHAAR",
    TENTH_MARKSHEET = "TENTH_MARKSHEET",
    TWELFTH_MARKSHEET = "TWELFTH_MARKSHEET",
    MIGRATION_CERTIFICATE = "MIGRATION_CERTIFICATE",
    TRANSFER_CERTIFICATE = "TRANSFER_CERTIFICATE",
    CASTE_CERTIFICATE = "CASTE_CERTIFICATE",
    INCOME_CERTIFICATE = "INCOME_CERTIFICATE",
    OTHER = "OTHER"
}

export enum DocumentStatus {
    UPLOADED = "UPLOADED",
    VERIFIED = "VERIFIED",
    REJECTED = "REJECTED"
}

export enum ActivityType {
    APPLICATION_CREATED = "APPLICATION_CREATED",
    PAYMENT_INITIATED = "PAYMENT_INITIATED",
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS",
    PAYMENT_FAILED = "PAYMENT_FAILED",
    OFFLINE_PAYMENT_VERIFIED = "OFFLINE_PAYMENT_VERIFIED",
    FORM_COMPLETED = "FORM_COMPLETED",
    DOCUMENT_UPLOADED = "DOCUMENT_UPLOADED",
    DOCUMENT_VERIFIED = "DOCUMENT_VERIFIED",
    DOCUMENT_REJECTED = "DOCUMENT_REJECTED",
    STATUS_CHANGED = "STATUS_CHANGED",
    ADMISSION_CONFIRMED = "ADMISSION_CONFIRMED",
    ADMISSION_REJECTED = "ADMISSION_REJECTED"
}

export interface ApplicationDocument {
    id: number;
    application_id: number;
    document_type: DocumentType;
    file_url: string;
    file_name: string;
    file_size: number;
    status: DocumentStatus;
    rejection_reason?: string;
    verified_by?: number;
    verified_at?: string;
    uploaded_at: string;
}

export interface ActivityLog {
    id: number;
    application_id: number;
    activity_type: ActivityType;
    description: string;
    extra_data?: string;
    performed_by?: number;
    ip_address?: string;
    created_at: string;
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
    fee_mode: FeeMode;
    payment_proof_url?: string;
    offline_payment_verified: boolean;
    offline_payment_verified_by?: number;
    offline_payment_verified_at?: string;
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
    documents?: ApplicationDocument[];
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
    fee_mode: FeeMode;
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

export interface OfflinePaymentVerify {
    payment_proof_url: string;
    verified: boolean;
}

export interface DocumentVerify {
    status: DocumentStatus;
    rejection_reason?: string;
}
