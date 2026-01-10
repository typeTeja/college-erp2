/**
 * Navigation Context Provider
 * Provides memoized filtered navigation to all components
 */
'use client';

import { createContext, useContext, useMemo, useEffect } from 'react';
import { filterNavigation } from '@/utils/permissions';
import { NAVIGATION_CONFIG } from '@/config/navigation';
import { useNavPreferences } from '@/hooks/use-nav-preferences';
import type { NavigationConfig } from '@/types/navigation';

interface NavigationContextValue {
    filteredConfig: NavigationConfig;
    role: string;
    userPermissions: string[];
}

const NavigationContext = createContext<NavigationContextValue | null>(null);

export function NavigationProvider({
    children,
    role,
    userPermissions
}: {
    children: React.ReactNode;
    role: string;
    userPermissions: string[];
}) {
    const { validatePinnedItems, initializeDefaults } = useNavPreferences();

    // Memoize filtering once per layout
    const filteredConfig = useMemo(
        () => filterNavigation(NAVIGATION_CONFIG[role] || NAVIGATION_CONFIG.SUPER_ADMIN, userPermissions),
        [role, userPermissions]
    );

    // Initialize preferences on mount
    useEffect(() => {
        initializeDefaults(filteredConfig);
        validatePinnedItems(filteredConfig);
    }, [filteredConfig, initializeDefaults, validatePinnedItems]);

    return (
        <NavigationContext.Provider value={{ filteredConfig, role, userPermissions }}>
            {children}
        </NavigationContext.Provider>
    );
}

export function useNavigation() {
    const context = useContext(NavigationContext);
    if (!context) {
        throw new Error('useNavigation must be used within NavigationProvider');
    }
    return context;
}
