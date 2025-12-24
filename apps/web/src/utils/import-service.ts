import { api } from './api';

export enum ImportRowStatus {
    VALID = "VALID",
    INVALID = "INVALID",
    WARNING = "WARNING",
    DUPLICATE = "DUPLICATE"
}

export interface ImportErrorDetail {
    field: string;
    message: string;
}

export interface ImportPreviewRow {
    row_number: number;
    data: any;
    status: ImportRowStatus;
    errors: ImportErrorDetail[];
}

export interface ImportPreviewResponse {
    total_rows: number;
    valid_count: number;
    invalid_count: number;
    duplicate_count: number;
    rows: ImportPreviewRow[];
}

export interface ImportExecuteResponse {
    message: string;
    log_id: number;
    status: string;
}

export const importService = {
    async downloadTemplate(): Promise<void> {
        try {
            const response = await api.get('/import/template', {
                responseType: 'blob'
            });

            // Create blob link to download
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'student_import_template.csv');
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Failed to download template', error);
            throw error;
        }
    },

    async uploadPreview(file: File): Promise<ImportPreviewResponse> {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post('/import/preview', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    async executeImport(previewData: ImportPreviewResponse, fileName: string): Promise<ImportExecuteResponse> {
        const response = await api.post('/import/execute', previewData, {
            params: { file_name: fileName }
        });
        return response.data;
    }
};
