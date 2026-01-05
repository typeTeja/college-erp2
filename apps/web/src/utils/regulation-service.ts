import { api } from './api';
import { Regulation } from '@/types/regulation';

export const getRegulations = async (programId?: number, isLocked?: boolean): Promise<Regulation[]> => {
    const params: Record<string, any> = {};
    if (programId) params.program_id = programId;
    if (isLocked !== undefined) params.is_locked = isLocked;

    const response = await api.get('/regulations/', { params });
    return response.data;
};
