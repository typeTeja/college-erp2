'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Check, X, Pencil, Loader2 } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

interface InlineEditableFieldProps {
    value: string | number;
    onSave: (newValue: string | number) => Promise<void>;
    type?: 'text' | 'number';
    min?: number;
    max?: number;
    placeholder?: string;
    className?: string;
    disabled?: boolean;
}

export function InlineEditableField({
    value,
    onSave,
    type = 'text',
    min,
    max,
    placeholder,
    className = '',
    disabled = false
}: InlineEditableFieldProps) {
    const [isEditing, setIsEditing] = useState(false);
    const [editValue, setEditValue] = useState(value);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        setEditValue(value);
    }, [value]);

    useEffect(() => {
        if (isEditing && inputRef.current) {
            inputRef.current.focus();
            inputRef.current.select();
        }
    }, [isEditing]);

    const handleSave = async () => {
        // Validate
        if (type === 'number') {
            const numValue = Number(editValue);
            if (isNaN(numValue)) {
                setError('Please enter a valid number');
                return;
            }
            if (min !== undefined && numValue < min) {
                setError(`Value must be at least ${min}`);
                return;
            }
            if (max !== undefined && numValue > max) {
                setError(`Value must be at most ${max}`);
                return;
            }
        }

        // No change
        if (editValue === value) {
            setIsEditing(false);
            setError(null);
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            await onSave(type === 'number' ? Number(editValue) : editValue);
            setIsEditing(false);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to save');
            // Revert to original value
            setEditValue(value);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCancel = () => {
        setEditValue(value);
        setIsEditing(false);
        setError(null);
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            handleSave();
        } else if (e.key === 'Escape') {
            handleCancel();
        }
    };

    if (!isEditing) {
        return (
            <button
                onClick={() => !disabled && setIsEditing(true)}
                disabled={disabled}
                className={`inline-flex items-center gap-1 px-2 py-1 rounded hover:bg-slate-100 transition-colors group ${className} ${disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'
                    }`}
                title="Click to edit"
            >
                <span className="font-medium">{value}</span>
                {!disabled && (
                    <Pencil className="h-3 w-3 text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                )}
            </button>
        );
    }

    return (
        <div className="inline-flex flex-col gap-1">
            <div className="inline-flex items-center gap-1">
                <Input
                    type={type}
                    value={editValue}
                    onChange={(e) => setEditValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    min={min}
                    max={max}
                    placeholder={placeholder}
                    disabled={isLoading}
                    autoFocus
                    className={`h-8 w-24 ${error ? 'border-red-500' : ''}`}
                />
                <Button
                    size="sm"
                    variant="ghost"
                    onClick={handleSave}
                    disabled={isLoading}
                    className="h-8 w-8 p-0 text-green-600 hover:text-green-700 hover:bg-green-50"
                >
                    {isLoading ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                        <Check className="h-4 w-4" />
                    )}
                </Button>
                <Button
                    size="sm"
                    variant="ghost"
                    onClick={handleCancel}
                    disabled={isLoading}
                    className="h-8 w-8 p-0 text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                    <X className="h-4 w-4" />
                </Button>
            </div>
            {error && (
                <span className="text-xs text-red-600">{error}</span>
            )}
        </div>
    );
}
