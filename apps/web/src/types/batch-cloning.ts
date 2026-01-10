/**
 * Batch Cloning Types
 */

export interface CloneOptions {
    clone_faculty_assignments: boolean;
    section_capacity_multiplier: number;
    lab_capacity_multiplier: number;
    custom_batch_name?: string;
}

export interface BatchCloneRequest {
    new_joining_year: number;
    new_regulation_id: number;
    clone_options: CloneOptions;
}

export interface BatchCloneResponse {
    batch_id: number;
    batch_code: string;
    batch_name: string;
    source_batch_id: number;
    years_created: number;
    semesters_created: number;
    sections_created: number;
    labs_created: number;
    message: string;
}
