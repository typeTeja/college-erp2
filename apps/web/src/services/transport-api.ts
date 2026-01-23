/**
 * Transport Management API Service
 * 
 * Provides methods to interact with transport endpoints
 */
import { api } from '@/utils/api';


export const transportApi = {
    /**
     * Get all vehicles
     */
    listVehicles: async (): Promise<any[]> => {
        const response = await api.get(`/vehicles`);
        return response.data;
    },

    /**
     * Get all routes
     */
    listRoutes: async (): Promise<any[]> => {
        const response = await api.get(`/routes`);
        return response.data;
    },

    /**
     * Allocate transport to student
     */
    allocateTransport: async (data: {
        student_id: number;
        route_id: number;
        pickup_point: string;
        from_date: string;
    }): Promise<any> => {
        const response = await api.post(`/allocations`, data);
        return response.data;
    },

    /**
     * Track vehicle
     */
    trackVehicle: async (vehicleId: number): Promise<any> => {
        const response = await api.get(`/vehicles/${vehicleId}/track`);
        return response.data;
    },

    /**
     * Get transport statistics
     */
    getStatistics: async (): Promise<any> => {
        const response = await api.get(`/statistics`);
        return response.data;
    },
};

export default transportApi;
