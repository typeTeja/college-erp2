import React from 'react';
import { 
    ChevronRight, 
    ChevronDown, 
    Calendar, 
    GraduationCap, 
    BookOpen, 
    Layers, 
    Clock, 
    Users, 
    FlaskConical 
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import { StructureNode } from './types';

interface TreeNodeProps {
    node: StructureNode;
    level: number;
    isExpanded: boolean;
    isSelected: boolean;
    onToggle: (node: StructureNode) => void;
    onSelect: (node: StructureNode) => void;
    isLoading?: boolean;
}

export const TreeNode: React.FC<TreeNodeProps> = ({
    node,
    level,
    isExpanded,
    isSelected,
    onToggle,
    onSelect,
    isLoading
}) => {
    const Icon = getNodeIcon(node.type);

    const handleToggle = (e: React.MouseEvent) => {
        e.stopPropagation();
        onToggle(node);
    };

    const handleSelect = (e: React.MouseEvent) => {
        e.stopPropagation();
        onSelect(node);
    };

    return (
        <div 
            className={cn(
                "group flex items-center py-1.5 px-2 cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors rounded-md mx-1",
                isSelected && "bg-blue-50 text-blue-700 hover:bg-blue-100 dark:bg-blue-900/20 dark:text-blue-300"
            )}
            style={{ paddingLeft: `${level * 16 + 8}px` }}
            onClick={handleSelect}
        >
            {/* Toggle Icon or Spacer */}
            <div className="w-5 h-5 flex items-center justify-center shrink-0 mr-1">
                {(node.hasChildren || (node.children && node.children.length > 0)) && (
                    <button 
                        onClick={handleToggle}
                        className="p-0.5 rounded-sm hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-400 hover:text-slate-600 transition-colors"
                    >
                        {isExpanded ? (
                            <ChevronDown className="w-4 h-4" />
                        ) : (
                            <ChevronRight className="w-4 h-4" />
                        )}
                    </button>
                )}
            </div>

            {/* Node Icon */}
            <Icon className={cn(
                "w-4 h-4 mr-2 shrink-0",
                getNodeColor(node.type)
            )} />

            {/* Label */}
            <span className="text-sm font-medium truncate flex-1 leading-none select-none">
                {node.label}
            </span>

            {/* Badges/Indicators */}
            {isLoading && (
                <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse ml-2" />
            )}
            
            {node.details?.count !== undefined && (
                <Badge variant="secondary" className="ml-2 h-5 px-1.5 text-[10px] min-w-[20px] justify-center">
                    {node.details.count}
                </Badge>
            )}
        </div>
    );
};

function getNodeIcon(type: string) {
    switch (type) {
        case 'ROOT': return Calendar; // Or some global icon
        case 'YEAR': return Calendar;
        case 'PROGRAM': return GraduationCap;
        case 'REGULATION': return BookOpen;
        case 'BATCH': return Layers;
        case 'SEMESTER': return Clock;
        case 'SECTION_GROUP': return Users;
        case 'SECTION': return Users;
        case 'LAB_GROUP': return FlaskConical;
        case 'LAB': return FlaskConical;
        default: return Layers;
    }
}

function getNodeColor(type: string) {
    switch (type) {
        case 'YEAR': return "text-indigo-500";
        case 'PROGRAM': return "text-purple-600";
        case 'REGULATION': return "text-amber-600";
        case 'BATCH': return "text-blue-600";
        case 'SEMESTER': return "text-emerald-600";
        case 'SECTION': return "text-slate-600";
        case 'LAB': return "text-teal-600";
        default: return "text-slate-500";
    }
}
