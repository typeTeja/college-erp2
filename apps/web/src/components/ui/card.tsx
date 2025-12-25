import React from 'react';

export const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => {
    return (
        <div className={`bg-white shadow rounded-lg overflow-hidden ${className}`}>
            {children}
        </div>
    );
};

export const CardHeader = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
    <div className={`px-4 py-5 sm:px-6 border-b border-gray-200 ${className}`}>
        {children}
    </div>
);

export const CardContent = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
    <div className={`px-4 py-5 sm:p-6 ${className}`}>
        {children}
    </div>
);

export const CardTitle = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
    <h3 className={`text-lg leading-6 font-medium text-gray-900 ${className}`}>
        {children}
    </h3>
);

export const CardDescription = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
    <p className={`mt-1 max-w-2xl text-sm text-gray-500 ${className}`}>
        {children}
    </p>
);
