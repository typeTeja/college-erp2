import { api } from "@/utils/api";
import { useQuery } from "@tanstack/react-query";

export interface Program {
    id: number;
    code: string;
    name: string;
    duration_years: number;
}

export const programService = {
    usePrograms: () => {
        return useQuery({
            queryKey: ["programs"],
            queryFn: async () => {
                const response = await api.get<Program[]>("/programs/");
                return response.data;
            }
        });
    }
};
