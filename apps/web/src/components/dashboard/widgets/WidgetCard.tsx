import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface WidgetCardProps {
  title: string;
  description?: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
  className?: string;
}

/**
 * WidgetCard - Reusable card component for dashboard widgets
 * 
 * Provides consistent styling and structure for dashboard widgets:
 * - Title and optional description
 * - Optional action buttons in header
 * - Content area
 * 
 * Usage:
 * <WidgetCard 
 *   title="Enrollment Trends" 
 *   description="Last 5 years"
 *   actions={<Button>View Details</Button>}
 * >
 *   <Chart data={data} />
 * </WidgetCard>
 */
export function WidgetCard({ 
  title, 
  description, 
  children, 
  actions,
  className = ''
}: WidgetCardProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-lg font-semibold">{title}</CardTitle>
            {description && (
              <p className="text-sm text-slate-500 mt-1">{description}</p>
            )}
          </div>
          {actions && (
            <div className="ml-4">
              {actions}
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent>
        {children}
      </CardContent>
    </Card>
  );
}
