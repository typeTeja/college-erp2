/**
 * Command Palette Component
 * Cmd+K / Ctrl+K quick navigation with permission validation
 */
'use client';

import { useState, useEffect, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import { Command } from 'cmdk';
import { Search } from 'lucide-react';
import { useNavigation } from '@/contexts/NavigationContext';
import { useNavPreferences } from '@/hooks/use-nav-preferences';
import { findItemById } from '@/utils/permissions';

export function CommandPalette() {
    const [open, setOpen] = useState(false);
    const router = useRouter();
    const { filteredConfig } = useNavigation();
    const { recentlyVisited, addToRecent } = useNavPreferences();

    // Cmd+K / Ctrl+K to open
    useEffect(() => {
        const down = (e: KeyboardEvent) => {
            if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                setOpen((open) => !open);
            }
        };

        document.addEventListener('keydown', down);
        return () => document.removeEventListener('keydown', down);
    }, []);

    // Validate recently visited against filtered config
    const validRecentItems = useMemo(() => {
        const validIds = new Set(
            filteredConfig.groups.flatMap(g => g.items.map(i => i.id))
        );
        return recentlyVisited.filter(id => validIds.has(id)).slice(0, 5);
    }, [recentlyVisited, filteredConfig]);

    const [search, setSearch] = useState('');

    const filteredGroups = useMemo(() => {
        if (!search) return filteredConfig.groups;

        const lowerSearch = search.toLowerCase();

        return filteredConfig.groups.map(group => {
            const filteredItems = group.items.filter(item => {
                // Match label
                if (item.label.toLowerCase().includes(lowerSearch)) return true;
                
                // Match aliases
                if (item.aliases?.some(alias => alias.toLowerCase().includes(lowerSearch))) return true;
                
                return false;
            });

            return {
                ...group,
                items: filteredItems
            };
        }).filter(group => group.items.length > 0);
    }, [filteredConfig.groups, search]);

    const handleSelect = (path: string, itemId: string) => {
        router.push(path);
        addToRecent(itemId);
        setOpen(false);
        setSearch('');
    };

    return (
        <Command.Dialog
            open={open}
            onOpenChange={setOpen}
            className="fixed top-1/4 left-1/2 -translate-x-1/2 w-full max-w-2xl bg-white rounded-lg shadow-2xl border z-50"
        >
            <div className="flex items-center border-b px-4">
                <Search className="h-5 w-5 text-gray-400 mr-2" />
                <Command.Input
                    placeholder="Search menu or type 'settings'..."
                    className="flex-1 py-3 outline-none text-sm"
                    value={search}
                    onValueChange={setSearch}
                />
            </div>

            <Command.List className="max-h-96 overflow-y-auto p-2">
                <Command.Empty className="py-6 text-center text-sm text-gray-500">
                    No results found.
                </Command.Empty>

                {/* Recently Visited (only show when not searching) */}
                {!search && validRecentItems.length > 0 && (
                    <Command.Group heading="Recently Visited" className="mb-2">
                        {validRecentItems.map((itemId) => {
                            const item = findItemById(filteredConfig.groups, itemId);
                            if (!item) return null;

                            const ItemIcon = item.icon;

                            return (
                                <Command.Item
                                    key={itemId}
                                    onSelect={() => handleSelect(item.path, item.id)}
                                    className="flex items-center gap-2 px-3 py-2 rounded-md cursor-pointer hover:bg-gray-100 aria-selected:bg-gray-100"
                                >
                                    <ItemIcon className="h-4 w-4 text-gray-500" />
                                    <span className="flex-1 text-sm">{item.label}</span>
                                </Command.Item>
                            );
                        })}
                    </Command.Group>
                )}

                {/* Filtered Groups */}
                {filteredGroups.map((group) => (
                    <Command.Group
                        key={group.id}
                        heading={group.label}
                        className="mb-2"
                    >
                        {group.items.map((item) => {
                            const ItemIcon = item.icon;

                            return (
                                <Command.Item
                                    key={item.id}
                                    onSelect={() => handleSelect(item.path, item.id)}
                                    className="flex items-center gap-2 px-3 py-2 rounded-md cursor-pointer hover:bg-gray-100 aria-selected:bg-gray-100"
                                >
                                    <ItemIcon className="h-4 w-4 text-gray-500" />
                                    <span className="flex-1 text-sm">{item.label}</span>
                                    {item.badge && (
                                        <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs">
                                            {item.badge}
                                        </span>
                                    )}
                                    {item.shortcut && (
                                        <kbd className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-mono">
                                            {item.shortcut}
                                        </kbd>
                                    )}
                                </Command.Item>
                            );
                        })}
                    </Command.Group>
                ))}
            </Command.List>
        </Command.Dialog>
    );
}
