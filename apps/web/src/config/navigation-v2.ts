/**
 * Navigation Configuration V2
 * 
 * 5-Tier Hierarchy for 20-Year Architecture:
 * Tier 1: Daily Operations (Dashboard, Admissions, Students, Academics, Finance)
 * Tier 2: Core Domains (Faculty, Attendance, Exams, Library)
 * Tier 3: Configuration [Config Badge] (Academic, Finance, Admission configs)
 * Tier 4: Institutional Setup [Setup Badge] (Institute, Departments, Programs)
 * Tier 5: System Administration [Admin Badge] (Users, Roles, Integrations)
 * 
 * Key Principles:
 * - Max 2 levels depth (group → item, no sub-items)
 * - Badge system for visual hierarchy
 * - Role-based visibility
 * - Domain boundaries enforced
 * 
 * Last Updated: 2026-02-04
 */

import {
    LayoutDashboard, GraduationCap, Users, DollarSign,
    Building2, ClipboardList, Megaphone, Settings,
    BookOpen, Calendar, FileText, UserCheck, Briefcase,
    BedDouble, Library, Package, HeadphonesIcon,
    FileCheck, Clock, Layers, BarChart3, Menu, Award,
    Shield, School, Key, FileInput, Cog, Database,
    UserCog, Lock, Activity, Wrench, Building
} from 'lucide-react';
import type { NavigationConfig } from '@/types/navigation';

/**
 * Badge types for visual hierarchy
 */
export type NavigationBadge = 'config' | 'setup' | 'admin';

/**
 * Navigation tier (1-5)
 */
export type NavigationTier = 1 | 2 | 3 | 4 | 5;

/**
 * Extended navigation item with V2 features
 */
export interface NavigationItemV2 {
    id: string;
    label: string;
    path: string;
    icon?: any;
    badge?: NavigationBadge;
    tier?: NavigationTier;
    requiredPermissions?: string[];
    requiredRoles?: string[];
    shortcut?: string;
    description?: string;
}

/**
 * Extended navigation group with V2 features
 */
export interface NavigationGroupV2 {
    id: string;
    label: string;
    icon?: any;
    badge?: NavigationBadge;
    tier: NavigationTier;
    order: number;
    items: NavigationItemV2[];
    requiredPermissions?: string[];
    requiredRoles?: string[];
}

const COMMON_MOBILE_NAV = [
    { id: 'dashboard', label: 'Home', path: '/', icon: LayoutDashboard },
    { id: 'academics', label: 'Academics', path: '/academics', icon: GraduationCap },
    { id: 'people', label: 'People', path: '/students', icon: Users },
    { id: 'more', label: 'Menu', path: '/menu', icon: Menu }
];

/**
 * Navigation V2 Configuration
 */
