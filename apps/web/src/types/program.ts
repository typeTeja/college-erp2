export enum ProgramType {
    UG = "UG",
    PG = "PG",
    DIPLOMA = "DIPLOMA",
    CERTIFICATE = "CERTIFICATE",
    PHD = "PHD"
}

export enum ProgramStatus {
    DRAFT = "DRAFT",
    ACTIVE = "ACTIVE",
    ARCHIVED = "ARCHIVED"
}

export interface Semester {
    id: number;
    name: string;
    semester_number: number;
    is_internship: boolean;
    is_project_semester: boolean;
    start_month?: number;
    end_month?: number;
}

export interface ProgramYear {
    id: number;
    name: string;
    year_number: number;
    is_active: boolean;
    semesters: Semester[];
}

export interface Program {
    id: number;
    code: string;
    name: string;
    program_type: ProgramType;
    status: ProgramStatus;
    duration_years: number;
    description?: string;
    department_id: number;
    department_name: string;
    eligibility_criteria?: string;
    program_outcomes?: string;
    total_credits: number;
    is_active: boolean;
    years?: ProgramYear[];
}

export interface ProgramCreateData {
    code: string;
    name: string;
    program_type: ProgramType;
    duration_years: number;
    department_id: number;
    description?: string;
    eligibility_criteria?: string;
    program_outcomes?: string;
    total_credits?: number;
}
