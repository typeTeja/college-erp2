/**
 * HR & Payroll API Service
 * 
 * Provides methods to interact with HR endpoints
 */
import { api } from '@/utils/api';

export const hrApi = {
    /**
     * Get all employees
     */
    listEmployees: async (filters?: { department?: string }): Promise<any[]> => {
        const response = await api.get('/hr/employees', { params: filters });
        return response.data;
    },

    /**
     * Mark attendance
     */
    markAttendance: async (data: {
        employee_id: number;
        date: string;
        status: string;
    }): Promise<any> => {
        const response = await api.post('/hr/attendance', data);
        return response.data;
    },

    /**
     * Apply for leave
     */
    applyLeave: async (data: {
        employee_id: number;
        leave_type: string;
        from_date: string;
        to_date: string;
        reason: string;
    }): Promise<any> => {
        const response = await api.post('/hr/leave', data);
        return response.data;
    },

    /**
     * Approve leave
     */
    approveLeave: async (leaveId: number): Promise<any> => {
        const response = await api.post(`/hr/leave/${leaveId}/approve`);
        return response.data;
    },

    /**
     * Generate salary slip
     */
    generateSalarySlip: async (data: {
        employee_id: number;
        month: number;
        year: number;
    }): Promise<any> => {
        const response = await api.post('/hr/salary', data);
        return response.data;
    },

    /**
     * Get HR statistics
     */
    getStatistics: async (): Promise<any> => {
        const response = await api.get('/hr/statistics');
        return response.data;
    },
};

export default hrApi;
