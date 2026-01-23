/**
 * Hostel Management API Service
 * 
 * Provides methods to interact with hostel endpoints
 */
import { api } from '@/utils/api';


export const hostelApi = {
    /**
     * Get all hostels
     */
    listHostels: async (): Promise<any[]> => {
        const response = await api.get(`/hostels`);
        return response.data;
    },

    /**
     * Get available rooms
     */
    listRooms: async (filters?: {
        hostel_id?: number;
        available?: boolean;
        room_type?: string;
    }): Promise<any[]> => {
        const response = await api.get(`/rooms`, { params: filters });
        return response.data;
    },

    /**
     * Allocate room to student
     */
    allocateRoom: async (data: {
        student_id: number;
        room_id: number;
        from_date: string;
        to_date?: string;
    }): Promise<any> => {
        const response = await api.post(`/allocations`, data);
        return response.data;
    },

    /**
     * Vacate room
     */
    vacateRoom: async (allocationId: number, vacateDate: string): Promise<any> => {
        const response = await api.post(`/allocations/${allocationId}/vacate`, {
            vacate_date: vacateDate
        });
        return response.data;
    },

    /**
     * Log visitor
     */
    logVisitor: async (data: any): Promise<any> => {
        const response = await api.post(`/visitors`, data);
        return response.data;
    },

    /**
     * Create maintenance request
     */
    createMaintenanceRequest: async (data: any): Promise<any> => {
        const response = await api.post(`/maintenance`, data);
        return response.data;
    },

    /**
     * Get hostel statistics
     */
    getStatistics: async (hostelId?: number): Promise<any> => {
        const response = await api.get(`/statistics`, {
            params: { hostel_id: hostelId }
        });
        return response.data;
    },
};

export default hostelApi;
