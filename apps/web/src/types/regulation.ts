export interface Regulation {
    id: number;
    regulation_code: string;
    regulation_name: string;
    program_id: number;
    is_active: boolean;
    is_locked: boolean;
    version: number;
    year1_to_year2_min_percentage: number;
    year2_to_year3_min_year2_percentage: number;
    year3_to_graduation_min_percentage: number;
    min_internal_pass: number;
    min_external_pass: number;
    min_total_pass: number;
    theory_max_marks: number;
    theory_internal_max: number;
    theory_external_max: number;
    theory_pass_percentage: number;
    practical_max_marks: number;
    practical_internal_max: number;
    practical_external_max: number;
    practical_pass_percentage: number;
    created_at: string;
    updated_at: string;
}

export interface RegulationCreate {
    regulation_code: string;
    regulation_name: string;
    program_id: number;
    promotion_model?: string; // Default CREDIT_BASED
    year1_to_year2_min_percentage?: number;
    year2_to_year3_min_year2_percentage?: number;
    year3_to_graduation_min_percentage?: number;
    min_internal_pass?: number;
    min_external_pass?: number;
    min_total_pass?: number;
    // Theory Config
    theory_max_marks?: number;
    theory_internal_max?: number;
    theory_external_max?: number;
    theory_pass_percentage?: number;
    // Practical Config
    practical_max_marks?: number;
    practical_internal_max?: number;
    practical_external_max?: number;
    practical_pass_percentage?: number;
    is_active?: boolean;
}
