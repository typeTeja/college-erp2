'use client';

import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface KPICardProps {
    title: string;
    value: string | number;
    icon: React.ReactNode;
    trend?: {
        value: string;
        isPositive: boolean;
    };
    color?: 'blue' | 'green' | 'orange' | 'purple' | 'red' | 'indigo';
}

export function KPICard({ title, value, icon, trend, color = 'blue' }: KPICardProps) {
    const colorClasses = {
        blue: 'from-blue-500 to-blue-600',
        green: 'from-green-500 to-green-600',
        orange: 'from-orange-500 to-orange-600',
        purple: 'from-purple-500 to-purple-600',
        red: 'from-red-500 to-red-600',
        indigo: 'from-indigo-500 to-indigo-600',
    }[color];

    return (
        <div className="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between">
                <div className="flex-1">
                    <p className="text-slate-600 text-sm mb-2">{title}</p>
                    <p className="text-slate-900 text-3xl font-semibold mb-3">{value}</p>
                    {trend && (
                        <div className={`flex items-center gap-1 text-sm ${trend.isPositive ? 'text-green-600' : 'text-red-600'}`}>
                            {trend.isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                            <span>{trend.value}</span>
                        </div>
                    )}
                </div>
                <div className={`w-12 h-12 bg-gradient-to-br ${colorClasses} rounded-lg flex items-center justify-center text-white`}>
                    {icon}
                </div>
            </div>
        </div>
    );
}
