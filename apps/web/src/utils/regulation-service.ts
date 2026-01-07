import { api } from './api';
import { Regulation, RegulationCreate } from '@/types/regulation';

// Base Regulation Operations
export const getRegulations = async (programId?: number, isLocked?: boolean): Promise<Regulation[]> => {
    const params: Record<string, any> = {};
    if (programId) params.program_id = programId;
    if (isLocked !== undefined) params.is_locked = isLocked;

    const response = await api.get('/regulations/', { params });
    return response.data;
};

export const createRegulation = async (data: RegulationCreate): Promise<Regulation> => {
    const response = await api.post('/regulations/', data);
    return response.data;
};

export const updateRegulation = async (id: number, data: Partial<RegulationCreate> & { version: number }): Promise<Regulation> => {
    const { version, ...updateData } = data;
    const response = await api.patch(`/regulations/${id}?version=${version}`, updateData);
    return response.data;
};

export const deleteRegulation = async (id: number): Promise<void> => {
    await api.delete(`/regulations/${id}`);
};

export const lockRegulation = async (id: number): Promise<Regulation> => {
    const response = await api.post(`/regulations/${id}/lock`);
    return response.data;
};
