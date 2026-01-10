/**
 * Grouped Sidebar Component
 * Production-grade sidebar with groups, accessibility, and tooltips
 */
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronDown, ChevronRight, HelpCircle, Menu, X } from 'lucide-react';
import { useNavigation } from '@/contexts/NavigationContext';
import { useNavPreferences } from '@/hooks/use-nav-preferences';
import { Tooltip, TooltipContent, TooltipTrigger, TooltipProvider } from '@/components/ui/tooltip';

const DefaultIcon = HelpCircle;

export function GroupedSidebar() {
    const pathname = usePathname();
    const { filteredConfig } = useNavigation();
    const {
        expandedGroups,
        sidebarCollapsed,
        toggleGroup,
        toggleSidebar
    } = useNavPreferences();

    const isActive = (itemPath: string) => {
        if (itemPath === '/') {
            return pathname === '/';
        }
        return pathname.startsWith(itemPath);
    };

    const isGroupActive = (items: any[]) =>
        items.some(item => isActive(item.path));

    return (
        <aside
            className={`fixed left-0 top-0 h-screen bg-white border-r border-gray-200 z-40 transition-all duration-300 ${sidebarCollapsed ? 'w-20' : 'w-64'
                }`}
            role="navigation"
            aria-label="Main navigation"
        >
            <div className="flex flex-col h-full">
                {/* Header */}
                <div className="p-4 border-b border-gray-200 flex items-center justify-between">
                    {!sidebarCollapsed && (
                        <h1 className="text-lg font-semibold text-gray-900">College ERP</h1>
                    )}
                    <button
                        onClick={toggleSidebar}
                        className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                        aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                    >
                        {sidebarCollapsed ? <Menu className="h-5 w-5" /> : <X className="h-5 w-5" />}
                    </button>
                </div>

                {/* Navigation */}
                <TooltipProvider>
                    <nav className="flex-1 overflow-y-auto p-4 space-y-1">
                        {filteredConfig.groups.map((group) => {
                            const isExpanded = expandedGroups.includes(group.id);
                            const GroupIcon = group.icon ?? DefaultIcon;
                            const groupIsActive = isGroupActive(group.items);
                            const isSingleItem = group.items.length === 1;

                            // For single-item groups, render as direct link
                            if (isSingleItem) {
                                const item = group.items[0];
                                const ItemIcon = item.icon ?? DefaultIcon;
                                const itemIsActive = isActive(item.path);

                                return (
                                    <Tooltip key={group.id}>
                                        <TooltipTrigger asChild>
                                            <Link
                                                href={item.path}
                                                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${itemIsActive
                                                        ? 'bg-blue-600 text-white'
                                                        : 'hover:bg-gray-100 text-gray-700'
                                                    }`}
                                                aria-current={itemIsActive ? 'page' : undefined}
                                            >
                                                <ItemIcon className="h-5 w-5 shrink-0" />
                                                {!sidebarCollapsed && (
                                                    <>
                                                        <span className="flex-1 font-medium text-sm">
                                                            {group.label}
                                                        </span>
                                                        {item.badge && (
                                                            <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs">
                                                                {item.badge}
                                                            </span>
                                                        )}
                                                    </>
                                                )}
                                            </Link>
                                        </TooltipTrigger>
                                        {item.shortcut && (
                                            <TooltipContent side="right">
                                                <p className="text-xs">
                                                    Shortcut: <kbd className="px-1 bg-gray-200 rounded">{item.shortcut}</kbd>
                                                </p>
                                            </TooltipContent>
                                        )}
                                    </Tooltip>
                                );
                            }

                            // For multi-item groups, render as collapsible dropdown
                            return (
                                <div key={group.id} className="mb-1">
                                    {/* Group Header */}
                                    <button
                                        onClick={() => toggleGroup(group.id)}
                                        className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${groupIsActive
                                                ? 'bg-blue-50 text-blue-700'
                                                : 'hover:bg-gray-100 text-gray-700'
                                            }`}
                                        aria-expanded={isExpanded}
                                        aria-controls={`group-${group.id}`}
                                    >
                                        <GroupIcon className="h-5 w-5 shrink-0" />
                                        {!sidebarCollapsed && (
                                            <>
                                                <span className="flex-1 text-left font-medium text-sm">
                                                    {group.label}
                                                </span>
                                                {isExpanded ? (
                                                    <ChevronDown className="h-4 w-4" />
                                                ) : (
                                                    <ChevronRight className="h-4 w-4" />
                                                )}
                                            </>
                                        )}
                                    </button>

                                    {/* Group Items */}
                                    {isExpanded && !sidebarCollapsed && (
                                        <div id={`group-${group.id}`} className="pl-6 mt-1 space-y-1">
                                            {group.items.map((item) => {
                                                const ItemIcon = item.icon ?? DefaultIcon;
                                                const itemIsActive = isActive(item.path);

                                                return (
                                                    <Tooltip key={item.id}>
                                                        <TooltipTrigger asChild>
                                                            <Link
                                                                href={item.path}
                                                                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm ${itemIsActive
                                                                        ? 'bg-blue-600 text-white'
                                                                        : 'hover:bg-gray-100 text-gray-700'
                                                                    }`}
                                                                aria-current={itemIsActive ? 'page' : undefined}
                                                            >
                                                                <ItemIcon className="h-4 w-4 shrink-0" />
                                                                <span className="flex-1">{item.label}</span>
                                                                {item.badge && (
                                                                    <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs">
                                                                        {item.badge}
                                                                    </span>
                                                                )}
                                                            </Link>
                                                        </TooltipTrigger>
                                                        {item.shortcut && (
                                                            <TooltipContent side="right">
                                                                <p className="text-xs">
                                                                    Shortcut: <kbd className="px-1 bg-gray-200 rounded">{item.shortcut}</kbd>
                                                                </p>
                                                            </TooltipContent>
                                                        )}
                                                    </Tooltip>
                                                );
                                            })}
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </nav>
                </TooltipProvider>
            </div>
        </aside>
    );
}
