import React from 'react';
import { ChevronRight, Info } from 'lucide-react';
import { getBadgeLabel, getBadgeClasses, type NavigationBadge } from '@/config/navigation-v2';

interface ConfigPageTemplateProps {
  title: string;
  description: string;
  badge?: NavigationBadge;
  movedFrom?: string; // Old location (e.g., "Settings > Programs")
  children: React.ReactNode;
  actions?: React.ReactNode;
}

/**
 * ConfigPageTemplate - Consistent layout for all configuration pages
 * 
 * Provides:
 * - Page header with title, description, and badge
 * - Breadcrumbs
 * - "Moved from" notification (dismissible, 30-day expiration)
 * - Action buttons area
 * - Content area
 * 
 * Usage:
 * <ConfigPageTemplate
 *   title="Programs"
 *   description="Manage degree programs"
 *   badge="setup"
 *   movedFrom="Settings > Programs"
 *   actions={<Button>Add Program</Button>}
 * >
 *   {children}
 * </ConfigPageTemplate>
 */
export function ConfigPageTemplate({
  title,
  description,
  badge,
  movedFrom,
  children,
  actions
}: ConfigPageTemplateProps) {
  return (
    <div className="space-y-6">
      {/* Moved From Badge */}
      {movedFrom && <MovedFromBadge oldLocation={movedFrom} />}

      {/* Page Header */}
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-semibold text-slate-900">{title}</h1>
            {badge && (
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium uppercase tracking-wider ${getBadgeClasses(badge)}`}>
                {getBadgeLabel(badge)}
              </span>
            )}
          </div>
          <p className="text-slate-600 mt-1">{description}</p>
        </div>

        {/* Action Buttons */}
        {actions && (
          <div className="ml-4">
            {actions}
          </div>
        )}
      </div>

      {/* Page Content */}
      <div>
        {children}
      </div>
    </div>
  );
}

/**
 * MovedFromBadge - Shows notification that page has moved
 * 
 * Features:
 * - Dismissible (stored in localStorage)
 * - 30-day auto-expiration
 * - Shows old location
 * 
 * Usage:
 * <MovedFromBadge oldLocation="Settings > Programs" />
 */
interface MovedFromBadgeProps {
  oldLocation: string;
}

function MovedFromBadge({ oldLocation }: MovedFromBadgeProps) {
  const [dismissed, setDismissed] = React.useState(false);

  // Check if badge was dismissed
  React.useEffect(() => {
    const key = `moved-from-dismissed-${oldLocation}`;
    const dismissedData = localStorage.getItem(key);
    
    if (dismissedData) {
      const { timestamp } = JSON.parse(dismissedData);
      const daysSinceDismissal = (Date.now() - timestamp) / (1000 * 60 * 60 * 24);
      
      // Auto-expire after 30 days
      if (daysSinceDismissal < 30) {
        setDismissed(true);
      } else {
        localStorage.removeItem(key);
      }
    }
  }, [oldLocation]);

  const handleDismiss = () => {
    const key = `moved-from-dismissed-${oldLocation}`;
    localStorage.setItem(key, JSON.stringify({ timestamp: Date.now() }));
    setDismissed(true);
  };

  if (dismissed) return null;

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <div className="flex items-start gap-3">
        <Info className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <p className="text-sm text-blue-900">
            <strong>This page has moved.</strong> Previously located at: <span className="font-mono text-xs">{oldLocation}</span>
          </p>
          <p className="text-xs text-blue-700 mt-1">
            This notification will automatically disappear in 30 days.
          </p>
        </div>
        <button
          onClick={handleDismiss}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium flex-shrink-0"
        >
          Dismiss
        </button>
      </div>
    </div>
  );
}

/**
 * Breadcrumbs component for navigation
 */
interface BreadcrumbsProps {
  items: Array<{
    label: string;
    href?: string;
  }>;
}

export function Breadcrumbs({ items }: BreadcrumbsProps) {
  return (
    <nav className="flex items-center space-x-2 text-sm text-slate-600">
      {items.map((item, index) => (
        <React.Fragment key={index}>
          {index > 0 && <ChevronRight className="h-4 w-4" />}
          {item.href ? (
            <a href={item.href} className="hover:text-slate-900">
              {item.label}
            </a>
          ) : (
            <span className="text-slate-900 font-medium">{item.label}</span>
          )}
        </React.Fragment>
      ))}
    </nav>
  );
}
