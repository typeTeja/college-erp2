import { api } from "./api";
import { Student } from "@/types/student";

export const studentService = {
    getAll: async (params?: { program_id?: number; semester_id?: number; search?: string }) => {
        const response = await api.get<Student[]>("/students/", { params });
        return response.data;
    },

    getById: async (id: number) => {
        const response = await api.get<Student>(`/students/${id}/`);
        return response.data;
    }
};
