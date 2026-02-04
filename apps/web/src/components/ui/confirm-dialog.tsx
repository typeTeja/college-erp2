"use client"

import React from 'react';
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { AlertCircle, Trash2, CheckCircle, Info } from 'lucide-react';

/**
 * ConfirmDialog Component
 * 
 * Reusable confirmation dialog following UX laws:
 * - Fitts's Law: Large, easy-to-click action buttons
 * - Hick's Law: Limited choices (2-3 max)
 * - Miller's Law: Clear, concise messaging
 * 
 * Usage:
 * <ConfirmDialog
 *   open={isOpen}
 *   onOpenChange={setIsOpen}
 *   title="Delete Student?"
 *   description="This action cannot be undone."
 *   variant="danger"
 *   onConfirm={handleDelete}
 * />
 */

interface ConfirmDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    title: string;
    description: string;
    variant?: 'danger' | 'warning' | 'info' | 'success';
    confirmText?: string;
    cancelText?: string;
    onConfirm: () => void | Promise<void>;
    onCancel?: () => void;
    loading?: boolean;
}

export function ConfirmDialog({
    open,
    onOpenChange,
    title,
    description,
    variant = 'danger',
    confirmText = 'Confirm',
    cancelText = 'Cancel',
    onConfirm,
    onCancel,
    loading = false,
}: ConfirmDialogProps) {
    const handleConfirm = async () => {
        await onConfirm();
        onOpenChange(false);
    };

    const handleCancel = () => {
        onCancel?.();
        onOpenChange(false);
    };

    const variantConfig = {
        danger: {
            icon: <Trash2 className="h-6 w-6 text-red-600" />,
            iconBg: 'bg-red-100',
            confirmClass: 'bg-red-600 hover:bg-red-700 text-white',
        },
        warning: {
            icon: <AlertCircle className="h-6 w-6 text-yellow-600" />,
            iconBg: 'bg-yellow-100',
            confirmClass: 'bg-yellow-600 hover:bg-yellow-700 text-white',
        },
        info: {
            icon: <Info className="h-6 w-6 text-blue-600" />,
            iconBg: 'bg-blue-100',
            confirmClass: 'bg-blue-600 hover:bg-blue-700 text-white',
        },
        success: {
            icon: <CheckCircle className="h-6 w-6 text-green-600" />,
            iconBg: 'bg-green-100',
            confirmClass: 'bg-green-600 hover:bg-green-700 text-white',
        },
    };

    const config = variantConfig[variant];

    return (
        <AlertDialog open={open} onOpenChange={onOpenChange}>
            <AlertDialogContent className="max-w-md">
                <AlertDialogHeader>
                    <div className="flex items-start gap-4">
                        <div className={`p-3 rounded-full ${config.iconBg}`}>
                            {config.icon}
                        </div>
                        <div className="flex-1">
                            <AlertDialogTitle className="text-lg font-semibold text-slate-900">
                                {title}
                            </AlertDialogTitle>
                            <AlertDialogDescription className="mt-2 text-sm text-slate-600">
                                {description}
                            </AlertDialogDescription>
                        </div>
                    </div>
                </AlertDialogHeader>
                <AlertDialogFooter className="mt-6">
                    {/* Fitts's Law: Large, easy-to-click buttons with adequate spacing */}
                    <AlertDialogCancel
                        onClick={handleCancel}
                        disabled={loading}
                        className="min-w-[100px] h-10"
                    >
                        {cancelText}
                    </AlertDialogCancel>
                    <AlertDialogAction
                        onClick={handleConfirm}
                        disabled={loading}
                        className={`min-w-[100px] h-10 ${config.confirmClass}`}
                    >
                        {loading ? 'Processing...' : confirmText}
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    );
}

/**
 * useConfirmDialog Hook
 * 
 * Convenient hook for managing confirm dialog state
 * 
 * Usage:
 * const { confirm, ConfirmDialogComponent } = useConfirmDialog();
 * 
 * const handleDelete = async () => {
 *   const confirmed = await confirm({
 *     title: 'Delete Student?',
 *     description: 'This action cannot be undone.',
 *     variant: 'danger',
 *   });
 *   if (confirmed) {
 *     // Perform delete
 *   }
 * };
 */
export function useConfirmDialog() {
    const [isOpen, setIsOpen] = React.useState(false);
    const [config, setConfig] = React.useState<Omit<ConfirmDialogProps, 'open' | 'onOpenChange' | 'onConfirm'> & { onConfirm?: () => void }>({
        title: '',
        description: '',
    });
    const resolveRef = React.useRef<((value: boolean) => void) | null>(null);

    const confirm = React.useCallback((dialogConfig: Omit<ConfirmDialogProps, 'open' | 'onOpenChange' | 'onConfirm'>) => {
        setConfig(dialogConfig);
        setIsOpen(true);
        return new Promise<boolean>((resolve) => {
            resolveRef.current = resolve;
        });
    }, []);

    const handleConfirm = React.useCallback(async () => {
        await config.onConfirm?.();
        resolveRef.current?.(true);
        setIsOpen(false);
    }, [config]);

    const handleCancel = React.useCallback(() => {
        config.onCancel?.();
        resolveRef.current?.(false);
        setIsOpen(false);
    }, [config]);

    const ConfirmDialogComponent = React.useMemo(
        () => (
            <ConfirmDialog
                open={isOpen}
                onOpenChange={setIsOpen}
                {...config}
                onConfirm={handleConfirm}
                onCancel={handleCancel}
            />
        ),
        [isOpen, config, handleConfirm, handleCancel]
    );

    return { confirm, ConfirmDialogComponent };
}
