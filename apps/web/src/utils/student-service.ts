import { api } from './api';

export interface Student {
    id: number;
    admission_number: string;
    name: string;
    dob: string | null;
    phone: string | null;
    email: string | null;
    program_name: string;
    program_code: string;
    current_year: number;
    current_semester: number;
    section: string;
    batch: string;
    status: string;
    gender: string;
}

export interface StudentListResponse {
    total: number;
    items: Student[];
    page: number;
    limit: number;
}

export interface StudentFilters {
    page?: number;
    limit?: number;
    search?: string;
    program_id?: number | null;
    batch?: string;
    section?: string;
    status?: string;
}

export const studentService = {
    async getStudents(filters: StudentFilters = {}): Promise<StudentListResponse> {
        const params = new URLSearchParams();
        if (filters.page) params.append('page', filters.page.toString());
        if (filters.limit) params.append('limit', filters.limit.toString());
        if (filters.search) params.append('search', filters.search);
        if (filters.program_id) params.append('program_id', filters.program_id.toString());
        if (filters.batch) params.append('batch', filters.batch);
        if (filters.section) params.append('section', filters.section);
        if (filters.status) params.append('status', filters.status);

        const response = await api.get('/students', { params });
        return response.data;
    },

    async getStudent(id: number): Promise<Student> {
        const response = await api.get(`/students/${id}`);
        return response.data;
    },

    async verifyStudent(id: number): Promise<Student> {
        const response = await api.patch(`/students/${id}/verify`);
        return response.data;
    }
};
