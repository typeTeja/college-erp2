export interface Department {
    id: number;
    department_name: string;
    department_code: string;
    description?: string;
    hod_faculty_id?: number;
    is_active: boolean;
    created_at: string;
}

export interface DepartmentCreateData {
    department_name: string;
    department_code: string;
    description?: string;
    hod_faculty_id?: number;
}

export interface Designation {
    id: number;
    name: string;
    code: string;
    level: number;
    department_id?: number;
    min_experience_years: number;
    min_qualification?: string;
    is_teaching: boolean;
    is_active: boolean;
    display_order: number;
    created_at: string;
}

export interface DesignationCreateData {
    name: string;
    code: string;
    level?: number;
    department_id?: number;
    min_experience_years?: number;
    min_qualification?: string;
    is_teaching?: boolean;
    display_order?: number;
}
