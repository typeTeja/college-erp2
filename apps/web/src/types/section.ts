export interface Section {
    id: number;
    name: string;
    code: string;
    batch_semester_id: number;
    batch_id?: number;
    faculty_id?: number;
    max_strength: number;
    current_strength: number;
    is_active: boolean;
    created_at: string;
}

export interface SectionUpdate {
    name?: string;
    code?: string;
    max_strength?: number;
    faculty_id?: number | null;
}
