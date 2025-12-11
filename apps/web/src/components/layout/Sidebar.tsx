'use client';

import React from 'react';
import Link from 'next/link';
import {
    LayoutDashboard, Users, GraduationCap, Calendar, BookOpen,
    DollarSign, Building2, ClipboardList, FileText, BarChart3,
    Settings, LogOut, UserCheck, Home, Library, Shield, Wallet,
    BedDouble, Clock, FileCheck, TrendingUp
} from 'lucide-react';
import { useAuthStore } from '@/store/use-auth-store';

interface SidebarProps {
    isOpen: boolean;
    onToggle: () => void;
}

interface NavItem {
    icon: React.ReactNode;
    label: string;
    path: string;
    badge?: string;
}

const roleNavItems: Record<string, NavItem[]> = {
    SUPER_ADMIN: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <Users size={20} />, label: 'Students', path: '/students' },
        { icon: <GraduationCap size={20} />, label: 'Faculty', path: '/faculty' },
        { icon: <Calendar size={20} />, label: 'Attendance', path: '/attendance' },
        { icon: <DollarSign size={20} />, label: 'Fees Management', path: '/fees' },
        { icon: <FileText size={20} />, label: 'Examinations', path: '/exams' },
        { icon: <Building2 size={20} />, label: 'Hostel', path: '/hostel' },
        { icon: <BookOpen size={20} />, label: 'Library', path: '/library' },
        { icon: <Clock size={20} />, label: 'Timetable', path: '/timetable' },
        { icon: <FileCheck size={20} />, label: 'Gate Pass', path: '/gatepass' },
        { icon: <ClipboardList size={20} />, label: 'ODC', path: '/odc' },
        { icon: <BarChart3 size={20} />, label: 'Reports', path: '/reports' },
        { icon: <Settings size={20} />, label: 'Settings', path: '/settings' },
    ],
    FACULTY: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <Users size={20} />, label: 'My Classes', path: '/classes' },
        { icon: <UserCheck size={20} />, label: 'Attendance', path: '/attendance' },
        { icon: <FileText size={20} />, label: 'Exams & Grades', path: '/exams' },
        { icon: <Clock size={20} />, label: 'My Timetable', path: '/timetable' },
        { icon: <ClipboardList size={20} />, label: 'Assignments', path: '/assignments' },
        { icon: <FileCheck size={20} />, label: 'ODC Requests', path: '/odc' },
        { icon: <Settings size={20} />, label: 'Profile', path: '/profile' },
    ],
    STUDENT: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <Calendar size={20} />, label: 'My Attendance', path: '/attendance' },
        { icon: <DollarSign size={20} />, label: 'Fee Status', path: '/fees' },
        { icon: <FileText size={20} />, label: 'Exams & Results', path: '/exams' },
        { icon: <Clock size={20} />, label: 'Timetable', path: '/timetable' },
        { icon: <BookOpen size={20} />, label: 'Library', path: '/library' },
        { icon: <ClipboardList size={20} />, label: 'Assignments', path: '/assignments' },
        { icon: <FileCheck size={20} />, label: 'ODC / On Duty', path: '/odc/student' },
        { icon: <FileCheck size={20} />, label: 'Gate Pass', path: '/gatepass' },
        { icon: <Settings size={20} />, label: 'Profile', path: '/profile' },
    ],
    ADMIN: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <Users size={20} />, label: 'Students', path: '/students' },
        { icon: <GraduationCap size={20} />, label: 'Faculty', path: '/faculty' },
        { icon: <DollarSign size={20} />, label: 'Fees', path: '/fees' },
        { icon: <ClipboardList size={20} />, label: 'ODC Management', path: '/odc' },
        { icon: <BarChart3 size={20} />, label: 'Reports', path: '/reports' },
        { icon: <Settings size={20} />, label: 'Settings', path: '/settings' },
    ],
};

export function Sidebar({ isOpen, onToggle }: SidebarProps) {
    const { user, logout, hasHydrated } = useAuthStore();

    // Prevent hydration mismatch / flash of content
    // Render skeleton/loading state instead of null to maintain layout
    if (!hasHydrated) {
        return (
            <aside className="fixed left-0 top-0 h-screen w-64 bg-white border-r border-slate-200 z-40">
                <div className="flex flex-col h-full">
                    <div className="p-6 border-b border-slate-200">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-slate-100 rounded-lg animate-pulse" />
                            <div>
                                <div className="h-4 w-24 bg-slate-100 rounded animate-pulse mb-1" />
                                <div className="h-3 w-16 bg-slate-100 rounded animate-pulse" />
                            </div>
                        </div>
                    </div>
                    <nav className="flex-1 overflow-y-auto p-4">
                        <ul className="space-y-1">
                            {[1, 2, 3, 4, 5].map((i) => (
                                <li key={i}>
                                    <div className="w-full flex items-center gap-3 px-4 py-3 rounded-lg">
                                        <div className="w-5 h-5 bg-slate-100 rounded animate-pulse" />
                                        <div className="h-4 w-24 bg-slate-100 rounded animate-pulse" />
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </nav>
                </div>
            </aside>
        );
    }

    const userRole = user?.roles?.[0];
    const navItems = userRole && roleNavItems[userRole] ? roleNavItems[userRole] : [];

    if (!navItems.length) return null;

    return (
        <aside className="fixed left-0 top-0 h-screen w-64 bg-white border-r border-slate-200 z-40">
            <div className="flex flex-col h-full">
                {/* Logo */}
                <div className="p-6 border-b border-slate-200">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
                            <Shield className="text-white" size={24} />
                        </div>
                        <div>
                            <h1 className="text-slate-900 font-semibold">College ERP</h1>
                            <p className="text-xs text-slate-500">Management System</p>
                        </div>
                    </div>
                </div>

                {/* Navigation */}
                <nav className="flex-1 overflow-y-auto p-4">
                    <ul className="space-y-1">
                        {navItems.map((item, index) => (
                            <li key={index}>
                                <Link
                                    href={item.path}
                                    className="w-full flex items-center gap-3 px-4 py-3 text-slate-700 hover:bg-blue-50 hover:text-blue-700 rounded-lg transition-colors group"
                                >
                                    <span className="text-slate-500 group-hover:text-blue-600">
                                        {item.icon}
                                    </span>
                                    <span className="flex-1 text-left text-sm">{item.label}</span>
                                    {item.badge && (
                                        <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs">
                                            {item.badge}
                                        </span>
                                    )}
                                </Link>
                            </li>
                        ))}
                    </ul>
                </nav>

                {/* Footer */}
                <div className="p-4 border-t border-slate-200">
                    <button
                        onClick={logout}
                        className="w-full flex items-center gap-3 px-4 py-3 text-slate-700 hover:bg-red-50 hover:text-red-600 rounded-lg transition-colors"
                    >
                        <LogOut size={20} />
                        <span className="text-sm">Logout</span>
                    </button>
                </div>
            </div>
        </aside>
    );
}
