/**
 * Focus Trap Hook
 * Traps focus within a modal for accessibility
 */
'use client';

import { useEffect } from 'react';

export function useFocusTrap(
    ref: React.RefObject<HTMLElement | null>,
    active: boolean
) {
    useEffect(() => {
        if (!active || !ref.current) return;

        const element = ref.current;
        const focusableElements = element.querySelectorAll(
            'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0] as HTMLElement;
        const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

        // Store previous active element to restore on close
        const previousActiveElement = document.activeElement as HTMLElement;

        firstElement?.focus();

        const handleTab = (e: KeyboardEvent) => {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement?.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement?.focus();
                }
            }
        };

        element.addEventListener('keydown', handleTab);

        return () => {
            element.removeEventListener('keydown', handleTab);
            previousActiveElement?.focus();
        };
    }, [ref, active]);
}
