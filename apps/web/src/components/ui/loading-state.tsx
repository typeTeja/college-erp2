import React from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Loader2 } from 'lucide-react';

/**
 * LoadingState Component
 * 
 * Reusable loading state with spinner and message
 * Following UX laws:
 * - Provide feedback (Jakob's Law)
 * - Keep users informed (Visibility of System Status)
 * 
 * Usage:
 * <LoadingState message="Loading students..." />
 */

interface LoadingStateProps {
    message?: string;
    size?: 'sm' | 'md' | 'lg';
    className?: string;
}

export function LoadingState({
    message = 'Loading...',
    size = 'md',
    className = '',
}: LoadingStateProps) {
    const sizeClasses = {
        sm: 'h-4 w-4',
        md: 'h-8 w-8',
        lg: 'h-12 w-12',
    };

    const paddingClasses = {
        sm: 'py-4',
        md: 'py-8',
        lg: 'py-12',
    };

    return (
        <div className={`text-center ${paddingClasses[size]} ${className}`}>
            <div className="flex justify-center mb-3">
                <Loader2 className={`${sizeClasses[size]} text-blue-600 animate-spin`} />
            </div>
            <p className="text-sm text-slate-600">{message}</p>
        </div>
    );
}

/**
 * LoadingCard Component
 * 
 * Loading state wrapped in a card
 */
export function LoadingCard({ message }: { message?: string }) {
    return (
        <Card>
            <CardContent className="p-8">
                <LoadingState message={message} />
            </CardContent>
        </Card>
    );
}

/**
 * Skeleton Screens for Dashboards
 * 
 * Pre-built skeleton screens for common dashboard layouts
 */

export function DashboardSkeleton() {
    return (
        <div className="space-y-6">
            {/* Header Skeleton */}
            <div className="space-y-2">
                <Skeleton className="h-8 w-64" />
                <Skeleton className="h-4 w-96" />
            </div>

            {/* KPI Cards Skeleton */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {[1, 2, 3, 4].map((i) => (
                    <Card key={i}>
                        <CardContent className="pt-6">
                            <Skeleton className="h-4 w-24 mb-2" />
                            <Skeleton className="h-8 w-16" />
                        </CardContent>
                    </Card>
                ))}
            </div>

            {/* Main Content Grid Skeleton */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {[1, 2].map((i) => (
                    <Card key={i}>
                        <CardHeader>
                            <Skeleton className="h-6 w-48" />
                            <Skeleton className="h-4 w-64 mt-2" />
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-3">
                                {[1, 2, 3].map((j) => (
                                    <Skeleton key={j} className="h-16 w-full" />
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
    return (
        <div className="space-y-3">
            {/* Table Header */}
            <div className="flex gap-4 pb-3 border-b">
                <Skeleton className="h-4 w-32" />
                <Skeleton className="h-4 w-48" />
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-4 w-24" />
            </div>

            {/* Table Rows */}
            {Array.from({ length: rows }).map((_, i) => (
                <div key={i} className="flex gap-4 py-3">
                    <Skeleton className="h-4 w-32" />
                    <Skeleton className="h-4 w-48" />
                    <Skeleton className="h-4 w-24" />
                    <Skeleton className="h-4 w-24" />
                </div>
            ))}
        </div>
    );
}

export function CardListSkeleton({ items = 3 }: { items?: number }) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: items }).map((_, i) => (
                <Card key={i}>
                    <CardHeader>
                        <div className="flex items-center gap-3">
                            <Skeleton className="h-12 w-12 rounded-full" />
                            <div className="flex-1">
                                <Skeleton className="h-5 w-32 mb-2" />
                                <Skeleton className="h-3 w-24" />
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            <Skeleton className="h-4 w-full" />
                            <Skeleton className="h-4 w-3/4" />
                        </div>
                    </CardContent>
                </Card>
            ))}
        </div>
    );
}

export function FormSkeleton() {
    return (
        <div className="space-y-6">
            {[1, 2, 3, 4].map((i) => (
                <div key={i} className="space-y-2">
                    <Skeleton className="h-4 w-32" />
                    <Skeleton className="h-10 w-full" />
                </div>
            ))}
            <div className="flex gap-3 pt-4">
                <Skeleton className="h-10 w-24" />
                <Skeleton className="h-10 w-24" />
            </div>
        </div>
    );
}

/**
 * useLoadingState Hook
 * 
 * Hook for managing loading states
 * 
 * Usage:
 * const { isLoading, startLoading, stopLoading } = useLoadingState();
 */
export function useLoadingState(initialState = false) {
    const [isLoading, setIsLoading] = React.useState(initialState);

    const startLoading = React.useCallback(() => setIsLoading(true), []);
    const stopLoading = React.useCallback(() => setIsLoading(false), []);

    return { isLoading, startLoading, stopLoading, setIsLoading };
}
