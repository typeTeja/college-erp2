'use client';

import React from 'react';
import Link from 'next/link';
import {
    LayoutDashboard, Users, GraduationCap, Calendar, BookOpen,
    DollarSign, Building2, ClipboardList, FileText, BarChart3,
    Settings, LogOut, UserCheck, Home, Library, Shield, Wallet,
    BedDouble, Clock, FileCheck, TrendingUp, Briefcase, Wrench,
    Megaphone
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
        { icon: <ClipboardList size={20} />, label: 'Admissions', path: '/admissions' },
        { icon: <Users size={20} />, label: 'Students', path: '/students' },
        { icon: <FileText size={20} />, label: 'Import Students', path: '/students/import', badge: 'New' },
        { icon: <GraduationCap size={20} />, label: 'Faculty', path: '/faculty' },
        { icon: <ClipboardList size={20} />, label: 'Academics', path: '/academics' },
        { icon: <Calendar size={20} />, label: 'Attendance', path: '/attendance' },
        { icon: <DollarSign size={20} />, label: 'Fees Management', path: '/fees' },
        { icon: <FileText size={20} />, label: 'Examinations', path: '/exams' },
        { icon: <Building2 size={20} />, label: 'Hostel', path: '/hostel' },
        { icon: <BookOpen size={20} />, label: 'Library', path: '/library' },
        { icon: <Clock size={20} />, label: 'Timetable', path: '/timetable' },
        { icon: <FileCheck size={20} />, label: 'Gate Pass', path: '/gatepass' },
        { icon: <ClipboardList size={20} />, label: 'ODC', path: '/odc' },
        { icon: <Briefcase size={20} />, label: 'Staff Directory', path: '/staff/directory' },
        { icon: <Clock size={20} />, label: 'Shift Roster', path: '/staff/ops/shifts' },
        { icon: <Wrench size={20} />, label: 'Inventory', path: '/inventory' },
        { icon: <Wrench size={20} />, label: 'Helpdesk', path: '/staff/ops/tickets' },
        { icon: <Megaphone size={20} />, label: 'Circulars', path: '/circulars' },
        { icon: <BarChart3 size={20} />, label: 'Reports', path: '/reports' },
        { icon: <Settings size={20} />, label: 'Settings', path: '/settings' },
    ],
    FACULTY: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <ClipboardList size={20} />, label: 'Academics', path: '/academics' },
        { icon: <Users size={20} />, label: 'My Classes', path: '/classes' },
        { icon: <UserCheck size={20} />, label: 'Attendance', path: '/attendance' },
        { icon: <FileText size={20} />, label: 'Exams & Grades', path: '/exams' },
        { icon: <Clock size={20} />, label: 'My Timetable', path: '/timetable' },
        { icon: <ClipboardList size={20} />, label: 'Assignments', path: '/assignments' },
        { icon: <FileCheck size={20} />, label: 'ODC Requests', path: '/odc' },
        { icon: <Megaphone size={20} />, label: 'Circulars', path: '/circulars' },
        { icon: <Settings size={20} />, label: 'Settings', path: '/settings' },
    ],
    STUDENT: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <Calendar size={20} />, label: 'My Attendance', path: '/attendance' },
        { icon: <DollarSign size={20} />, label: 'Fee Status', path: '/fees' },
        { icon: <FileText size={20} />, label: 'Exams & Results', path: '/exams' },
        { icon: <Clock size={20} />, label: 'Timetable', path: '/timetable' },
        { icon: <BookOpen size={20} />, label: 'Library', path: '/library' },
        { icon: <ClipboardList size={20} />, label: 'Assignments', path: '/assignments' },
        { icon: <FileCheck size={20} />, label: 'Outdoor Catering (ODC)', path: '/odc/student' },
        { icon: <FileCheck size={20} />, label: 'Gate Pass', path: '/gatepass' },
        { icon: <Megaphone size={20} />, label: 'Circulars', path: '/circulars' },
        { icon: <Settings size={20} />, label: 'Settings', path: '/settings' },
    ],
    ADMIN: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <ClipboardList size={20} />, label: 'Admissions', path: '/admissions' },
        { icon: <Users size={20} />, label: 'Students', path: '/students' },
        { icon: <FileText size={20} />, label: 'Import Students', path: '/students/import' },
        { icon: <GraduationCap size={20} />, label: 'Faculty', path: '/faculty' },
        { icon: <ClipboardList size={20} />, label: 'Academics', path: '/academics' },
        { icon: <Calendar size={20} />, label: 'Attendance', path: '/attendance' },
        { icon: <DollarSign size={20} />, label: 'Fees', path: '/fees' },
        { icon: <FileText size={20} />, label: 'Examinations', path: '/exams' },
        { icon: <ClipboardList size={20} />, label: 'ODC Management', path: '/odc' },
        { icon: <Briefcase size={20} />, label: 'Staff Directory', path: '/staff/directory' },
        { icon: <Clock size={20} />, label: 'Shift Roster', path: '/staff/ops/shifts' },
        { icon: <Wrench size={20} />, label: 'Inventory', path: '/inventory' },
        { icon: <Wrench size={20} />, label: 'Helpdesk', path: '/staff/ops/tickets' },
        { icon: <Megaphone size={20} />, label: 'Circulars', path: '/circulars' },
        { icon: <BarChart3 size={20} />, label: 'Reports', path: '/reports' },
        { icon: <Settings size={20} />, label: 'Settings', path: '/settings' },
    ],
    PRINCIPAL: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <Users size={20} />, label: 'Students', path: '/students' },
        { icon: <GraduationCap size={20} />, label: 'Faculty', path: '/faculty' },
        { icon: <DollarSign size={20} />, label: 'Fees', path: '/fees' },
        { icon: <Building2 size={20} />, label: 'Departments', path: '/departments' },
        { icon: <BarChart3 size={20} />, label: 'Reports', path: '/reports' },
        { icon: <Settings size={20} />, label: 'Settings', path: '/settings' },
    ],
    ADMISSION_OFFICER: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <ClipboardList size={20} />, label: 'Admissions', path: '/admissions' },
        { icon: <Users size={20} />, label: 'Students', path: '/students' },
    ],
    ACCOUNTS: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <DollarSign size={20} />, label: 'Fees Management', path: '/fees' },
        { icon: <Wallet size={20} />, label: 'Payroll', path: '/payroll' },
    ],
    LIBRARIAN: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <BookOpen size={20} />, label: 'Books', path: '/library' },
        { icon: <FileText size={20} />, label: 'Issued Books', path: '/library/issued' },
    ],
    WARDEN: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <Building2 size={20} />, label: 'Hostel Rooms', path: '/hostel' },
        { icon: <Users size={20} />, label: 'Inmates', path: '/hostel/students' },
    ],
    ODC_COORDINATOR: [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <ClipboardList size={20} />, label: 'ODC Requests', path: '/odc' },
        { icon: <Building2 size={20} />, label: 'Hotels', path: '/odc/hotels' },
    ],
};

