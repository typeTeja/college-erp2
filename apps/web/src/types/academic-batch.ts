
export interface BatchSemester {
    id: number;
    batch_id: number;
    program_year_id: number;
    program_year: number; // 1, 2, 3
    semester_no: number; // 1, 2, 3, 4
    semester_name: string; // "Semester 1"
    total_credits: number;
    min_credits_to_pass: number;
    start_date?: string;
    end_date?: string;
    is_active: boolean;
    sections?: Section[];
    practical_batches?: PracticalBatch[];
}

export interface BatchSubject {
    id: number;
    batch_id: number;
    subject_id: number;
    semester_no: number;
    subject_code: string;
    subject_name: string;
    credits: number;
    subject_type: string;
    is_elective: boolean;
}

export interface Section {
    id: number;
    name: string; // "Section A"
    code: string; // "A"
    batch_semester_id: number;
    batch_id: number;
    max_strength: number;
    current_strength: number;
    is_active: boolean;
    // practical_batches removed
}

export interface PracticalBatch {
    id: number;
    name: string; // "Lab Batch A1"
    code: string; // "L1"
    batch_semester_id: number; // Linked to semester
    // section_id removed
    max_strength: number;
    current_strength: number;
    is_active: boolean;
}