export const NAVIGATION_CONFIG_V2: Record<string, NavigationConfig> = {
    SUPER_ADMIN: {
        groups: [
            // TIER 1: DAILY OPERATIONS
            {
                id: 'dashboard',
                label: 'Dashboard',
                icon: LayoutDashboard,
                tier: 1,
                order: 1,
                items: [
                    {
                        id: 'home',
                        label: 'Home',
                        path: '/',
                        icon: LayoutDashboard,
                        shortcut: 'g d'
                    },
                    {
                        id: 'reports',
                        label: 'Reports & Analytics',
                        path: '/reports',
                        icon: BarChart3
                    },
                    {
                        id: 'circulars',
                        label: 'Circulars',
                        path: '/circulars',
                        icon: Megaphone
                    }
                ]
            },
            {
                id: 'admissions',
                label: 'Admissions',
                icon: ClipboardList,
                tier: 1,
                order: 2,
                items: [
                    {
                        id: 'applications',
                        label: 'Applications',
                        path: '/admissions',
                        icon: ClipboardList
                    },
                    {
                        id: 'verification',
                        label: 'Verification',
                        path: '/admissions/verification',
                        icon: FileCheck
                    }
                ]
            },
            {
                id: 'students',
                label: 'Students',
                icon: Users,
                tier: 1,
                order: 3,
                items: [
                    {
                        id: 'all-students',
                        label: 'All Students',
                        path: '/students',
                        icon: Users
                    },
                    {
                        id: 'assignments',
                        label: 'Student Assignment',
                        path: '/academics/assignments',
                        icon: UserCheck
                    }
                ]
            },
            {
                id: 'academics',
                label: 'Academics',
                icon: GraduationCap,
                tier: 1,
                order: 4,
                items: [
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
                    },
                    {
                        id: 'attendance',
                        label: 'Class Attendance',
                        path: '/attendance',
                        icon: UserCheck
                    }
                ]
            },
            {
                id: 'finance',
                label: 'Finance',
                icon: DollarSign,
                tier: 1,
                order: 5,
                items: [
                    {
                        id: 'fee-collection',
                        label: 'Fee Collection',
                        path: '/finance/collection',
                        icon: DollarSign
                    },
                    {
                        id: 'payment-verification',
                        label: 'Payment Verification',
                        path: '/finance/verification',
                        icon: FileCheck
                    }
                ]
            },

            // TIER 2: CORE DOMAINS
            {
                id: 'faculty',
                label: 'Faculty',
                icon: Briefcase,
                tier: 2,
                order: 6,
                items: [
                    {
                        id: 'all-faculty',
                        label: 'All Faculty',
                        path: '/faculty',
                        icon: Briefcase
                    },
                    {
                        id: 'workload',
                        label: 'Workload',
                        path: '/faculty/workload',
                        icon: Clock
                    }
                ]
            },
            {
                id: 'library',
                label: 'Library',
                icon: Library,
                tier: 2,
                order: 7,
                items: [
                    {
                        id: 'books',
                        label: 'Books',
                        path: '/library/books',
                        icon: BookOpen
                    },
                    {
                        id: 'issues',
                        label: 'Issue/Return',
                        path: '/library/issues',
                        icon: FileInput
                    }
                ]
            },
            {
                id: 'hostel',
                label: 'Hostel',
                icon: BedDouble,
                tier: 2,
                order: 8,
                items: [
                    {
                        id: 'rooms',
                        label: 'Rooms',
                        path: '/hostel/rooms',
                        icon: BedDouble
                    },
                    {
                        id: 'gate-pass',
                        label: 'Gate Pass',
                        path: '/hostel/gate-pass',
                        icon: Key
                    }
                ]
            },

            // TIER 3: CONFIGURATION
            {
                id: 'academic-config',
                label: 'Academic Configuration',
                icon: GraduationCap,
                badge: 'config',
                tier: 3,
                order: 9,
                items: [
                    {
                        id: 'regulations',
                        label: 'Regulations',
                        path: '/config/academic/regulations',
                        icon: FileText,
                        badge: 'config',
                        description: 'Academic regulations and policies'
                    },
                    {
                        id: 'structure',
                        label: 'Academic Structure',
                        path: '/config/academic/structure',
                        icon: Layers,
                        badge: 'config',
                        description: 'Semesters, subjects, credits'
                    }
                ]
            },
            {
                id: 'finance-config',
                label: 'Finance Configuration',
                icon: DollarSign,
                badge: 'config',
                tier: 3,
                order: 10,
                items: [
                    {
                        id: 'fee-heads',
                        label: 'Fee Heads',
                        path: '/config/finance/fee-heads',
                        icon: DollarSign,
                        badge: 'config',
                        description: 'Fee categories and amounts'
                    },
                    {
                        id: 'scholarships',
                        label: 'Scholarships',
                        path: '/config/finance/scholarships',
                        icon: Award,
                        badge: 'config',
                        description: 'Scholarship schemes'
                    }
                ]
            },
            {
                id: 'admission-config',
                label: 'Admission Configuration',
                icon: ClipboardList,
                badge: 'config',
                tier: 3,
                order: 11,
                items: [
                    {
                        id: 'admission-settings',
                        label: 'Admission Settings',
                        path: '/config/admission/settings',
                        icon: Settings,
                        badge: 'config',
                        description: 'Admission process settings'
                    },
                    {
                        id: 'boards',
                        label: 'Boards',
                        path: '/config/admission/boards',
                        icon: School,
                        badge: 'config',
                        description: 'Education boards'
                    },
                    {
                        id: 'categories',
                        label: 'Categories',
                        path: '/config/admission/categories',
                        icon: Layers,
                        badge: 'config',
                        description: 'Student categories'
                    },
                    {
                        id: 'sources',
                        label: 'Sources',
                        path: '/config/admission/sources',
                        icon: Megaphone,
                        badge: 'config',
                        description: 'Admission sources'
                    }
                ]
            },

            // TIER 4: INSTITUTIONAL SETUP
            {
                id: 'institutional-setup',
                label: 'Institutional Setup',
                icon: Building,
                badge: 'setup',
                tier: 4,
                order: 12,
                items: [
                    {
                        id: 'institute',
                        label: 'Institute Information',
                        path: '/setup/institute',
                        icon: Building2,
                        badge: 'setup',
                        description: 'Basic institute details'
                    },
                    {
                        id: 'departments',
                        label: 'Departments',
                        path: '/setup/departments',
                        icon: Building,
                        badge: 'setup',
                        description: 'Academic departments'
                    },
                    {
                        id: 'programs',
                        label: 'Programs',
                        path: '/setup/programs',
                        icon: School,
                        badge: 'setup',
                        description: 'Degree programs'
                    },
                    {
                        id: 'academic-years',
                        label: 'Academic Years',
                        path: '/setup/academic-years',
                        icon: Calendar,
                        badge: 'setup',
                        description: 'Academic year setup'
                    },
                    {
                        id: 'batches',
                        label: 'Batches',
                        path: '/setup/batches',
                        icon: Users,
                        badge: 'setup',
                        description: 'Student batches'
                    },
                    {
                        id: 'designations',
                        label: 'Designations',
                        path: '/setup/designations',
                        icon: Award,
                        badge: 'setup',
                        description: 'Faculty designations'
                    }
                ]
            },

            // TIER 5: SYSTEM ADMINISTRATION
            {
                id: 'system-admin',
                label: 'System Administration',
                icon: Shield,
                badge: 'admin',
                tier: 5,
                order: 13,
                items: [
                    {
                        id: 'users',
                        label: 'Users',
                        path: '/system/users',
                        icon: UserCog,
                        badge: 'admin',
                        description: 'User management'
                    },
                    {
                        id: 'roles',
                        label: 'Roles & Permissions',
                        path: '/system/roles',
                        icon: Lock,
                        badge: 'admin',
                        description: 'Role-based access control'
                    },
                    {
                        id: 'integrations',
                        label: 'Integrations',
                        path: '/system/integrations',
                        icon: Database,
                        badge: 'admin',
                        description: 'Third-party integrations'
                    },
                    {
                        id: 'audit',
                        label: 'Audit Logs',
                        path: '/system/audit',
                        icon: Activity,
                        badge: 'admin',
                        description: 'System audit trail'
                    }
                ]
            }
        ],
        mobileBottomNav: COMMON_MOBILE_NAV
    },

    // PRINCIPAL: Same as SUPER_ADMIN but without System Administration
    PRINCIPAL: {
        groups: [], // Will be populated from SUPER_ADMIN, excluding tier 5
        mobileBottomNav: COMMON_MOBILE_NAV
    },

    // FACULTY: Simplified view
    FACULTY: {
        groups: [
            {
                id: 'dashboard',
                label: 'Dashboard',
                icon: LayoutDashboard,
                tier: 1,
                order: 1,
                items: [
                    {
                        id: 'home',
                        label: 'Home',
                        path: '/',
                        icon: LayoutDashboard
                    }
                ]
            },
            {
                id: 'academics',
                label: 'Academics',
                icon: GraduationCap,
                tier: 1,
                order: 2,
                items: [
                    {
                        id: 'timetable',
                        label: 'My Timetable',
                        path: '/timetable',
                        icon: Calendar
                    },
                    {
                        id: 'attendance',
                        label: 'Mark Attendance',
                        path: '/attendance',
                        icon: UserCheck
                    },
                    {
                        id: 'examinations',
                        label: 'Examinations',
                        path: '/exams',
                        icon: FileText
                    }
                ]
            }
        ],
        mobileBottomNav: COMMON_MOBILE_NAV
    },

    // STUDENT: Minimal view
    STUDENT: {
        groups: [
            {
                id: 'dashboard',
                label: 'Dashboard',
                icon: LayoutDashboard,
                tier: 1,
                order: 1,
                items: [
                    {
                        id: 'home',
                        label: 'Home',
                        path: '/',
                        icon: LayoutDashboard
                    }
                ]
            },
            {
                id: 'academics',
                label: 'Academics',
                icon: GraduationCap,
                tier: 1,
                order: 2,
                items: [
                    {
                        id: 'timetable',
                        label: 'Timetable',
                        path: '/timetable',
                        icon: Calendar
                    },
                    {
                        id: 'attendance',
                        label: 'My Attendance',
                        path: '/attendance',
                        icon: UserCheck
                    },
                    {
                        id: 'exams',
                        label: 'Examinations',
                        path: '/exams',
                        icon: FileText
                    }
                ]
            },
            {
                id: 'library',
                label: 'Library',
                icon: Library,
                tier: 2,
                order: 3,
                items: [
                    {
                        id: 'my-books',
                        label: 'My Books',
                        path: '/library/my-books',
                        icon: BookOpen
                    }
                ]
            }
        ],
        mobileBottomNav: COMMON_MOBILE_NAV
    },

    // PARENT: Minimal view
    PARENT: {
        groups: [
            {
                id: 'dashboard',
                label: 'Dashboard',
                icon: LayoutDashboard,
                tier: 1,
                order: 1,
                items: [
                    {
                        id: 'home',
                        label: 'Home',
                        path: '/',
                        icon: LayoutDashboard
                    }
                ]
            }
        ],
        mobileBottomNav: COMMON_MOBILE_NAV
    }
};

