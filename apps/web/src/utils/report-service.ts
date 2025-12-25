import { api } from "@/utils/api";
import { useQuery } from "@tanstack/react-query";

export const reportService = {
    useAcademicSyllabus: () => {
        return useQuery({
            queryKey: ["reports", "academic", "syllabus"],
            queryFn: async () => {
                const response = await api.get("/reports/academic/syllabus-progress");
                return response.data;
            }
        });
    },

    useAcademicAttendance: () => {
        return useQuery({
            queryKey: ["reports", "academic", "attendance"],
            queryFn: async () => {
                const response = await api.get("/reports/academic/attendance-summary");
                return response.data;
            }
        });
    },

    useFinancialFeeCollection: () => {
        return useQuery({
            queryKey: ["reports", "financial", "fee-collection"],
            queryFn: async () => {
                const response = await api.get("/reports/financial/fee-collection");
                return response.data;
            }
        });
    },

    useInventoryStock: () => {
        return useQuery({
            queryKey: ["reports", "inventory", "stock"],
            queryFn: async () => {
                const response = await api.get("/reports/inventory/stock-status");
                return response.data;
            }
        });
    }
};
