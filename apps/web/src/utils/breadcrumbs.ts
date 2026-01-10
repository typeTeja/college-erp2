/**
 * Breadcrumb Utilities
 * Generate breadcrumbs from navigation config
 */
import { findItemByPath } from '@/utils/permissions';
import type { Breadcrumb, NavigationConfig } from '@/types/navigation';

/**
 * Generate breadcrumbs from pathname
 * Includes group labels and uses longest prefix matching
 */
export function generateBreadcrumbs(
    pathname: string,
    filteredConfig: NavigationConfig
): Breadcrumb[] {
    const breadcrumbs: Breadcrumb[] = [
        { label: 'Home', path: '/' }
    ];

    // Skip if on home page
    if (pathname === '/') {
        return breadcrumbs;
    }

    let currentPath = '';
    const segments = pathname.split('/').filter(Boolean);

    for (let i = 0; i < segments.length; i++) {
        currentPath += `/${segments[i]}`;

        const match = findItemByPath(filteredConfig.groups, currentPath);

        if (match) {
            // Add group label if not already added
            const lastBreadcrumb = breadcrumbs[breadcrumbs.length - 1];
            if (lastBreadcrumb.label !== match.group.label) {
                breadcrumbs.push({
                    label: match.group.label,
                    path: match.item.path
                });
            }

            // Add item label
            breadcrumbs.push({
                label: match.item.label,
                path: match.item.path
            });

            // Skip remaining segments if matched
            break;
        } else {
            // Dynamic segment (e.g., /students/123)
            const label = segments[i].charAt(0).toUpperCase() + segments[i].slice(1);
            breadcrumbs.push({
                label,
                path: currentPath
            });
        }
    }

    return breadcrumbs;
}
