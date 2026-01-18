/**
 * Exam Management Types
 */

// Internal Exam Types
export interface InternalExam {
    id: number;
    program_id: number;
    year: number;
    semester: number;
    exam_type: 'mid1' | 'mid2' | 'assignment' | 'quiz' | 'practical' | 'seminar';
    exam_name: string;
    academic_year: string;
    start_date: string;
    end_date: string;
    max_marks: number;
    passing_marks: number;
    weightage: number;
    is_published: boolean;
    published_at?: string;
    created_at: string;
    updated_at: string;
}

export interface InternalExamMarks {
    id: number;
    exam_id: number;
    student_id: number;
    subject_id: number;
    marks_obtained: number;
    grade?: string;
    remarks?: string;
    entered_by: number;
    entered_at: string;
    created_at: string;
    updated_at: string;
}

// Hall Ticket Types
export interface HallTicketConfig {
    id: number;
    config_name: string;
    exam_type: string;
    academic_year: string;
    start_date: string;
    end_date: string;
    instructions?: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface HallTicket {
    id: number;
    config_id: number;
    student_id: number;
    hall_ticket_number: string;
    qr_code_data: string;
    qr_code_url?: string;
    pdf_url?: string;
    is_eligible: boolean;
    ineligibility_reason?: string;
    generated_at: string;
    created_at: string;
}

// University Exam Types
export interface UniversityExam {
    id: number;
    exam_name: string;
    exam_code: string;
    academic_year: string;
    semester: number;
    start_date: string;
    end_date: string;
    registration_start_date: string;
    registration_end_date: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface UniversityExamRegistration {
    id: number;
    exam_id: number;
    student_id: number;
    registration_number: string;
    subjects: number[];
    registration_fee: number;
    payment_status: string;
    registration_date: string;
    created_at: string;
    updated_at: string;
}

export interface UniversityExamResult {
    id: number;
    exam_id: number;
    student_id: number;
    subject_id: number;
    internal_marks: number;
    external_marks: number;
    total_marks: number;
    grade: string;
    grade_points: number;
    result_status: 'pass' | 'fail' | 'absent';
    created_at: string;
    updated_at: string;
}

export interface Transcript {
    id: number;
    student_id: number;
    transcript_number: string;
    cgpa: number;
    total_credits: number;
    pdf_url?: string;
    generated_at: string;
    created_at: string;
}

// Request types
export interface InternalExamCreate {
    program_id: number;
    year: number;
    semester: number;
    exam_type: string;
    exam_name: string;
    academic_year: string;
    start_date: string;
    end_date: string;
    max_marks: number;
    passing_marks: number;
    weightage: number;
}

export interface MarksEntryRequest {
    marks: Array<{
        student_id: number;
        subject_id: number;
        marks_obtained: number;
    }>;
}

export interface UniversityExamRegistrationRequest {
    exam_id: number;
    student_id: number;
    subjects: number[];
}
