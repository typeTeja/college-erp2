'use client';

import React from 'react';
import { Menu, Bell, Search, User } from 'lucide-react';
import { useAuthStore } from '@/store/use-auth-store';
import Link from 'next/link';
import { communicationService } from '@/utils/communication-service';

interface TopNavProps {
    onMenuToggle: () => void;
}

const roleLabels: Record<string, string> = {
    SUPER_ADMIN: 'Super Admin',
    ADMIN: 'Admin',
    FACULTY: 'Faculty',
    STUDENT: 'Student',
    PARENT: 'Parent',
};

export function TopNav({ onMenuToggle }: TopNavProps) {
    const { user } = useAuthStore();
    const userRole = user?.roles?.[0];
    const roleLabel = userRole && roleLabels[userRole] ? roleLabels[userRole] : 'User';

    const { data: notifications } = communicationService.useNotifications({ unread_only: true });
    const unreadCount = notifications?.length || 0;

    return (
        <header className="sticky top-0 z-30 bg-white border-b border-slate-200">
            <div className="flex items-center justify-between px-6 py-4">
                {/* Left section */}
                <div className="flex items-center gap-4">
                    <button
                        onClick={onMenuToggle}
                        className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                    >
                        <Menu size={20} className="text-slate-700" />
                    </button>

                    {/* Search */}
                    <div className="relative hidden md:block">
                        <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                        <input
                            type="text"
                            placeholder="Search students, faculty, courses..."
                            className="w-96 pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>
                </div>

                {/* Right section */}
                <div className="flex items-center gap-4">
                    {/* Notifications */}
                    <Link href="/notifications">
                        <button className="relative p-2 hover:bg-slate-100 rounded-lg transition-colors">
                            <Bell size={20} className="text-slate-700" />
                            {unreadCount > 0 && (
                                <span className="absolute top-1.5 right-1.5 w-4 h-4 bg-red-500 text-white text-[10px] flex items-center justify-center rounded-full font-bold">
                                    {unreadCount > 9 ? '9+' : unreadCount}
                                </span>
                            )}
                        </button>
                    </Link>

                    {/* User profile */}
                    <div className="flex items-center gap-3 pl-4 border-l border-slate-200">
                        <div className="text-right hidden sm:block">
                            <p className="text-sm text-slate-900 font-medium">{user?.email || 'User'}</p>
                            <p className="text-xs text-slate-500">{roleLabel}</p>
                        </div>
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
                            <User size={20} className="text-white" />
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
}
