"use client"

import React, { useState, useEffect } from 'react';
import { X, Info, CheckCircle, AlertTriangle } from 'lucide-react';
import { Button } from './button';
import { cn } from '@/lib/utils';

export interface AnnouncementBannerProps {
  title: string;
  message: string;
  ctaText?: string;
  ctaLink?: string;
  variant?: 'info' | 'success' | 'warning';
  dismissible?: boolean;
  storageKey?: string;
  className?: string;
}

/**
 * AnnouncementBanner Component
 * 
 * Displays important announcements to users with optional CTA and dismissal.
 * Uses localStorage to persist dismissal state across sessions.
 * 
 * @example
 * ```tsx
 * <AnnouncementBanner
 *   title="New Navigation Available!"
 *   message="We've redesigned the navigation for a better experience."
 *   ctaText="View What's New"
 *   ctaLink="/docs/whats-new"
 *   variant="info"
 *   dismissible
 *   storageKey="announcement-new-nav-2026"
 * />
 * ```
 */
export function AnnouncementBanner({
  title,
  message,
  ctaText,
  ctaLink,
  variant = 'info',
  dismissible = true,
  storageKey = 'announcement-dismissed',
  className,
}: AnnouncementBannerProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Check if banner was previously dismissed
    const dismissed = localStorage.getItem(storageKey);
    if (!dismissed) {
      setIsVisible(true);
    }
  }, [storageKey]);

  const handleDismiss = () => {
    setIsVisible(false);
    localStorage.setItem(storageKey, 'true');
  };

  if (!isVisible) return null;

  const variants = {
    info: {
      bg: 'bg-blue-50 dark:bg-blue-950',
      border: 'border-blue-200 dark:border-blue-800',
      text: 'text-blue-900 dark:text-blue-100',
      icon: Info,
      iconColor: 'text-blue-600 dark:text-blue-400',
    },
    success: {
      bg: 'bg-green-50 dark:bg-green-950',
      border: 'border-green-200 dark:border-green-800',
      text: 'text-green-900 dark:text-green-100',
      icon: CheckCircle,
      iconColor: 'text-green-600 dark:text-green-400',
    },
    warning: {
      bg: 'bg-yellow-50 dark:bg-yellow-950',
      border: 'border-yellow-200 dark:border-yellow-800',
      text: 'text-yellow-900 dark:text-yellow-100',
      icon: AlertTriangle,
      iconColor: 'text-yellow-600 dark:text-yellow-400',
    },
  };

  const config = variants[variant];
  const Icon = config.icon;

  return (
    <div
      className={cn(
        'relative border-b',
        config.bg,
        config.border,
        className
      )}
      role="alert"
      aria-live="polite"
    >
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between gap-4">
          {/* Icon + Content */}
          <div className="flex items-start gap-3 flex-1">
            <Icon className={cn('h-5 w-5 mt-0.5 flex-shrink-0', config.iconColor)} />
            
            <div className="flex-1 min-w-0">
              <h3 className={cn('font-semibold text-sm', config.text)}>
                {title}
              </h3>
              <p className={cn('text-sm mt-1', config.text)}>
                {message}
              </p>
            </div>
          </div>

          {/* CTA + Dismiss */}
          <div className="flex items-center gap-2 flex-shrink-0">
            {ctaText && ctaLink && (
              <Button
                variant="outline"
                size="sm"
                asChild
                className={cn(
                  'whitespace-nowrap',
                  variant === 'info' && 'border-blue-300 hover:bg-blue-100 dark:border-blue-700 dark:hover:bg-blue-900',
                  variant === 'success' && 'border-green-300 hover:bg-green-100 dark:border-green-700 dark:hover:bg-green-900',
                  variant === 'warning' && 'border-yellow-300 hover:bg-yellow-100 dark:border-yellow-700 dark:hover:bg-yellow-900'
                )}
              >
                <a href={ctaLink}>{ctaText}</a>
              </Button>
            )}

            {dismissible && (
              <button
                onClick={handleDismiss}
                className={cn(
                  'p-1 rounded-md hover:bg-black/5 dark:hover:bg-white/5 transition-colors',
                  config.text
                )}
                aria-label="Dismiss announcement"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * useAnnouncementBanner Hook
 * 
 * Utility hook to programmatically show/hide announcements
 */
export function useAnnouncementBanner(storageKey: string) {
  const [isDismissed, setIsDismissed] = useState(false);

  useEffect(() => {
    const dismissed = localStorage.getItem(storageKey);
    setIsDismissed(!!dismissed);
  }, [storageKey]);

  const dismiss = () => {
    localStorage.setItem(storageKey, 'true');
    setIsDismissed(true);
  };

  const reset = () => {
    localStorage.removeItem(storageKey);
    setIsDismissed(false);
  };

  return { isDismissed, dismiss, reset };
}
