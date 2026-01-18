/**
 * Enhanced Admission Types
 * Types for RCMS admission features
 */

export interface EntranceTestConfig {
    id: number;
    test_name: string;
    test_code: string;
    academic_year: string;
    program_ids?: number[];
    test_date: string;
    test_time: string;
    test_duration_minutes: number;
    reporting_time: string;
    venue_name: string;
    venue_address: string;
    venue_instructions?: string;
    guidelines?: string;
    documents_required?: string[];
    total_marks: number;
    subjects?: SubjectMarks[];
    is_active: boolean;
    registration_open: boolean;
    registration_deadline?: string;
    created_at: string;
    updated_at: string;
    created_by?: number;
}

export interface SubjectMarks {
    subject_name: string;
    max_marks: number;
}

export interface TentativeAdmission {
    id: number;
    application_id: number;
    scholarship_slab: string;
    scholarship_amount: number;
    base_annual_fee: number;
    net_annual_fee: number;
    first_installment_amount: number;
    admission_letter_url?: string;
    payment_link?: string;
    valid_until: string;
    status: string;
    created_at: string;
    updated_at: string;
}

export interface ScholarshipCalculation {
    id: number;
    application_id: number;
    previous_percentage: number;
    entrance_percentage: number;
    final_merit_score: number;
    scholarship_slab: string;
    scholarship_amount: number;
    calculation_date: string;
    created_at: string;
}

export interface EntranceExamResult {
    id: number;
    admission_id: number;
    test_config_id: number;
    scholarship_slab_id?: number;
    hall_ticket_number: string;
    student_name: string;
    program_code: string;
    total_max_marks: number;
    total_secured_marks: number;
    entrance_percentage: number;
    subject_marks?: Record<string, number>;
    previous_percentage: number;
    entrance_points: number;
    previous_points: number;
    total_points: number;
    average_points: number;
    entrance_weightage: number;
    previous_weightage: number;
    scholarship_amount?: number;
    scholarship_percentage?: number;
    result_status: string;
    remarks?: string;
    omr_sheet_number?: string;
    omr_sheet_url?: string;
    entered_by?: number;
    entered_at?: string;
    verified_by?: number;
    verified_at?: string;
    created_at: string;
    updated_at: string;
}

export interface ScholarshipSlab {
    id: number;
    slab_name: string;
    slab_code: string;
    min_points: number;
    max_points: number;
    scholarship_percentage: number;
    description?: string;
    program_ids?: number[];
    academic_year: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

// Request types
export interface EntranceTestConfigCreate {
    test_name: string;
    test_code: string;
    academic_year: string;
    program_ids?: number[];
    test_date: string;
    test_time: string;
    test_duration_minutes?: number;
    reporting_time?: string;
    venue_name: string;
    venue_address: string;
    venue_instructions?: string;
    guidelines?: string;
    documents_required?: string[];
    total_marks?: number;
    subjects?: SubjectMarks[];
    registration_deadline?: string;
}

export interface TentativeAdmissionCreate {
    application_id: number;
    scholarship_slab: string;
    scholarship_amount: number;
    base_annual_fee: number;
    net_annual_fee: number;
    first_installment_amount: number;
    valid_until: string;
}

export interface ScholarshipCalculationCreate {
    application_id: number;
    previous_percentage: number;
    entrance_percentage: number;
}