export function Sidebar({ isOpen, onToggle }: SidebarProps) {
    const { user, logout, hasHydrated } = useAuthStore();

    // Prevent hydration mismatch / flash of content
    if (!hasHydrated) {
        return (
            <aside className={`fixed left-0 top-0 h-screen bg-white border-r border-slate-200 z-40 transition-all duration-300 ${isOpen ? 'w-64' : 'w-20'}`}>
                <div className="flex flex-col h-full">
                    <div className="p-6 border-b border-slate-200">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-slate-100 rounded-lg animate-pulse shrink-0" />
                            {isOpen && (
                                <div>
                                    <div className="h-4 w-24 bg-slate-100 rounded animate-pulse mb-1" />
                                    <div className="h-3 w-16 bg-slate-100 rounded animate-pulse" />
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </aside>
        );
    }

    const userRole = user?.roles?.[0]?.toUpperCase();
    const navItems = userRole && roleNavItems[userRole] ? roleNavItems[userRole] : [];

    if (!navItems.length) return null;

    return (
        <aside className={`fixed left-0 top-0 h-screen bg-white border-r border-slate-200 z-40 transition-all duration-300 ${isOpen ? 'w-64' : 'w-20'}`}>
            <div className="flex flex-col h-full">
                {/* Logo */}
                <div className="p-6 border-b border-slate-200">
                    <div className="flex items-center gap-3 overflow-hidden">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center shrink-0">
                            <Shield className="text-white" size={24} />
                        </div>
                        <div className={`transition-opacity duration-300 ${isOpen ? 'opacity-100' : 'opacity-0 w-0'}`}>
                            <h1 className="text-slate-900 font-semibold whitespace-nowrap">College ERP</h1>
                            <p className="text-xs text-slate-500 whitespace-nowrap">Management System</p>
                        </div>
                    </div>
                </div>

                {/* Navigation */}
                <nav className="flex-1 overflow-y-auto p-4 scrollbar-hide">
                    <ul className="space-y-1">
                        {navItems.map((item, index) => (
                            <li key={index}>
                                <Link
                                    href={item.path}
                                    className={`flex items-center gap-3 px-4 py-3 text-slate-700 hover:bg-blue-50 hover:text-blue-700 rounded-lg transition-colors group ${!isOpen ? 'justify-center' : ''}`}
                                    title={!isOpen ? item.label : undefined}
                                >
                                    <span className="text-slate-500 group-hover:text-blue-600 shrink-0">
                                        {item.icon}
                                    </span>
                                    {isOpen && (
                                        <>
                                            <span className="flex-1 text-left text-sm whitespace-nowrap overflow-hidden text-ellipsis">{item.label}</span>
                                            {item.badge && (
                                                <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs whitespace-nowrap">
                                                    {item.badge}
                                                </span>
                                            )}
                                        </>
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
                        className={`w-full flex items-center gap-3 px-4 py-3 text-slate-700 hover:bg-red-50 hover:text-red-600 rounded-lg transition-colors ${!isOpen ? 'justify-center' : ''}`}
                        title={!isOpen ? "Logout" : undefined}
                    >
                        <LogOut size={20} className="shrink-0" />
                        {isOpen && <span className="text-sm whitespace-nowrap">Logout</span>}
                    </button>
                </div>
            </div>
        </aside>
    );
}
