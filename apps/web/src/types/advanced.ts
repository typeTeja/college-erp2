/**
 * Placement, HR & Analytics Types
 */

// Placement Types
export interface Company {
    id: number;
    company_name: string;
    industry: string;
    website?: string;
    contact_person?: string;
    contact_email?: string;
    contact_phone?: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface PlacementDrive {
    id: number;
    company_id: number;
    drive_name: string;
    drive_date: string;
    job_role: string;
    job_description?: string;
    min_cgpa?: number;
    package_offered?: number;
    registration_deadline: string;
    status: 'upcoming' | 'ongoing' | 'completed' | 'cancelled';
    created_at: string;
    updated_at: string;
}

export interface StudentPlacement {
    id: number;
    drive_id: number;
    student_id: number;
    application_status: 'applied' | 'shortlisted' | 'selected' | 'rejected';
    package_offered?: number;
    joining_date?: string;
    created_at: string;
    updated_at: string;
}

export interface TrainingProgram {
    id: number;
    program_name: string;
    description?: string;
    start_date: string;
    end_date: string;
    trainer_name?: string;
    max_participants?: number;
    status: 'upcoming' | 'ongoing' | 'completed';
    created_at: string;
    updated_at: string;
}

export interface Internship {
    id: number;
    student_id: number;
    company_name: string;
    role: string;
    start_date: string;
    end_date: string;
    stipend?: number;
    status: 'ongoing' | 'completed';
    certificate_url?: string;
    created_at: string;
    updated_at: string;
}

// HR Types
export interface Employee {
    id: number;
    employee_code: string;
    name: string;
    email: string;
    phone: string;
    department: string;
    designation: string;
    join_date: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface EmployeeAttendance {
    id: number;
    employee_id: number;
    date: string;
    status: 'present' | 'absent' | 'half_day' | 'leave';
    check_in_time?: string;
    check_out_time?: string;
    created_at: string;
}

export interface EmployeeLeave {
    id: number;
    employee_id: number;
    leave_type: 'casual' | 'sick' | 'earned' | 'unpaid';
    from_date: string;
    to_date: string;
    days: number;
    reason: string;
    status: 'pending' | 'approved' | 'rejected';
    approved_by?: number;
    approved_at?: string;
    created_at: string;
    updated_at: string;
}

export interface SalarySlip {
    id: number;
    employee_id: number;
    month: number;
    year: number;
    basic_salary: number;
    allowances: number;
    deductions: number;
    gross_salary: number;
    net_salary: number;
    pdf_url?: string;
    generated_at: string;
    created_at: string;
}

// Analytics Types
export interface DashboardSummary {
    students: {
        total: number;
        active: number;
        new_admissions: number;
    };
    academics: {
        ongoing_exams: number;
        upcoming_exams: number;
        average_attendance: number;
    };
    finance: {
        total_fees_collected: number;
        pending_fees: number;
        collection_percentage: number;
    };
    placements: {
        total_placed: number;
        placement_percentage: number;
        average_package: number;
    };
}

export interface EnrollmentTrend {
    year: string;
    total_students: number;
    new_admissions: number;
    program_wise: Record<string, number>;
}

export interface FeeAnalytics {
    academic_year: string;
    total_fees: number;
    collected: number;
    pending: number;
    collection_rate: number;
    month_wise_collection: Array<{
        month: string;
        amount: number;
    }>;
}

export interface ExamPerformance {
    program: string;
    semester: number;
    average_marks: number;
    pass_percentage: number;
    grade_distribution: Record<string, number>;
}

// Request types
export interface PlacementApplicationRequest {
    drive_id: number;
    student_id: number;
}

export interface LeaveApplicationRequest {
    employee_id: number;
    leave_type: string;
    from_date: string;
    to_date: string;
    reason: string;
}

export interface SalarySlipGenerateRequest {
    employee_id: number;
    month: number;
    year: number;
}

export interface CustomReportRequest {
    report_type: string;
    filters: Record<string, any>;
}
