'use client';
import { useAuthStore } from '@/store/use-auth-store';
import { useRouter } from 'next/navigation';

import Link from 'next/link';

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const logout = useAuthStore((state) => state.logout);
    const router = useRouter();

    return (
        <div className="min-h-screen bg-gray-100">
            {/* Top Sidebar / Nav placeholder */}
            <nav className="bg-white shadow">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="flex h-16 justify-between">
                        <div className="flex">
                            <div className="flex flex-shrink-0 items-center mr-8">
                                <span className="font-bold text-xl text-indigo-600">College ERP</span>
                            </div>
                            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                                <Link href="/" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-gray-300">
                                    Dashboard
                                </Link>
                                <Link href="/odc" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-gray-300">
                                    ODC
                                </Link>
                            </div>
                        </div>
                        <div className="flex items-center">
                            <button
                                onClick={() => logout()}
                                className="ml-3 inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            <main>
                <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
                    {children}
                </div>
            </main>
        </div>
    );
}
