'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ODCBilling, BillingStatus } from '@/types/odc';

interface ODCBillingListProps {
    billings: ODCBilling[];
    isLoading: boolean;
}

export function ODCBillingList({ billings, isLoading }: ODCBillingListProps) {
    if (isLoading) {
        return <div className="text-center py-10">Loading...</div>;
    }

    if (billings.length === 0) {
        return (
            <p className="text-gray-500 text-center py-8">No billings found</p>
        );
    }

    const getStatusBadge = (status: BillingStatus) => {
        const variants: Record<BillingStatus, string> = {
            DRAFT: 'bg-gray-500',
            SENT: 'bg-blue-500',
            PAID: 'bg-green-500',
            CANCELLED: 'bg-red-500'
        };
        return <Badge className={variants[status]}>{status}</Badge>;
    };

    const formatCurrency = (amount: number) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-IN');
    };

    return (
        <div className="overflow-x-auto">
            <table className="w-full">
                <thead className="bg-gray-50">
                    <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Event</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Hotel</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Students</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice Date</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                    {billings.map((billing) => (
                        <tr key={billing.id} className="hover:bg-gray-50">
                            <td className="px-4 py-3 text-sm font-medium text-gray-900">
                                {billing.invoice_number}
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-900">
                                {billing.event_name || `Request #${billing.request_id}`}
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-900">
                                {billing.hotel_name || '-'}
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-900">
                                {billing.total_students}
                            </td>
                            <td className="px-4 py-3 text-sm font-semibold text-gray-900">
                                {formatCurrency(billing.total_amount)}
                            </td>
                            <td className="px-4 py-3 text-sm">
                                {getStatusBadge(billing.status)}
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-900">
                                {formatDate(billing.invoice_date)}
                            </td>
                            <td className="px-4 py-3 text-sm">
                                {billing.status !== BillingStatus.PAID && (
                                    <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={() => {
                                            // TODO: Implement mark as paid dialog
                                            alert('Mark as paid functionality - to be implemented');
                                        }}
                                    >
                                        Mark Paid
                                    </Button>
                                )}
                                {billing.status === BillingStatus.PAID && billing.paid_date && (
                                    <span className="text-xs text-gray-500">
                                        Paid: {formatDate(billing.paid_date)}
                                    </span>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
