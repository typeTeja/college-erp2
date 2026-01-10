/**
 * Keyboard Shortcuts Hook
 * Safe keyboard navigation with modifier guards and input context awareness
 */
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useNavigation } from '@/contexts/NavigationContext';

const FEATURE_FLAG_SHORTCUTS = true;

export function useKeyboardShortcuts() {
    const router = useRouter();
    const { filteredConfig } = useNavigation();

    useEffect(() => {
        if (!FEATURE_FLAG_SHORTCUTS) return;

        let keys: string[] = [];
        let timeout: NodeJS.Timeout;

        const handleKeyDown = (e: KeyboardEvent) => {
            const target = e.target as HTMLElement;

            // Ignore shortcuts in input contexts
            if (
                target.tagName === 'INPUT' ||
                target.tagName === 'TEXTAREA' ||
                target.isContentEditable
            ) {
                return;
            }

            // Require modifier key to start sequence
            if (keys.length === 0 && !e.altKey && !e.metaKey) {
                return;
            }

            keys.push(e.key.toLowerCase());
            clearTimeout(timeout);

            timeout = setTimeout(() => {
                keys = [];
            }, 1000);

            const combo = keys.join(' ');
            const allItems = filteredConfig.groups.flatMap(g => g.items);
            const matchedItem = allItems.find(item => item.shortcut === combo);

            if (matchedItem) {
                e.preventDefault();
                router.push(matchedItem.path);
                keys = [];
            }
        };

        document.addEventListener('keydown', handleKeyDown);
        return () => document.removeEventListener('keydown', handleKeyDown);
    }, [router, filteredConfig]);
}
