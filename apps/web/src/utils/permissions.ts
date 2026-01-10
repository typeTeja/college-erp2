/**
 * Permission Utilities
 * Centralized permission checking and navigation filtering
 */
import type { NavigationConfig, NavGroup, NavItem } from '@/types/navigation';

/**
 * Check if user has required permissions
 */
export function hasPermission(
    requiredPermissions: string[] | undefined,
    userPermissions: string[]
): boolean {
    if (!requiredPermissions || requiredPermissions.length === 0) {
        return true;
    }
    return requiredPermissions.some(p => userPermissions.includes(p));
}

/**
 * Filter navigation config based on user permissions
 * Single source of truth for permission-based filtering
 */
export function filterNavigation(
    config: NavigationConfig,
    userPermissions: string[]
): NavigationConfig {
    return {
        ...config,
        groups: config.groups
            .map(group => ({
                ...group,
                items: group.items.filter(item =>
                    hasPermission(item.requiredPermissions, userPermissions)
                )
            }))
            .filter(group => group.items.length > 0), // Remove empty groups
        mobileBottomNav: config.mobileBottomNav.filter(item =>
            hasPermission(item.requiredPermissions, userPermissions)
        )
    };
}

/**
 * Find navigation item by ID
 */
export function findItemById(groups: NavGroup[], itemId: string): NavItem | null {
    for (const group of groups) {
        const item = group.items.find(i => i.id === itemId);
        if (item) return item;
    }
    return null;
}

/**
 * Find navigation item by path (longest prefix match)
 */
export function findItemByPath(
    groups: NavGroup[],
    path: string
): { item: NavItem; group: NavGroup } | null {
    for (const group of groups) {
        // Match longest prefix, not exact
        const matchedItem = group.items
            .filter(i => path.startsWith(i.path))
            .sort((a, b) => b.path.length - a.path.length)[0];

        if (matchedItem) {
            return { item: matchedItem, group };
        }
    }
    return null;
}
