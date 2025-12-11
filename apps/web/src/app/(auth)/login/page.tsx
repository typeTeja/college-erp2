'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/use-auth-store';
import Link from 'next/link';
import { Loader2 } from 'lucide-react';

const loginSchema = z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export default function LoginPage() {
    const router = useRouter();
    const login = useAuthStore((state) => state.login);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LoginFormValues>({
        resolver: zodResolver(loginSchema),
    });

    const onSubmit = async (data: LoginFormValues) => {
        setIsLoading(true);
        setError(null);
        try {
            await login(data);
            router.push('/'); // Redirect to dashboard
        } catch (err: any) {
            setError(err.response?.data?.message || 'Login failed. Please checks your credentials.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="bg-white p-8 shadow-xl ring-1 ring-gray-900/5 sm:mx-auto sm:w-full sm:max-w-md sm:rounded-lg">
            <div className="mb-6 text-center">
                <h2 className="text-3xl font-bold tracking-tight text-gray-900">College ERP</h2>
                <p className="mt-2 text-sm text-gray-600">
                    Sign in to your account
                </p>
            </div>

            <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
                <div>
                    <label
                        htmlFor="email"
                        className="block text-sm font-medium leading-6 text-gray-900"
                    >
                        Email address
                    </label>
                    <div className="mt-2">
                        <input
                            id="email"
                            type="email"
                            autoComplete="email"
                            className={`block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pl-3 ${errors.email ? 'ring-red-500' : ''
                                }`}
                            {...register('email')}
                        />
                        {errors.email && (
                            <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
                        )}
                    </div>
                </div>

                <div>
                    <label
                        htmlFor="password"
                        className="block text-sm font-medium leading-6 text-gray-900"
                    >
                        Password
                    </label>
                    <div className="mt-2">
                        <input
                            id="password"
                            type="password"
                            autoComplete="current-password"
                            className={`block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pl-3 ${errors.password ? 'ring-red-500' : ''
                                }`}
                            {...register('password')}
                        />
                        {errors.password && (
                            <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
                        )}
                    </div>
                </div>

                {error && (
                    <div className="rounded-md bg-red-50 p-4">
                        <div className="flex">
                            <div className="ml-3">
                                <h3 className="text-sm font-medium text-red-800">Login Error</h3>
                                <div className="mt-2 text-sm text-red-700">
                                    <p>{error}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                <div>
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50"
                    >
                        {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                        Sign in
                    </button>
                </div>
            </form>

            <p className="mt-10 text-center text-sm text-gray-500">
                Forgot your password?{' '}
                <Link href="/forgot-password" className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">
                    Reset it here
                </Link>
            </p>
        </div>
    );
}
