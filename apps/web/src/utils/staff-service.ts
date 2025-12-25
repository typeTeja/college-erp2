import { api } from "@/utils/api";
import { Staff, StaffCreateDTO, StaffUpdateDTO, Shift, MaintenanceTicket, MaintenanceTicketCreateDTO } from "@/types/staff";

export const staffService = {
    // --- Staff ---
    getAll: async (department?: string) => {
        const params = department ? { department } : {};
        const response = await api.get<Staff[]>("/staff/", { params });
        return response.data;
    },

    create: async (data: StaffCreateDTO) => {
        const response = await api.post<Staff>("/staff/", data);
        return response.data;
    },

    update: async (id: number, data: StaffUpdateDTO) => {
        const response = await api.put<Staff>(`/staff/${id}`, data);
        return response.data;
    },

    delete: async (id: number) => {
        const response = await api.delete(`/staff/${id}`);
        return response.data;
    },

    // --- Shifts ---
    getShifts: async () => {
        const response = await api.get<Shift[]>("/operations/shifts");
        return response.data;
    },

    // --- Tickets ---
    getTickets: async (status?: string) => {
        const params = status ? { status } : {};
        const response = await api.get<MaintenanceTicket[]>("/operations/tickets", { params });
        return response.data;
    },

    createTicket: async (data: MaintenanceTicketCreateDTO) => {
        const response = await api.post<MaintenanceTicket>("/operations/tickets", data);
        return response.data;
    },

    updateTicket: async (id: number, status?: string, assignedTo?: number) => {
        const response = await api.put<MaintenanceTicket>(`/operations/tickets/${id}`, {
            status,
            assigned_to_id: assignedTo
        });
        return response.data;
    }
};
