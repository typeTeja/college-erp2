import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
    FileQuestion, Users, BookOpen, Calendar, 
    DollarSign, Home, Search, Plus 
} from 'lucide-react';

/**
 * EmptyState Component
 * 
 * Reusable empty state component following UX laws:
 * - Miller's Law: Clear, concise messaging (5-7 words max for title)
 * - Fitts's Law: Large, centered action button
 * - Visual hierarchy with icon, title, description, action
 * 
 * Usage:
 * <EmptyState
 *   icon={<Users />}
 *   title="No students found"
 *   description="Get started by adding your first student"
 *   actionLabel="Add Student"
 *   onAction={handleAddStudent}
 * />
 */

interface EmptyStateProps {
    icon?: React.ReactNode;
    title: string;
    description?: string;
    actionLabel?: string;
    onAction?: () => void;
    variant?: 'default' | 'search' | 'error';
    className?: string;
}

export function EmptyState({
    icon,
    title,
    description,
    actionLabel,
    onAction,
    variant = 'default',
    className = '',
}: EmptyStateProps) {
    const defaultIcons = {
        default: <FileQuestion className="h-12 w-12 text-slate-300" />,
        search: <Search className="h-12 w-12 text-slate-300" />,
        error: <FileQuestion className="h-12 w-12 text-red-300" />,
    };

    return (
        <div className={`text-center py-12 ${className}`}>
            <div className="flex justify-center mb-4">
                {icon || defaultIcons[variant]}
            </div>
            
            {/* Miller's Law: Keep title concise (5-7 words) */}
            <h3 className="text-lg font-semibold text-slate-900 mb-2">
                {title}
            </h3>
            
            {description && (
                <p className="text-sm text-slate-500 mb-6 max-w-md mx-auto">
                    {description}
                </p>
            )}
            
            {/* Fitts's Law: Large, centered action button */}
            {actionLabel && onAction && (
                <Button
                    onClick={onAction}
                    className="min-w-[140px] h-10"
                >
                    <Plus className="h-4 w-4 mr-2" />
                    {actionLabel}
                </Button>
            )}
        </div>
    );
}

/**
 * EmptyStateCard Component
 * 
 * Empty state wrapped in a card with dashed border
 * Commonly used in list views and tables
 */
export function EmptyStateCard(props: EmptyStateProps) {
    return (
        <Card className="border-2 border-dashed border-slate-200 bg-slate-50">
            <CardContent className="p-8">
                <EmptyState {...props} />
            </CardContent>
        </Card>
    );
}

/**
 * Pre-configured empty states for common scenarios
 */
export const EmptyStates = {
    Students: (props: Partial<EmptyStateProps>) => (
        <EmptyState
            icon={<Users className="h-12 w-12 text-slate-300" />}
            title="No students found"
            description="Get started by adding your first student to the system"
            actionLabel="Add Student"
            {...props}
        />
    ),
    
    Faculty: (props: Partial<EmptyStateProps>) => (
        <EmptyState
            icon={<Users className="h-12 w-12 text-slate-300" />}
            title="No faculty found"
            description="Add faculty members to manage courses and students"
            actionLabel="Add Faculty"
            {...props}
        />
    ),
    
    Courses: (props: Partial<EmptyStateProps>) => (
        <EmptyState
            icon={<BookOpen className="h-12 w-12 text-slate-300" />}
            title="No courses found"
            description="Create your first course to get started"
            actionLabel="Add Course"
            {...props}
        />
    ),
    
    Events: (props: Partial<EmptyStateProps>) => (
        <EmptyState
            icon={<Calendar className="h-12 w-12 text-slate-300" />}
            title="No events scheduled"
            description="Schedule events to keep everyone informed"
            actionLabel="Create Event"
            {...props}
        />
    ),
    
    Payments: (props: Partial<EmptyStateProps>) => (
        <EmptyState
            icon={<DollarSign className="h-12 w-12 text-slate-300" />}
            title="No payments found"
            description="Payment history will appear here"
            {...props}
        />
    ),
    
    Hostel: (props: Partial<EmptyStateProps>) => (
        <EmptyState
            icon={<Home className="h-12 w-12 text-slate-300" />}
            title="No hostel records"
            description="Add hostel information to manage accommodations"
            actionLabel="Add Hostel"
            {...props}
        />
    ),
    
    Search: (props: Partial<EmptyStateProps>) => (
        <EmptyState
            icon={<Search className="h-12 w-12 text-slate-300" />}
            title="No results found"
            description="Try adjusting your search or filters"
            variant="search"
            {...props}
        />
    ),
};
