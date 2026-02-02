/**
 * Navigation System Types
 * Production-grade type definitions for grouped navigation
 */
import { LucideIcon } from 'lucide-react';

export interface NavItem {
    id: string;
    label: string;
    path: string;
    icon: LucideIcon;
    badge?: string;
    shortcut?: string;
    requiredPermissions?: string[];
}

export interface NavGroup {
    id: string;
    label: string;
    icon: LucideIcon;
    items: NavItem[];
    defaultExpanded?: boolean;
    order: number;
    requiredPermissions?: string[];
}

export interface NavigationConfig {
    groups: NavGroup[];
    mobileBottomNav: NavItem[];
}

export interface UserNavPreferences {
    userId: string;
    expandedGroups: string[];
    pinnedItems: string[];
    recentlyVisited: string[];
    sidebarCollapsed: boolean;
}

export interface Breadcrumb {
    label: string;
    path: string;
}
