// Entrance Exam Types

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
    subjects?: SubjectConfig[];
    is_active: boolean;
    registration_open: boolean;
    registration_deadline?: string;
    created_at: string;
    updated_at: string;
}

export interface SubjectConfig {
    name: string;
    marks: number;
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

export interface SubjectMarks {
    subject: string;
    max: number;
    secured: number;
}

export interface EntranceExamResult {
    id: number;
    admission_id: number;
    test_config_id: number;
    scholarship_slab_id?: number;
    hall_ticket_number: string;
    student_name: string;
    program_code: string;

    // Marks
    total_max_marks: number;
    total_secured_marks: number;
    entrance_percentage: number;
    subject_marks?: SubjectMarks[];

    // Previous qualification
    previous_percentage: number;

    // Points calculation
    entrance_points: number;
    previous_points: number;
    total_points: number;
    average_points: number;
    entrance_weightage: number;
    previous_weightage: number;

    // Scholarship
    scholarship_amount?: number;
    scholarship_percentage?: number;

    // Status
    result_status: string;
    remarks?: string;

    // OMR
    omr_sheet_number?: string;
    omr_sheet_url?: string;

    // Tracking
    entered_by?: number;
    entered_at?: string;
    verified_by?: number;
    verified_at?: string;
    created_at: string;
    updated_at: string;
}

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
    subjects?: SubjectConfig[];
}

export interface ScholarshipSlabCreate {
    slab_name: string;
    slab_code: string;
    min_points: number;
    max_points: number;
    scholarship_percentage: number;
    description?: string;
    program_ids?: number[];
    academic_year: string;
}

export interface EntranceExamResultCreate {
    admission_id: number;
    test_config_id: number;
    hall_ticket_number: string;
    student_name: string;
    program_code: string;
    total_max_marks: number;
    total_secured_marks: number;
    entrance_percentage: number;
    previous_percentage: number;
    subject_marks?: SubjectMarks[];
    entrance_weightage?: number;
    previous_weightage?: number;
    omr_sheet_number?: string;
    omr_sheet_url?: string;
}

export interface BulkResultEntry {
    hall_ticket_number: string;
    total_secured_marks: number;
    subject_marks?: SubjectMarks[];
}

export interface BulkResultUpload {
    test_config_id: number;
    results: BulkResultEntry[];
}

export interface ScholarshipCalculation {
    result_id: number;
    entrance_points: number;
    previous_points: number;
    total_points: number;
    average_points: number;
    scholarship_slab_id?: number;
    scholarship_slab_name?: string;
    scholarship_percentage: number;
    scholarship_amount: number;
    base_fee: number;
    final_fee: number;
}
