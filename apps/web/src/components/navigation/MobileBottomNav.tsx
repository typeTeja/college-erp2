/**
 * Mobile Bottom Navigation
 * Bottom navigation bar for mobile devices with permission checking
 */
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { useNavigation } from '@/contexts/NavigationContext';
import { MobileMoreMenu } from './MobileMoreMenu';

export function MobileBottomNav() {
    const pathname = usePathname();
    const { filteredConfig } = useNavigation();
    const [showMore, setShowMore] = useState(false);

    const isActive = (path: string) => {
        if (path === '/') return pathname === '/';
        return pathname.startsWith(path);
    };

    return (
        <>
            <nav
                className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 md:hidden z-50"
                role="navigation"
                aria-label="Mobile navigation"
            >
                <div className="flex justify-around items-center h-16">
                    {filteredConfig.mobileBottomNav.map((item) => {
                        const Icon = item.icon;
                        const active = isActive(item.path);

                        if (item.id === 'more') {
                            return (
                                <button
                                    key={item.id}
                                    onClick={() => setShowMore(true)}
                                    className="flex flex-col items-center justify-center flex-1 py-2 text-gray-600 hover:text-blue-600 transition-colors"
                                    aria-label="More menu"
                                >
                                    <Icon className="h-6 w-6" />
                                    <span className="text-xs mt-1">{item.label}</span>
                                </button>
                            );
                        }

                        return (
                            <Link
                                key={item.id}
                                href={item.path}
                                className={`flex flex-col items-center justify-center flex-1 py-2 transition-colors ${active
                                        ? 'text-blue-600'
                                        : 'text-gray-600 hover:text-blue-600'
                                    }`}
                                aria-current={active ? 'page' : undefined}
                            >
                                <Icon className="h-6 w-6" />
                                <span className="text-xs mt-1">{item.label}</span>
                            </Link>
                        );
                    })}
                </div>
            </nav>

            {/* More Menu Modal */}
            {showMore && (
                <MobileMoreMenu
                    onClose={() => setShowMore(false)}
                />
            )}
        </>
    );
}
