import { api } from "./api";
import {
    Exam, CreateExamDTO,
    ExamSchedule, CreateScheduleDTO,
    ExamResult, BulkMarksEntryDTO
} from "@/types/exam";

export const examService = {
    // --- Exam Management ---
    getExams: async (semesterId?: number) => {
        const params = semesterId ? { semester_id: semesterId } : {};
        const response = await api.get<Exam[]>("/exams", { params });
        return response.data;
    },

    getExam: async (id: number) => {
        const response = await api.get<Exam>(`/exams/${id}`);
        return response.data;
    },

    createExam: async (data: CreateExamDTO) => {
        const response = await api.post<Exam>("/exams", data);
        return response.data;
    },

    // --- Schedule Management ---
    getSchedules: async (examId: number) => {
        const response = await api.get<ExamSchedule[]>(`/exams/${examId}/schedules`);
        return response.data;
    },

    createSchedule: async (examId: number, data: CreateScheduleDTO) => {
        const response = await api.post<ExamSchedule>(`/exams/${examId}/schedules`, data);
        return response.data;
    },

    getEnrolledStudents: async (scheduleId: number) => {
        const response = await api.get<{ id: number, name: string, admission_number: string }[]>(`/exams/${scheduleId}/students`);
        return response.data;
    },

    // --- Marks Management ---
    bulkEnterMarks: async (data: BulkMarksEntryDTO) => {
        const response = await api.post<ExamResult[]>("/exams/marks/bulk", data);
        return response.data;
    },

    getStudentResults: async (studentId: number) => {
        const response = await api.get<ExamResult[]>(`/exams/student/${studentId}/results`);
        return response.data;
    },
};
