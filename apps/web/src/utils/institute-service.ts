import { api } from '@/utils/api';
import { InstituteInfo } from '@/types/institute';

export const getInstituteInfo = async (): Promise<InstituteInfo> => {
    const response = await api.get<InstituteInfo>('/institute/');
    return response.data;
};

export const updateInstituteInfo = async (data: InstituteInfo): Promise<InstituteInfo> => {
    const response = await api.put<InstituteInfo>('/institute/', data);
    return response.data;
};
