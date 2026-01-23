import axios from 'axios';
import Cookies from 'js-cookie';
import { getApiUrl } from '@/config/env';

/**
 * Centralized API Client
 * 
 * All API calls MUST use this instance to ensure:
 * - Validated HTTPS URLs in production
 * - Automatic authentication headers
 * - Centralized error handling
 * - Request/response interceptors
 */

// Get validated URL (will throw if invalid)
const API_URL = getApiUrl();

// Log in development for debugging (server-side only)
if (typeof window === 'undefined' && process.env.NODE_ENV === 'development') {
    console.log(`🔧 API Client initialized with base URL: ${API_URL}/api/v1`);
}

export const api = axios.create({
    baseURL: `${API_URL}/api/v1`,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000, // 30 second timeout
});

// Request Interceptor - Attach token & validate URL
api.interceptors.request.use(
    (config) => {
        // Attach authentication token
        const token = Cookies.get('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        // Security check: Block HTTP requests in production (only at request time, not module load)
        if (process.env.NODE_ENV === 'production') {
            const fullUrl = config.baseURL + (config.url || '');
            if (fullUrl.startsWith('http://')) {
                throw new Error(
                    `🚨 BLOCKED: Attempted HTTP request in production: ${fullUrl}`
                );
            }
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response Interceptor - Handle errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Handle 401 Unauthorized - redirect to login
        if (error.response?.status === 401) {
            // Clear token
            Cookies.remove('access_token');

            // Redirect to login (only in browser)
            if (typeof window !== 'undefined' && !window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }

        return Promise.reject(error);
    }
);

export default api;
