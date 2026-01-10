/**
 * Breadcrumbs Component
 * Auto-generated breadcrumbs from navigation config
 */
'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { ChevronRight, Home } from 'lucide-react';
import { useNavigation } from '@/contexts/NavigationContext';
import { generateBreadcrumbs } from '@/utils/breadcrumbs';

export function Breadcrumbs() {
    const pathname = usePathname();
    const { filteredConfig } = useNavigation();

    const breadcrumbs = generateBreadcrumbs(pathname, filteredConfig);

    // Don't show breadcrumbs on home page
    if (breadcrumbs.length <= 1) {
        return null;
    }

    return (
        <nav
            className="flex items-center gap-2 text-sm text-gray-600 mb-4"
            aria-label="Breadcrumb"
        >
            <Link
                href="/"
                className="hover:text-gray-900 transition-colors"
                aria-label="Home"
            >
                <Home className="h-4 w-4" />
            </Link>

            {breadcrumbs.slice(1).map((crumb, index) => {
                const isLast = index === breadcrumbs.length - 2;

                return (
                    <div key={`breadcrumb-${index}`} className="flex items-center gap-2">
                        <ChevronRight className="h-4 w-4 text-gray-400" />
                        {isLast ? (
                            <span
                                className="text-gray-900 font-medium"
                                aria-current="page"
                            >
                                {crumb.label}
                            </span>
                        ) : (
                            <Link
                                href={crumb.path}
                                className="hover:text-gray-900 transition-colors"
                            >
                                {crumb.label}
                            </Link>
                        )}
                    </div>
                );
            })}
        </nav>
    );
}
