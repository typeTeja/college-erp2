import { api } from "@/utils/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
    Application, QuickApplyData, FullApplicationData, ApplicationStatus,
    ApplicationDocument, DocumentType, DocumentVerify,
    ActivityLog, OfflinePaymentVerify
} from "@/types/admissions";

export const admissionsService = {
    // Queries
    useApplications: (status?: ApplicationStatus) => {
        return useQuery({
            queryKey: ["applications", status],
            queryFn: async () => {
                const response = await api.get<Application[]>("/admissions/admin/applications", {
                    params: { status }
                });
                return response.data;
            }
        });
    },

    useApplication: (id: number) => {
        return useQuery({
            queryKey: ["application", id],
            queryFn: async () => {
                const response = await api.get<Application>(`/admissions/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    useDocuments: (applicationId: number) => {
        return useQuery({
            queryKey: ["documents", applicationId],
            queryFn: async () => {
                const response = await api.get<ApplicationDocument[]>(`/admissions/${applicationId}/documents`);
                return response.data;
            },
            enabled: !!applicationId
        });
    },

    useTimeline: (applicationId: number) => {
        return useQuery({
            queryKey: ["timeline", applicationId],
            queryFn: async () => {
                const response = await api.get<ActivityLog[]>(`/admissions/${applicationId}/timeline`);
                return response.data;
            },
            enabled: !!applicationId
        });
    },

    // Mutations
    useQuickApply: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: QuickApplyData) => {
                const response = await api.post<Application>("/admissions/quick-apply", data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["applications"] });
            }
        });
    },

    useCreateOfflineApplication: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: any) => {
                if (data.is_full_entry) {
                    const response = await api.post<Application>("/admissions/offline/full", data);
                    return response.data;
                } else {
                    const response = await api.post<Application>("/admissions/quick-apply", data);
                    return response.data;
                }
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["applications"] });
            }
        });
    },

    useUpdateApplication: (id: number) => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: FullApplicationData) => {
                const response = await api.put<Application>(`/admissions/${id}`, data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["application", id] });
                queryClient.invalidateQueries({ queryKey: ["applications"] });
            }
        });
    },

    useUploadDocument: (applicationId: number) => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ documentType, file }: { documentType: DocumentType; file: File }) => {
                const formData = new FormData();
                formData.append("file", file);

                const response = await api.post<ApplicationDocument>(
                    `/admissions/${applicationId}/documents/upload?document_type=${documentType}`,
                    formData,
                    {
                        headers: {
                            "Content-Type": "multipart/form-data"
                        }
                    }
                );
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["documents", applicationId] });
                queryClient.invalidateQueries({ queryKey: ["timeline", applicationId] });
            }
        });
    },

    useVerifyDocument: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ docId, data }: { docId: number; data: DocumentVerify }) => {
                const response = await api.put<ApplicationDocument>(`/admissions/documents/${docId}/verify`, data);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["documents", data.application_id] });
                queryClient.invalidateQueries({ queryKey: ["timeline", data.application_id] });
            }
        });
    },

    useVerifyOfflinePayment: (applicationId: number) => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: OfflinePaymentVerify) => {
                const response = await api.post<Application>(
                    `/admissions/${applicationId}/payment/offline-verify`,
                    data
                );
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["application", applicationId] });
                queryClient.invalidateQueries({ queryKey: ["applications"] });
                queryClient.invalidateQueries({ queryKey: ["timeline", applicationId] });
            }
        });
    },

    useConfirmAdmission: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                const response = await api.post<Application>(`/admissions/${id}/confirm`);
                return response.data;
            },
            onSuccess: (data) => {
                queryClient.invalidateQueries({ queryKey: ["application", data.id] });
                queryClient.invalidateQueries({ queryKey: ["applications"] });
                queryClient.invalidateQueries({ queryKey: ["students"] });
                queryClient.invalidateQueries({ queryKey: ["timeline", data.id] });
            }
        });
    },

    useResendCredentials: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                const response = await api.post<{ message: string }>(`/admissions/v2/applications/${id}/resend-credentials`);
                return response.data;
            },
            onSuccess: (data, id) => {
                // Nothing to invalidate really, maybe just toast
            }
        });
    }
};
