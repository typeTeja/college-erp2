import { api } from './api';
import { AcademicDashboardResponse } from '@/types/academic-dashboard';

export const academicDashboardService = {
    /**
     * Get academic dashboard data
     */
    getDashboard: async (params?: {
        program_id?: number;
        batch_id?: number;
    }): Promise<AcademicDashboardResponse> => {
        const response = await api.get<AcademicDashboardResponse>(
            '/academic-setup/dashboard/',
            { params }
        );
        return response.data;
    },
};
