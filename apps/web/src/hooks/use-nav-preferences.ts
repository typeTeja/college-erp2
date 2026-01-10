/**
 * Navigation Preferences Hook
 * Manages user navigation preferences with persistence
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { NavigationConfig } from '@/types/navigation';

interface NavPreferencesStore {
    expandedGroups: string[];
    pinnedItems: string[];
    recentlyVisited: string[];
    sidebarCollapsed: boolean;

    toggleGroup: (groupId: string) => void;
    toggleSidebar: () => void;
    pinItem: (itemId: string) => void;
    unpinItem: (itemId: string) => void;
    addToRecent: (itemId: string) => void;
    validatePinnedItems: (config: NavigationConfig) => void;
    initializeDefaults: (config: NavigationConfig) => void;
}

function getDefaultExpandedGroups(config: NavigationConfig): string[] {
    return config.groups
        .filter(group => group.defaultExpanded)
        .map(group => group.id);
}

export const useNavPreferences = create<NavPreferencesStore>()(
    persist(
        (set, get) => ({
            expandedGroups: [],
            pinnedItems: [],
            recentlyVisited: [],
            sidebarCollapsed: false,

            toggleGroup: (groupId) =>
                set((state) => ({
                    expandedGroups: state.expandedGroups.includes(groupId)
                        ? state.expandedGroups.filter((id) => id !== groupId)
                        : [...state.expandedGroups, groupId]
                })),

            toggleSidebar: () =>
                set((state) => ({
                    sidebarCollapsed: !state.sidebarCollapsed
                })),

            pinItem: (itemId) =>
                set((state) => ({
                    pinnedItems: state.pinnedItems.length < 5
                        ? [...state.pinnedItems, itemId]
                        : state.pinnedItems
                })),

            unpinItem: (itemId) =>
                set((state) => ({
                    pinnedItems: state.pinnedItems.filter((id) => id !== itemId)
                })),

            addToRecent: (itemId) =>
                set((state) => ({
                    recentlyVisited: [
                        itemId,
                        ...state.recentlyVisited.filter((id) => id !== itemId)
                    ].slice(0, 10)
                })),

            // Validate pinned items against current config
            validatePinnedItems: (config: NavigationConfig) => {
                const validIds = new Set(
                    config.groups.flatMap(g => g.items.map(i => i.id))
                );

                set(state => ({
                    pinnedItems: state.pinnedItems.filter(id => validIds.has(id))
                }));
            },

            // Initialize defaults from config
            initializeDefaults: (config: NavigationConfig) => {
                const stored = get().expandedGroups;
                if (stored.length === 0) {
                    set({ expandedGroups: getDefaultExpandedGroups(config) });
                }
            }
        }),
        {
            name: 'nav-preferences'
        }
    )
);
