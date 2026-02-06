"use client";

import React, { useState } from 'react';
import { TreeSidebar } from './TreeSidebar';
import { StructureNode } from './types';
import { Card } from '@/components/ui/card';
import { Menu, PanelLeftClose, PanelLeftOpen } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
// We'll import DetailPanel later
import { DetailPanel } from './DetailPanel';

export function StructureExplorer() {
    const [selectedNode, setSelectedNode] = useState<StructureNode | null>(null);
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    return (
        <div className="flex h-[calc(100vh-140px)] border rounded-xl overflow-hidden bg-white shadow-sm">
            {/* Sidebar Column */}
            <div 
                className={cn(
                    "flex flex-col border-r bg-slate-50 transition-all duration-300 ease-in-out",
                    isSidebarOpen ? "w-[350px]" : "w-0 opacity-0 overflow-hidden"
                )}
            >
                <div className="h-10 px-4 flex items-center justify-between border-b bg-slate-100/50">
                    <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                        Browser
                    </span>
                    <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-6 w-6" 
                        onClick={() => setIsSidebarOpen(false)}
                    >
                        <PanelLeftClose className="h-3.5 w-3.5" />
                    </Button>
                </div>
                
                <div className="flex-1 overflow-y-auto p-2">
                    <TreeSidebar 
                        selectedNodeId={selectedNode?.id || null} 
                        onSelectNode={setSelectedNode} 
                    />
                </div>
            </div>

            {/* Main Content Column */}
            <div className="flex-1 flex flex-col min-w-0 bg-white">
                {!isSidebarOpen && (
                    <div className="h-10 border-b flex items-center px-4">
                        <Button 
                            variant="ghost" 
                            size="sm" 
                            className="gap-2 text-slate-500"
                            onClick={() => setIsSidebarOpen(true)}
                        >
                            <PanelLeftOpen className="h-4 w-4" />
                            <span className="text-xs">Open Explorer</span>
                        </Button>
                    </div>
                )}

                <div className="flex-1 overflow-y-auto p-6">
                    {selectedNode ? (
                        <DetailPanel node={selectedNode} />
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center text-slate-400">
                            <Menu className="h-12 w-12 mb-4 opacity-20" />
                            <p className="text-sm font-medium">Select an item from the tree to view details</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
