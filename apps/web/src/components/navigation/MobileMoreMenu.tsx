/**
 * Mobile More Menu
 * Full-screen modal showing all navigation groups on mobile
 */
'use client';

import { useRef } from 'react';
import Link from 'next/link';
import { X } from 'lucide-react';
import { useNavigation } from '@/contexts/NavigationContext';
import { useFocusTrap } from '@/hooks/use-focus-trap';

interface MobileMoreMenuProps {
    onClose: () => void;
}

export function MobileMoreMenu({ onClose }: MobileMoreMenuProps) {
    const modalRef = useRef<HTMLDivElement>(null);
    const { filteredConfig } = useNavigation();

    // Focus trap for accessibility
    useFocusTrap(modalRef, true);

    return (
        <div
            className="fixed inset-0 bg-black/50 z-50 md:hidden"
            onClick={onClose}
        >
            <div
                ref={modalRef}
                className="absolute bottom-0 left-0 right-0 bg-white rounded-t-2xl p-6 max-h-[80vh] overflow-y-auto"
                onClick={(e) => e.stopPropagation()}
                role="dialog"
                aria-modal="true"
                aria-label="More menu"
            >
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    aria-label="Close menu"
                >
                    <X className="h-6 w-6" />
                </button>

                <h2 className="text-lg font-semibold mb-6">Menu</h2>

                {filteredConfig.groups.map(group => {
                    const GroupIcon = group.icon;

                    return (
                        <div key={group.id} className="mb-6">
                            <div className="flex items-center gap-2 mb-3">
                                <GroupIcon className="h-5 w-5 text-gray-600" />
                                <h3 className="text-sm font-medium text-gray-700 uppercase">
                                    {group.label}
                                </h3>
                            </div>

                            <div className="space-y-1">
                                {group.items.map(item => {
                                    const ItemIcon = item.icon;

                                    return (
                                        <Link
                                            key={item.id}
                                            href={item.path}
                                            onClick={onClose}
                                            className="flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-gray-100 transition-colors"
                                        >
                                            <ItemIcon className="h-5 w-5 text-gray-600" />
                                            <span className="flex-1 text-sm">{item.label}</span>
                                            {item.badge && (
                                                <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs">
                                                    {item.badge}
                                                </span>
                                            )}
                                        </Link>
                                    );
                                })}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
