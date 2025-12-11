import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import Cookies from 'js-cookie';
import { api } from '@/lib/api';
import { jwtDecode } from 'jwt-decode';

interface User {
    id: number;
    email: string;
    roles: string[];
}

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    login: (credentials: any) => Promise<void>;
    logout: () => void;
    checkAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            isAuthenticated: false,

            login: async (credentials) => {
                const { data } = await api.post('/auth/login', credentials);
                const { access_token, refresh_token, user } = data;

                Cookies.set('access_token', access_token);
                Cookies.set('refresh_token', refresh_token);

                set({ user, isAuthenticated: true });
            },

            logout: () => {
                Cookies.remove('access_token');
                Cookies.remove('refresh_token');
                set({ user: null, isAuthenticated: false });
                window.location.href = '/login';
            },

            checkAuth: () => {
                const token = Cookies.get('access_token');
                if (token) {
                    try {
                        const decoded: any = jwtDecode(token);
                        // Ideally we should validate expiry here too
                        if (decoded.exp * 1000 > Date.now()) {
                            // We can't fully reconstruct User from just token without an API call usually,
                            // but if we store user in persist, we are okay.
                            // If we want to be strict, we call /auth/me here.
                            set({ isAuthenticated: true });
                        } else {
                            set({ isAuthenticated: false, user: null });
                        }
                    } catch (e) {
                        set({ isAuthenticated: false, user: null });
                    }
                } else {
                    set({ isAuthenticated: false, user: null });
                }
            },
        }),
        {
            name: 'auth-storage', // name of the item in the storage (must be unique)
            partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }), // only persist user and status
        }
    )
);