// ADMIN: Same as SUPER_ADMIN
NAVIGATION_CONFIG_V2.ADMIN = NAVIGATION_CONFIG_V2.SUPER_ADMIN;

/**
 * Populate PRINCIPAL navigation (same as SUPER_ADMIN minus tier 5)
 */
NAVIGATION_CONFIG_V2.PRINCIPAL.groups = NAVIGATION_CONFIG_V2.SUPER_ADMIN.groups.filter(
    group => group.tier !== 5
);

export const NAVIGATION_CONFIG = NAVIGATION_CONFIG_V2;

/**
 * Get badge label for display
 */
export function getBadgeLabel(badge: NavigationBadge): string {
    const labels: Record<NavigationBadge, string> = {
        config: 'Config',
        setup: 'Setup',
        admin: 'Admin'
    };
    return labels[badge];
}

/**
 * Get badge color classes
 */
export function getBadgeClasses(badge: NavigationBadge): string {
    const classes: Record<NavigationBadge, string> = {
        config: 'bg-blue-100 text-blue-700',
        setup: 'bg-purple-100 text-purple-700',
        admin: 'bg-red-100 text-red-700'
    };
    return classes[badge];
}

/**
 * Filter navigation based on user permissions
 */
export function filterNavigationByPermissions(
    groups: NavigationGroupV2[],
    userPermissions: string[]
): NavigationGroupV2[] {
    return groups
        .filter(group => {
            if (!group.requiredPermissions) return true;
            return group.requiredPermissions.some(perm => userPermissions.includes(perm));
        })
        .map(group => ({
            ...group,
            items: group.items.filter(item => {
                if (!item.requiredPermissions) return true;
                return item.requiredPermissions.some(perm => userPermissions.includes(perm));
            })
        }))
        .filter(group => group.items.length > 0);
}

/**
 * Filter navigation based on user roles
 */
export function filterNavigationByRoles(
    groups: NavigationGroupV2[],
    userRoles: string[]
): NavigationGroupV2[] {
    return groups
        .filter(group => {
            if (!group.requiredRoles) return true;
            return group.requiredRoles.some(role => userRoles.includes(role));
        })
        .map(group => ({
            ...group,
            items: group.items.filter(item => {
                if (!item.requiredRoles) return true;
                return item.requiredRoles.some(role => userRoles.includes(role));
            })
        }))
        .filter(group => group.items.length > 0);
}
