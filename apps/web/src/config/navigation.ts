/**
 * Navigation Configuration
 * Single source of truth for all navigation items
 */
import {
    LayoutDashboard, GraduationCap, Users, DollarSign,
    Building2, ClipboardList, Megaphone, Settings,
    BookOpen, Calendar, FileText, UserCheck, Briefcase,
    BedDouble, Library, Package, HeadphonesIcon,
    FileCheck, Clock, Layers, BarChart3, Menu, Award
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
                defaultExpanded: false,
                items: [
                    {
                        id: 'dashboard',
                        label: 'Dashboard',
                        path: '/',
                        icon: LayoutDashboard,
                        shortcut: 'g d'
                    }
                ]
            },
            {
                id: 'academics',
                label: 'Academics',
                icon: GraduationCap,
                order: 2,
                defaultExpanded: false,
                items: [
                    {
                        id: 'bulk-setup',
                        label: 'Bulk Setup',
                        path: '/academics/bulk-setup',
                        icon: Layers,
                        badge: 'New',
                        shortcut: 'g a b'
                    },
                    {
                        id: 'student-assignment',
                        label: 'Student Assignment',
                        path: '/academics/assignments',
                        icon: UserCheck,
                        badge: 'New',
                        shortcut: 'g a s'
                    },
                    {
                        id: 'regulations',
                        label: 'Regulations',
                        path: '/settings?tab=regulations',
                        icon: BookOpen
                    },
                    {
                        id: 'timetable',
                        label: 'Timetable',
                        path: '/timetable',
                        icon: Calendar
                    },
                    {
                        id: 'examinations',
                        label: 'Examinations',
                        path: '/exams',
                        icon: FileText
                    }
                ]
            },
            {
                id: 'people',
                label: 'People',
                icon: Users,
                order: 3,
                items: [
                    {
                        id: 'students',
                        label: 'Students',
                        path: '/students',
                        icon: Users,
                        shortcut: 'g p s'
                    },
                    {
                        id: 'import-students',
                        label: 'Import Students',
                        path: '/students/import',
                        icon: FileText
                    },
                    {
                        id: 'admissions',
                        label: 'Admissions',
                        path: '/admissions',
                        icon: ClipboardList
                    },
                    {
                        id: 'faculty',
                        label: 'Faculty',
                        path: '/faculty',
                        icon: GraduationCap
                    },
                    {
                        id: 'staff',
                        label: 'Staff Directory',
                        path: '/staff/directory',
                        icon: Briefcase
                    }
                ]
            },
            {
                id: 'finance',
                label: 'Finance',
                icon: DollarSign,
                order: 4,
                items: [
                    {
                        id: 'fees',
                        label: 'Fees Management',
                        path: '/fees',
                        icon: DollarSign,
                        shortcut: 'g f'
                    },
                    {
                        id: 'fee-heads',
                        label: 'Fee Heads',
                        path: '/settings?tab=fee-heads',
                        icon: FileText
                    },
                    {
                        id: 'scholarship-slabs',
                        label: 'Scholarship Slabs',
                        path: '/settings?tab=scholarship-slabs',
                        icon: Award
                    },
                    {
                        id: 'reports',
                        label: 'Financial Reports',
                        path: '/reports',
                        icon: BarChart3
                    }
                ]
            },
            {
                id: 'campus',
                label: 'Campus',
                icon: Building2,
                order: 5,
                items: [
                    {
                        id: 'hostel',
                        label: 'Hostel',
                        path: '/hostel',
                        icon: BedDouble
                    },
                    {
                        id: 'library',
                        label: 'Library',
                        path: '/library',
                        icon: Library
                    },
                    {
                        id: 'inventory',
                        label: 'Inventory',
                        path: '/inventory',
                        icon: Package
                    },
                    {
                        id: 'helpdesk',
                        label: 'Helpdesk',
                        path: '/staff/ops/tickets',
                        icon: HeadphonesIcon
                    }
                ]
            },
            {
                id: 'operations',
                label: 'Operations',
                icon: ClipboardList,
                order: 6,
                items: [
                    {
                        id: 'attendance',
                        label: 'Attendance',
                        path: '/attendance',
                        icon: UserCheck
                    },
                    {
                        id: 'odc',
                        label: 'ODC',
                        path: '/odc',
                        icon: ClipboardList
                    },
                    {
                        id: 'gate-pass',
                        label: 'Gate Pass',
                        path: '/gatepass',
                        icon: FileCheck
                    },
                    {
                        id: 'shift-roster',
                        label: 'Shift Roster',
                        path: '/staff/ops/shifts',
                        icon: Clock
                    }
                ]
            },
            {
                id: 'communication',
                label: 'Communication',
                icon: Megaphone,
                order: 7,
                items: [
                    {
                        id: 'circulars',
                        label: 'Circulars',
                        path: '/circulars',
                        icon: Megaphone
                    }
                ]
            },
            {
                id: 'settings',
                label: 'Settings',
                icon: Settings,
                order: 8,
                defaultExpanded: false,
                items: [
                    {
                        id: 'settings',
                        label: 'Settings',
                        path: '/settings',
                        icon: Settings,
                        shortcut: 'g s'
                    }
                ]
            }
        ],
        mobileBottomNav: [
            { id: 'dashboard', label: 'Home', path: '/', icon: LayoutDashboard },
            { id: 'academics-mobile', label: 'Academics', path: '/academics', icon: GraduationCap },
            { id: 'people-mobile', label: 'People', path: '/students', icon: Users },
            { id: 'finance-mobile', label: 'Finance', path: '/fees', icon: DollarSign },
            { id: 'more', label: 'More', path: '/menu', icon: Menu }
        ]
    },

    // Add other roles as needed
    ADMIN: {
        groups: [], // Copy from SUPER_ADMIN or customize
        mobileBottomNav: []
    },

    STUDENT: {
        groups: [
            {
                id: 'dashboard',
                label: 'Dashboard',
                icon: LayoutDashboard,
                order: 1,
                defaultExpanded: false,
                items: [
                    {
                        id: 'dashboard',
                        label: 'Dashboard',
                        path: '/',
                        icon: LayoutDashboard,
                        shortcut: 'g d'
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
                        id: 'attendance',
                        label: 'My Attendance',
                        path: '/attendance',
                        icon: Calendar
                    },
                    {
                        id: 'timetable',
                        label: 'My Timetable',
                        path: '/timetable',
                        icon: Clock
                    },
                    {
                        id: 'exams',
                        label: 'Exams & Results',
                        path: '/exams',
                        icon: FileText
                    },
                    {
                        id: 'assignments',
                        label: 'Assignments',
                        path: '/assignments',
                        icon: ClipboardList
                    }
                ]
            },
            {
                id: 'finance',
                label: 'Finance',
                icon: DollarSign,
                order: 3,
                items: [
                    {
                        id: 'fees',
                        label: 'Fee Status',
                        path: '/fees',
                        icon: DollarSign
                    }
                ]
            },
            {
                id: 'campus',
                label: 'Campus',
                icon: Building2,
                order: 4,
                items: [
                    {
                        id: 'library',
                        label: 'Library Books',
                        path: '/library',
                        icon: Library
                    },
                    {
                        id: 'gate-pass',
                        label: 'Gate Pass',
                        path: '/gatepass',
                        icon: FileCheck
                    },
                    {
                        id: 'odc',
                        label: 'ODC Request',
                        path: '/odc/student',
                        icon: ClipboardList
                    }
                ]
            },
            {
                id: 'communication',
                label: 'Communication',
                icon: Megaphone,
                order: 5,
                items: [
                    {
                        id: 'circulars',
                        label: 'Circulars',
                        path: '/circulars',
                        icon: Megaphone
                    }
                ]
            },
            {
                id: 'settings',
                label: 'Settings',
                icon: Settings,
                order: 6,
                items: [
                    {
                        id: 'settings',
                        label: 'Profile Settings',
                        path: '/settings',
                        icon: Settings
                    }
                ]
            }
        ],
        mobileBottomNav: [
            { id: 'dashboard', label: 'Home', path: '/', icon: LayoutDashboard },
            { id: 'attendance', label: 'Attendance', path: '/attendance', icon: Calendar },
            { id: 'fees', label: 'Fees', path: '/fees', icon: DollarSign },
            { id: 'more', label: 'More', path: '/menu', icon: Menu }
        ]
    }
};
