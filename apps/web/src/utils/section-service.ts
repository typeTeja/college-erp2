import { api } from './api';
import { Section, SectionUpdate } from '@/types/section';

export const sectionService = {
    /**
     * Update section details (inline editing)
     */
    updateSection: async (id: number, data: SectionUpdate): Promise<Section> => {
        const response = await api.patch<Section>(`/sections/${id}`, data);
        return response.data;
    },
};
