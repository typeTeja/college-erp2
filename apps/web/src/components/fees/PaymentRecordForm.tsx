'use client';

import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { feeService } from '@/utils/fee-service';
import type { FeePaymentCreate, PaymentMode } from '@/types/fee';
import { CreditCard, Save } from 'lucide-react';

interface PaymentRecordFormProps {
    studentFeeId: number;
    studentName: string;
    balanceAmount: number;
    onSuccess?: () => void;
}

export function PaymentRecordForm({
    studentFeeId,
    studentName,
    balanceAmount,
    onSuccess
}: PaymentRecordFormProps) {
    const queryClient = useQueryClient();
    const [formData, setFormData] = useState<FeePaymentCreate>({
        student_fee_id: studentFeeId,
        amount: 0,
        payment_mode: 'CASH' as PaymentMode,
        reference_number: '',
        bank_name: '',
        remarks: '',
    });

    const recordMutation = useMutation({
        mutationFn: (data: FeePaymentCreate) => feeService.payments.recordPayment(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['student-fee'] });
            alert('Payment recorded successfully!');
            onSuccess?.();
            // Reset form
            setFormData({
                student_fee_id: studentFeeId,
                amount: 0,
                payment_mode: 'CASH' as PaymentMode,
                reference_number: '',
                bank_name: '',
                remarks: '',
            });
        },
        onError: (error) => {
            console.error('Failed to record payment:', error);
            alert('Failed to record payment. Please try again.');
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (formData.amount <= 0) {
            alert('Please enter a valid amount');
            return;
        }

        if (formData.amount > balanceAmount) {
            alert('Payment amount cannot exceed balance due');
            return;
        }

        recordMutation.mutate(formData);
    };

    return (
        <Card>
            <CardContent className="p-6">
                <div className="flex items-center space-x-2 mb-4">
                    <CreditCard className="w-5 h-5 text-blue-600" />
                    <h3 className="text-lg font-bold text-gray-800">Record Payment</h3>
                </div>

                <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm text-gray-700">
                        <span className="font-semibold">Student:</span> {studentName}
                    </p>
                    <p className="text-sm text-gray-700">
                        <span className="font-semibold">Balance Due:</span> ₹{balanceAmount.toLocaleString()}
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4" method="POST">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Amount *
                        </label>
                        <Input
                            type="number"
                            value={formData.amount || ''}
                            onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) || 0 })}
                            placeholder="Enter payment amount"
                            required
                            min={0}
                            max={balanceAmount}
                            step={0.01}
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Payment Mode *
                        </label>
                        <select
                            value={formData.payment_mode}
                            onChange={(e) => setFormData({ ...formData, payment_mode: e.target.value as PaymentMode })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            required
                        >
                            <option value="CASH">Cash</option>
                            <option value="UPI">UPI</option>
                            <option value="CHEQUE">Cheque</option>
                            <option value="DD">Demand Draft</option>
                            <option value="ONLINE">Online Transfer</option>
                        </select>
                    </div>

                    {(formData.payment_mode === 'CHEQUE' || formData.payment_mode === 'DD' || formData.payment_mode === 'ONLINE') && (
                        <>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Reference Number
                                </label>
                                <Input
                                    type="text"
                                    value={formData.reference_number || ''}
                                    onChange={(e) => setFormData({ ...formData, reference_number: e.target.value })}
                                    placeholder="Cheque/DD/Transaction number"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Bank Name
                                </label>
                                <Input
                                    type="text"
                                    value={formData.bank_name || ''}
                                    onChange={(e) => setFormData({ ...formData, bank_name: e.target.value })}
                                    placeholder="Enter bank name"
                                />
                            </div>
                        </>
                    )}

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Remarks
                        </label>
                        <textarea
                            value={formData.remarks || ''}
                            onChange={(e) => setFormData({ ...formData, remarks: e.target.value })}
                            placeholder="Additional notes (optional)"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            rows={3}
                        />
                    </div>

                    <div className="flex justify-end space-x-3">
                        <Button
                            type="button"
                            variant="outline"
                            onClick={() => onSuccess?.()}
                        >
                            Cancel
                        </Button>
                        <Button
                            type="submit"
                            disabled={recordMutation.isPending}
                            className="bg-green-600 hover:bg-green-700 text-white"
                        >
                            <Save className="w-4 h-4 mr-2" />
                            {recordMutation.isPending ? 'Recording...' : 'Record Payment'}
                        </Button>
                    </div>
                </form>
            </CardContent>
        </Card>
    );
}
