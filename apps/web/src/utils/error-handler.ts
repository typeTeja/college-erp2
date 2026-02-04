/**
 * Error Handler Utilities
 * 
 * Safely extract human-readable error messages from API responses.
 * Especially handles FastAPI/Pydantic validation error objects.
 */

export interface PydanticError {
    type: string;
    loc: (string | number)[];
    msg: string;
    input: any;
    url?: string;
}

export function formatError(error: any): string {
    if (!error) return 'An unexpected error occurred';

    // 1. Handle string errors
    if (typeof error === 'string') return error;

    // 2. Handle Axios/Web response errors
    const responseData = error.response?.data;
    if (responseData) {
        // FASTAPI Detail (can be string or array of Pydantic objects)
        if (responseData.detail) {
            const detail = responseData.detail;
            
            if (typeof detail === 'string') return detail;
            
            if (Array.isArray(detail)) {
                // If it's a Pydantic validation error list
                return detail
                    .map((err: any) => {
                        if (typeof err === 'string') return err;
                        if (err.msg) {
                            // Format: "field: error message" or just "error message"
                            const field = err.loc && err.loc.length > 1 ? `${err.loc[err.loc.length - 1]}: ` : '';
                            return `${field}${err.msg}`;
                        }
                        return JSON.stringify(err);
                    })
                    .join(', ');
            }
            
            if (typeof detail === 'object') {
                return detail.msg || JSON.stringify(detail);
            }
        }

        // Generic message field
        if (responseData.message) return responseData.message;
        
        // Generic error field
        if (responseData.error) return typeof responseData.error === 'string' ? responseData.error : JSON.stringify(responseData.error);
    }

    // 3. Handle standard Error objects
    if (error instanceof Error) return error.message;

    // 4. Default fallback
    try {
        return JSON.stringify(error);
    } catch {
        return 'An unidentified error occurred';
    }
}
