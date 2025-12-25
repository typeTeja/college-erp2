export interface Faculty {
    id: number;
    user_id?: number;
    name: string;
    email?: string;
    phone?: string;
    department?: string;
    designation?: string;
    qualification?: string;
    max_weekly_hours: number;
    subjects?: {
        id: number;
        code: string;
        name: string;
    }[];
}

export interface FacultyCreateDTO {
    name: string;
    email?: string;
    phone?: string;
    department?: string;
    designation?: string;
    qualification?: string;
    max_weekly_hours?: number;
}

export interface FacultyUpdateDTO {
    name?: string;
    email?: string;
    phone?: string;
    department?: string;
    designation?: string;
    qualification?: string;
    max_weekly_hours?: number;
}
