export interface Student {
    id: number;
    user_id?: number;
    admission_number: string;
    name: string;
    dob?: string;
    gender?: string;
    address?: string;
    phone?: string;
    email?: string;
    program_id?: number;
    batch_semester_id?: number;
    current_year?: number;
    current_semester?: number; // 1, 2, 3 etc.
    section?: string;
    roll_number?: string;
    status: string;
    program_name?: string;
}
