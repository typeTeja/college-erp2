export interface DashboardLabGroup {
    id: number;
    name: string;
    code: string;
    max_strength: number;
    current_strength: number;
    utilization_percentage: number;
}

export interface DashboardSection {
    id: number;
    name: string;
    code: string;
    max_strength: number;
    current_strength: number;
    utilization_percentage: number;
    faculty_id?: number;
    faculty_name?: string;
}

export interface DashboardSemester {
    id: number;
    semester_no: number;
    semester_name: string;
    total_credits: number;
    sections: DashboardSection[];
    lab_groups: DashboardLabGroup[];
    total_students: number;
    total_capacity: number;
}

export interface DashboardYear {
    id: number;
    year_no: number;
    year_name: string;
    semesters: DashboardSemester[];
    total_students: number;
    total_capacity: number;
}

export interface DashboardBatch {
    id: number;
    batch_code: string;
    batch_name: string;
    program_id: number;
    program_name: string;
    regulation_id: number;
    regulation_name: string;
    status: string;
    years: DashboardYear[];
    total_students: number;
    total_capacity: number;
    overall_utilization: number;
}

export interface AcademicDashboardResponse {
    batches: DashboardBatch[];
    summary: {
        total_batches: number;
        total_students: number;
        total_capacity: number;
        total_sections: number;
        total_labs: number;
        overall_utilization: number;
    };
}
