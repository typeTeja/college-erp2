'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ODCPayoutList } from '@/components/odc/ODCPayoutList';
import { odcService } from '@/utils/odc-service';
import { ODCApplication, PaymentMethod } from '@/types/odc';

export default function PayoutManagementPage() {
    const [pendingPayouts, setPendingPayouts] = useState<ODCApplication[]>([]);
    const [selectedApplications, setSelectedApplications] = useState<number[]>([]);
    const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>(PaymentMethod.BANK_TRANSFER);
    const [loading, setLoading] = useState(true);
    const [processing, setProcessing] = useState(false);

    useEffect(() => {
        fetchPendingPayouts();
    }, []);

    const fetchPendingPayouts = async () => {
        try {
            const data = await odcService.getPendingPayouts();
            setPendingPayouts(data);
        } catch (error) {
            console.error('Error fetching pending payouts:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSelectAll = (checked: boolean) => {
        if (checked) {
            setSelectedApplications(pendingPayouts.map(app => app.id));
        } else {
            setSelectedApplications([]);
        }
    };

    const handleSelectApplication = (appId: number, checked: boolean) => {
        if (checked) {
            setSelectedApplications([...selectedApplications, appId]);
        } else {
            setSelectedApplications(selectedApplications.filter(id => id !== appId));
        }
    };

    const handleProcessPayouts = async () => {
        if (selectedApplications.length === 0) {
            alert('Please select at least one application');
            return;
        }

        if (!confirm(`Process ${selectedApplications.length} payout(s)?`)) {
            return;
        }

        setProcessing(true);
        try {
            await odcService.processPayouts({
                application_ids: selectedApplications,
                payment_method: paymentMethod,
                payout_date: new Date().toISOString().split('T')[0],
                notes: `Batch payout processed on ${new Date().toLocaleDateString()}`
            });

            alert('Payouts processed successfully!');
            setSelectedApplications([]);
            fetchPendingPayouts();
        } catch (error: any) {
            console.error('Error processing payouts:', error);
            // safe optional chaining for error msg
            const msg = error?.response?.data?.detail || 'Failed to process payouts';
            alert(msg);
        } finally {
            setProcessing(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">ODC Payout Management</h1>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium">Pending Payouts</h3>
                        {selectedApplications.length > 0 && (
                            <div className="flex items-center gap-4">
                                <select
                                    value={paymentMethod}
                                    onChange={(e) => setPaymentMethod(e.target.value as PaymentMethod)}
                                    className="border rounded px-3 py-2"
                                >
                                    <option value={PaymentMethod.BANK_TRANSFER}>Bank Transfer</option>
                                    <option value={PaymentMethod.UPI}>UPI</option>
                                    <option value={PaymentMethod.CASH}>Cash</option>
                                    <option value={PaymentMethod.CHEQUE}>Cheque</option>
                                </select>
                                <Button
                                    onClick={handleProcessPayouts}
                                    disabled={processing}
                                >
                                    {processing ? 'Processing...' : `Process ${selectedApplications.length} Payout(s)`}
                                </Button>
                            </div>
                        )}
                    </div>
                </CardHeader>
                <CardContent>
                    <ODCPayoutList
                        applications={pendingPayouts}
                        selectedIds={selectedApplications}
                        onSelectAll={handleSelectAll}
                        onSelectOne={handleSelectApplication}
                        isLoading={loading}
                    />
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <h3 className="text-lg font-medium">Payout Summary</h3>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-yellow-50 p-4 rounded-lg">
                            <p className="text-sm text-gray-500">Pending Payouts</p>
                            <p className="text-2xl font-bold text-yellow-900">{pendingPayouts.length}</p>
                        </div>
                        <div className="bg-blue-50 p-4 rounded-lg">
                            <p className="text-sm text-gray-500">Selected</p>
                            <p className="text-2xl font-bold text-blue-900">{selectedApplications.length}</p>
                        </div>
                        <div className="bg-purple-50 p-4 rounded-lg">
                            <p className="text-sm text-gray-500">Payment Method</p>
                            <p className="text-lg font-bold text-purple-900">
                                {paymentMethod.replace('_', ' ')}
                            </p>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
