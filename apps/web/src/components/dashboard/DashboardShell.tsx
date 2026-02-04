import React from 'react';

interface DashboardShellProps {
  title: string;
  subtitle: string;
  role: string;
  children: React.ReactNode;
}

/**
 * DashboardShell - Base layout for all role-specific dashboards
 * 
 * Provides consistent header structure with:
 * - Dashboard title
 * - User greeting/subtitle
 * - Role badge
 * 
 * Usage:
 * <DashboardShell title="Principal Dashboard" subtitle="Welcome back, John" role="Executive">
 *   {children}
 * </DashboardShell>
 */
export function DashboardShell({ title, subtitle, role, children }: DashboardShellProps) {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">{title}</h1>
          <p className="text-slate-600 mt-1">{subtitle}</p>
        </div>
        <div className="hidden md:block">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium uppercase tracking-wider bg-slate-100 text-slate-700">
            {role}
          </span>
        </div>
      </div>

      {/* Dashboard Content */}
      {children}
    </div>
  );
}
