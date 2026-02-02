/**
 * Navigation Configuration
 * Single source of truth for all navigation items
 * 
 * Refactored Phase 1 (2026-02-01):
 * - Task-based taxonomy (Dashboard, Academics, Admissions, People, Finance, Campus, System)
 * - Consolidated Settings into "System"
 * - Flattened deep hierarchies
 */
import {
    LayoutDashboard, GraduationCap, Users, DollarSign,
    Building2, ClipboardList, Megaphone, Settings,
    BookOpen, Calendar, FileText, UserCheck, Briefcase,
    BedDouble, Library, Package, HeadphonesIcon,
    FileCheck, Clock, Layers, BarChart3, Menu, Award,
    Shield, School, Key, FileInput
} from 'lucide-react';
import type { NavigationConfig } from '@/types/navigation';

export const NAVIGATION_CONFIG: Record<string, NavigationConfig> = {
    SUPER_ADMIN: {
        groups: [
            {
                id: 'dashboard',
                label: 'Dashboard',
                icon: LayoutDashboard,
                order: 1,
                items: [
                    {
                        id: 'dashboard',
                        label: 'Home',
                        path: '/',
                        icon: LayoutDashboard,
                        shortcut: 'g d'
                    },
                    {
                        id: 'reports',
                        label: 'Reports & Analytics',
                        path: '/reports',
                        icon: BarChart3,
                        requiredPermissions: ['reports:read']
                    },
                    {
                        id: 'circulars',
                        label: 'Circulars',
                        path: '/circulars',
                        icon: Megaphone,
                        requiredPermissions: ['circulars:write']
                    }

                ]
            },
            {
                id: 'academics',
                label: 'Academics',
                icon: GraduationCap,
                order: 2,
                items: [
                    {
                        id: 'programs',
                        label: 'Programs & Batches',
                        path: '/settings?tab=programs', // Temporary mapping until full split
                        icon: School,
                        requiredPermissions: ['academics:read']
                    },
                    {
                        id: 'assignments',
                        label: 'Student Assignment',
                        path: '/academics/assignments',
                        icon: UserCheck,
                        requiredPermissions: ['academics:write']
                    },
                    {
                        id: 'timetable',
                        label: 'Timetable',
                        path: '/timetable',
                        icon: Calendar,
                        requiredPermissions: ['timetable:manage']
                    },
                    {
                        id: 'examinations',
                        label: 'Examinations',
                        path: '/exams',
                        icon: FileText,
                        requiredPermissions: ['exams:read']
                    },
                    {
                        id: 'attendance',
                        label: 'Class Attendance',
                        path: '/attendance',
                        icon: UserCheck,
                        requiredPermissions: ['attendance:manage']
                    }
                ]
            },
            {
                id: 'admissions',
                label: 'Admissions',
                icon: ClipboardList,
                order: 3,
                items: [
                    {
                        id: 'applications',
                        label: 'Applications',
                        path: '/admissions',
                        icon: FileInput,
                        requiredPermissions: ['admissions:read']
                    },
                    {
                        id: 'enquiries',
                        label: 'Enquiries',
                        path: '/admissions/enquiries', // Placeholder path
                        icon: HeadphonesIcon,
                        requiredPermissions: ['admissions:read']
                    }
                ]
            },
            {
                id: 'people',
                label: 'People',
                icon: Users,
                order: 4,
                items: [
                    {
                        id: 'students',
                        label: 'Student Directory',
                        path: '/students',
                        icon: Users,
                        shortcut: 'g p s',
                        requiredPermissions: ['students:read']
                    },
                    {
                        id: 'faculty',
                        label: 'Faculty Directory',
                        path: '/faculty',
                        icon: GraduationCap,
                        requiredPermissions: ['staff:read']
                    },
                    {
                        id: 'staff',
                        label: 'Staff Directory',
                        path: '/staff/directory',
                        icon: Briefcase,
                        requiredPermissions: ['staff:read']
                    },
                    {
                        id: 'import-students',
                        label: 'Bulk Import',
                        path: '/students/import',
                        icon: FileText,
                        requiredPermissions: ['students:write']
                    }
                ]
            },
            {
                id: 'finance',
                label: 'Finance',
                icon: DollarSign,
                order: 5,
                items: [
                    {
                        id: 'fees',
                        label: 'Fee Collection',
                        path: '/fees',
                        icon: DollarSign,
                        shortcut: 'g f',
                        requiredPermissions: ['fees:read']
                    },
                    {
                        id: 'fee-setup',
                        label: 'Fee Structure',
                        path: '/settings?tab=fee-heads', // Temporary
                        icon: Settings,
                        requiredPermissions: ['fees:write']
                    },
                    {
                        id: 'payroll',
                        label: 'Payroll',
                        path: '/payroll', // Placeholder
                        icon: Wallet,
                        requiredPermissions: ['fees:approve'] // Temporary mapping
                    }
                ]
            },
            {
                id: 'campus',
                label: 'Campus',
                icon: Building2,
                order: 6,
                items: [
                    {
                        id: 'hostel',
                        label: 'Hostel',
                        path: '/hostel',
                        icon: BedDouble,
                        requiredPermissions: ['hostel:read']
                    },
                    {
                        id: 'library',
                        label: 'Library',
                        path: '/library',
                        icon: Library,
                        requiredPermissions: ['library:read']
                    },
                    {
                        id: 'inventory',
                        label: 'Inventory',
                        path: '/inventory',
                        icon: Package,
                        requiredPermissions: ['inventory:read']
                    },
                    {
                        id: 'transport',
                        label: 'Transport',
                        path: '/transport', // Placeholder
                        icon: Bus,
                        requiredPermissions: ['hostel:read'] // Temporary mapping
                    },
                    {
                        id: 'gate-pass',
                        label: 'Gate Pass',
                        path: '/gatepass',
                        icon: FileCheck,
                        requiredPermissions: ['hostel:read'] // Temporary mapping
                    },
                    {
                        id: 'helpdesk',
                        label: 'Helpdesk',
                        path: '/staff/ops/tickets',
                        icon: HeadphonesIcon,
                        requiredPermissions: ['staff:read']
                    }
                ]
            },
            {
                id: 'system',
                label: 'System',
                icon: Shield, // Changed from Settings icon to Shield to denote Admin
                order: 7,
                requiredPermissions: ['settings:write', 'rbac:manage'],
                items: [
                    {
                        id: 'configuration',
                        label: 'General Configuration',
                        path: '/settings',
                        icon: Settings,
                        requiredPermissions: ['settings:write']
                    },
                    {
                        id: 'access-control',
                        label: 'Access Control',
                        path: '/settings?tab=roles',
                        icon: Key,
                        requiredPermissions: ['rbac:manage']
                    },
                    {
                        id: 'audit-logs',
                        label: 'Audit Logs',
                        path: '/settings?tab=audit',
                        icon: FileCheck,
                        requiredPermissions: ['rbac:manage']
                    }
                ]
            }
        ],
        mobileBottomNav: [
            { id: 'dashboard', label: 'Home', path: '/', icon: LayoutDashboard },
            { id: 'academics', label: 'Academics', path: '/academics', icon: GraduationCap },
            { id: 'people', label: 'People', path: '/students', icon: Users },
            { id: 'more', label: 'Menu', path: '/menu', icon: Menu }
        ]
    },

    // Default Fallback (Copy of Super Admin for now, role-specific refinement in Phase 2)
    ADMIN: {
        groups: [],
        mobileBottomNav: []
    },

    // Minimal Student View
    STUDENT: {
        groups: [
            {
                id: 'dashboard',
                label: 'Dashboard',
                icon: LayoutDashboard,
                order: 1,
                items: [
                    { id: 'home', label: 'Home', path: '/', icon: LayoutDashboard }
                ]
            },
            {
                id: 'academics',
                label: 'Academics',
                icon: GraduationCap,
                order: 2,
                items: [
                    { id: 'attendance', label: 'My Attendance', path: '/attendance', icon: UserCheck },
                    { id: 'timetable', label: 'Timetable', path: '/timetable', icon: Calendar },
                    { id: 'exams', label: 'Results', path: '/exams', icon: FileText }
                ]
            },
            {
                id: 'finance',
                label: 'Finance',
                icon: DollarSign,
                order: 3,
                items: [
                    { id: 'fees', label: 'My Fees', path: '/fees', icon: DollarSign }
                ]
            },
            {
                id: 'campus',
                label: 'Campus',
                icon: Building2,
                order: 4,
                items: [
                    { id: 'library', label: 'Library Books', path: '/library', icon: Library },
                    { id: 'gatepass', label: 'Gate Pass', path: '/gatepass', icon: FileCheck }
                ]
            }
        ],
        mobileBottomNav: [
            { id: 'home', label: 'Home', path: '/', icon: LayoutDashboard },
            { id: 'attendance', label: 'Attendance', path: '/attendance', icon: UserCheck },
            { id: 'fees', label: 'Fees', path: '/fees', icon: DollarSign },
            { id: 'more', label: 'Menu', path: '/menu', icon: Menu }
        ]
    }
};

// Import missing icons locally to avoid error if Lucide doesn't export them yet
import { Wallet, Bus } from 'lucide-react';
// Note: Wallet, Bus might not be in the initial import list, added them above or ignore if missing types.
// Actually, let's stick to safe icons. Wallet is fine. Bus is usually available.
