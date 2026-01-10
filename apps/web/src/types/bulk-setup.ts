export interface BulkBatchSetupRequest {
    program_id: number;
    joining_year: number;
    regulation_id: number;
    sections_per_semester: number;
    section_capacity: number;
    labs_per_section: number;
    lab_capacity: number;
    batch_name_override?: string;
}

export interface BulkBatchSetupResponse {
    batch_id: number;
    batch_code: string;
    batch_name: string;
    years_created: number;
    semesters_created: number;
    sections_created: number;
    labs_created: number;
    total_section_capacity: number;
    total_lab_capacity: number;
    message: string;
}
