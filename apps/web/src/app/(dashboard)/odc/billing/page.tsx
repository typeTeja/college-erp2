'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { ODCBilling, BillingStatus } from '@/types/odc';
import { ODCBillingList } from '@/components/odc/ODCBillingList';
import { odcService } from '@/utils/odc-service';

export default function BillingManagementPage() {
    const [billings, setBillings] = useState<ODCBilling[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchBillings();
    }, []);

    const fetchBillings = async () => {
        try {
            const data = await odcService.getBilling();
            setBillings(data);
        } catch (error) {
            console.error('Error fetching billings:', error);
        } finally {
            setLoading(false);
        }
    };

    const formatCurrency = (amount: number) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">ODC Billing Management</h1>
            </div>

            <Card>
                <CardHeader>
                    <h3 className="text-lg font-medium">All Invoices</h3>
                </CardHeader>
                <CardContent>
                    <ODCBillingList billings={billings} isLoading={loading} />
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <h3 className="text-lg font-medium">Billing Summary</h3>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="bg-gray-50 p-4 rounded-lg">
                            <p className="text-sm text-gray-500">Total Invoices</p>
                            <p className="text-2xl font-bold text-gray-900">{billings.length}</p>
                        </div>
                        <div className="bg-blue-50 p-4 rounded-lg">
                            <p className="text-sm text-gray-500">Pending</p>
                            <p className="text-2xl font-bold text-blue-900">
                                {billings.filter(b => b.status === BillingStatus.DRAFT || b.status === BillingStatus.SENT).length}
                            </p>
                        </div>
                        <div className="bg-green-50 p-4 rounded-lg">
                            <p className="text-sm text-gray-500">Paid</p>
                            <p className="text-2xl font-bold text-green-900">
                                {billings.filter(b => b.status === BillingStatus.PAID).length}
                            </p>
                        </div>
                        <div className="bg-green-50 p-4 rounded-lg">
                            <p className="text-sm text-gray-500">Total Collected</p>
                            <p className="text-2xl font-bold text-green-900">
                                {formatCurrency(
                                    billings
                                        .filter(b => b.status === BillingStatus.PAID)
                                        .reduce((sum, b) => sum + (b.total_amount || 0), 0)
                                ).replace(/^₹/, '₹ ')}
                            </p>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
