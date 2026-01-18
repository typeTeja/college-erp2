/**
 * Transport Management API Service
 * 
 * Provides methods to interact with transport endpoints
 */
import axios from 'axios';

const BASE_URL = '/api/v1/transport';

export const transportApi = {
    /**
     * Get all vehicles
     */
    listVehicles: async (): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/vehicles`);
        return response.data;
    },

    /**
     * Get all routes
     */
    listRoutes: async (): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/routes`);
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
        const response = await axios.post(`${BASE_URL}/allocations`, data);
        return response.data;
    },

    /**
     * Track vehicle
     */
    trackVehicle: async (vehicleId: number): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/vehicles/${vehicleId}/track`);
        return response.data;
    },

    /**
     * Get transport statistics
     */
    getStatistics: async (): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/statistics`);
        return response.data;
    },
};

export default transportApi;
