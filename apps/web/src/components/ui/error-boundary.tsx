"use client"

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AlertCircle, RefreshCw, Home } from 'lucide-react';

/**
 * ErrorBoundary Component
 * 
 * React Error Boundary for graceful error handling
 * Following UX laws:
 * - Clear error messaging (Miller's Law)
 * - Easy recovery actions (Fitts's Law)
 * - Minimal choices (Hick's Law)
 * 
 * Usage:
 * <ErrorBoundary fallback={<CustomError />}>
 *   <YourComponent />
 * </ErrorBoundary>
 */

interface ErrorBoundaryProps {
    children: ReactNode;
    fallback?: ReactNode;
    onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
    hasError: boolean;
    error: Error | null;
    errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
    constructor(props: ErrorBoundaryProps) {
        super(props);
        this.state = {
            hasError: false,
            error: null,
            errorInfo: null,
        };
    }

    static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        // Log error to error reporting service
        console.error('ErrorBoundary caught an error:', error, errorInfo);
        
        this.setState({
            error,
            errorInfo,
        });

        // Call optional error handler
        this.props.onError?.(error, errorInfo);
    }

    handleReset = () => {
        this.setState({
            hasError: false,
            error: null,
            errorInfo: null,
        });
    };

    handleGoHome = () => {
        window.location.href = '/';
    };

    render() {
        if (this.state.hasError) {
            // Use custom fallback if provided
            if (this.props.fallback) {
                return this.props.fallback;
            }

            // Default error UI
            return (
                <div className="min-h-screen flex items-center justify-center p-6 bg-slate-50">
                    <Card className="max-w-lg w-full">
                        <CardContent className="pt-6">
                            <div className="text-center">
                                <div className="flex justify-center mb-4">
                                    <div className="p-3 bg-red-100 rounded-full">
                                        <AlertCircle className="h-8 w-8 text-red-600" />
                                    </div>
                                </div>
                                
                                <h2 className="text-xl font-semibold text-slate-900 mb-2">
                                    Something went wrong
                                </h2>
                                
                                <p className="text-sm text-slate-600 mb-6">
                                    We encountered an unexpected error. Please try refreshing the page or return to the home page.
                                </p>

                                {/* Show error details in development */}
                                {process.env.NODE_ENV === 'development' && this.state.error && (
                                    <div className="mb-6 p-4 bg-slate-100 rounded-lg text-left">
                                        <p className="text-xs font-mono text-red-600 mb-2">
                                            {this.state.error.toString()}
                                        </p>
                                        {this.state.errorInfo && (
                                            <details className="text-xs font-mono text-slate-600">
                                                <summary className="cursor-pointer mb-2">Stack trace</summary>
                                                <pre className="whitespace-pre-wrap overflow-auto max-h-40">
                                                    {this.state.errorInfo.componentStack}
                                                </pre>
                                            </details>
                                        )}
                                    </div>
                                )}

                                {/* Fitts's Law: Large, easy-to-click action buttons */}
                                <div className="flex gap-3 justify-center">
                                    <Button
                                        variant="outline"
                                        onClick={this.handleGoHome}
                                        className="min-w-[120px]"
                                    >
                                        <Home className="h-4 w-4 mr-2" />
                                        Go Home
                                    </Button>
                                    <Button
                                        onClick={this.handleReset}
                                        className="min-w-[120px] bg-blue-600 hover:bg-blue-700"
                                    >
                                        <RefreshCw className="h-4 w-4 mr-2" />
                                        Try Again
                                    </Button>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            );
        }

        return this.props.children;
    }
}

/**
 * ErrorFallback Component
 * 
 * Reusable error fallback UI for smaller components
 */
interface ErrorFallbackProps {
    error?: Error;
    resetError?: () => void;
    title?: string;
    description?: string;
}

export function ErrorFallback({
    error,
    resetError,
    title = 'Error loading content',
    description = 'Something went wrong. Please try again.',
}: ErrorFallbackProps) {
    return (
        <div className="text-center py-8">
            <div className="flex justify-center mb-4">
                <div className="p-3 bg-red-100 rounded-full">
                    <AlertCircle className="h-6 w-6 text-red-600" />
                </div>
            </div>
            
            <h3 className="text-lg font-semibold text-slate-900 mb-2">
                {title}
            </h3>
            
            <p className="text-sm text-slate-600 mb-4">
                {description}
            </p>

            {process.env.NODE_ENV === 'development' && error && (
                <p className="text-xs font-mono text-red-600 mb-4 max-w-md mx-auto">
                    {error.toString()}
                </p>
            )}

            {resetError && (
                <Button
                    onClick={resetError}
                    variant="outline"
                    size="sm"
                >
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Try Again
                </Button>
            )}
        </div>
    );
}

/**
 * useErrorHandler Hook
 * 
 * Hook for handling errors in functional components
 * 
 * Usage:
 * const handleError = useErrorHandler();
 * 
 * try {
 *   // risky operation
 * } catch (error) {
 *   handleError(error);
 * }
 */
export function useErrorHandler() {
    const [, setError] = React.useState<Error | null>(null);

    return React.useCallback((error: Error) => {
        setError(() => {
            throw error;
        });
    }, []);
}
