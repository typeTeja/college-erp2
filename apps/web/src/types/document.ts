/**
 * Document Management Types
 */

export interface DocumentCategory {
    id: number;
    name: string;
    code: string;
    description?: string;
    is_required: boolean;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface StudentDocument {
    id: number;
    student_id: number;
    category_id: number;
    file_name: string;
    file_path: string;
    file_size: number;
    file_type: string;
    verification_status: 'pending' | 'verified' | 'rejected';
    verified_by?: number;
    verified_at?: string;
    rejection_reason?: string;
    metadata?: Record<string, any>;
    uploaded_at: string;
    created_at: string;
    updated_at: string;
}

export interface DocumentVerification {
    id: number;
    document_id: number;
    verified_by: number;
    verification_status: 'verified' | 'rejected';
    remarks?: string;
    verified_at: string;
    created_at: string;
}

// Request types
export interface DocumentUploadRequest {
    student_id: number;
    category_id: number;
    file: File;
    metadata?: Record<string, any>;
}

export interface DocumentVerificationRequest {
    verified: boolean;
    remarks?: string;
}
