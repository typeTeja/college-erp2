'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { feeService } from '@/utils/fee-service';
import type { StudentFeeSummary } from '@/types/fee';
import { AlertCircle, CheckCircle, Clock, CreditCard, FileText } from 'lucide-react';

interface FeeDashboardProps {
    studentId: number;
    academicYear?: string;
}

export function FeeDashboard({ studentId, academicYear }: FeeDashboardProps) {
    const { data: feeSummary, isLoading, error } = useQuery({
        queryKey: ['student-fee', studentId, academicYear],
        queryFn: () => feeService.studentFees.getSummary(studentId, academicYear),
    });

    const handlePayNow = async () => {
        if (!feeSummary) return;

        try {
            const response = await feeService.payments.initiatePayment({
                student_fee_id: feeSummary.student_id,
                amount: feeSummary.balance,
            });

            // Redirect to payment gateway
            window.location.href = response.payment_url;
        } catch (error) {
            console.error('Payment initiation failed:', error);
            alert('Failed to initiate payment. Please try again.');
        }
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-12">
                <div className="text-center">
                    <Clock className="w-8 h-8 animate-spin mx-auto mb-2 text-blue-500" />
                    <p className="text-gray-600">Loading fee details...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <Card className="border-red-200 bg-red-50">
                <CardContent className="p-6">
                    <div className="flex items-center space-x-2 text-red-600">
                        <AlertCircle className="w-5 h-5" />
                        <p>Failed to load fee details. Please try again later.</p>
                    </div>
                </CardContent>
            </Card>
        );
    }

    if (!feeSummary) {
        return (
            <Card>
                <CardContent className="p-6 text-center text-gray-500">
                    <FileText className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                    <p>No fee record found for this academic year.</p>
                </CardContent>
            </Card>
        );
    }

    const balanceAmount = feeSummary.balance;
    const isPaid = balanceAmount <= 0;

    return (
        <div className="space-y-6">
            {/* Fee Summary Card */}
            <Card className={isPaid ? 'border-green-200 bg-green-50' : 'border-blue-200'}>
                <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-800">Fee Summary</h2>
                            <p className="text-sm text-gray-600">
                                {feeSummary.student_name} ({feeSummary.admission_number})
                            </p>
                            <p className="text-xs text-gray-500">Academic Year: {feeSummary.academic_year}</p>
                        </div>
                        {isPaid ? (
                            <Badge className="bg-green-600 text-white">
                                <CheckCircle className="w-4 h-4 mr-1" />
                                Fully Paid
                            </Badge>
                        ) : (
                            <Badge variant="destructive">
                                <AlertCircle className="w-4 h-4 mr-1" />
                                {feeSummary.is_blocked ? 'Blocked' : 'Pending'}
                            </Badge>
                        )}
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="bg-white p-4 rounded-lg shadow-sm">
                            <p className="text-xs text-gray-500 mb-1">Total Fee</p>
                            <p className="text-xl font-bold text-gray-800">₹{feeSummary.total_fee.toLocaleString()}</p>
                        </div>
                        <div className="bg-white p-4 rounded-lg shadow-sm">
                            <p className="text-xs text-gray-500 mb-1">Concession</p>
                            <p className="text-xl font-bold text-green-600">-₹{feeSummary.concession_amount.toLocaleString()}</p>
                        </div>
                        <div className="bg-white p-4 rounded-lg shadow-sm">
                            <p className="text-xs text-gray-500 mb-1">Fine</p>
                            <p className="text-xl font-bold text-red-600">+₹{feeSummary.fine_amount.toLocaleString()}</p>
                        </div>
                        <div className="bg-white p-4 rounded-lg shadow-sm">
                            <p className="text-xs text-gray-500 mb-1">Paid</p>
                            <p className="text-xl font-bold text-blue-600">₹{feeSummary.paid_amount.toLocaleString()}</p>
                        </div>
                    </div>

                    <div className="mt-4 p-4 bg-white rounded-lg shadow-sm border-2 border-blue-300">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600">Balance Due</p>
                                <p className="text-3xl font-bold text-blue-600">₹{balanceAmount.toLocaleString()}</p>
                            </div>
                            {!isPaid && (
                                <Button
                                    onClick={handlePayNow}
                                    className="bg-blue-600 hover:bg-blue-700 text-white"
                                    size="lg"
                                >
                                    <CreditCard className="w-4 h-4 mr-2" />
                                    Pay Now
                                </Button>
                            )}
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Installments Card */}
            <Card>
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold mb-4 text-gray-800">Installment Schedule</h3>
                    <div className="space-y-3">
                        {feeSummary.installments.map((installment) => (
                            <div
                                key={installment.installment_number}
                                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                            >
                                <div className="flex items-center space-x-3">
                                    <div className={`w-10 h-10 rounded-full flex items-center justify-center ${installment.status === 'paid'
                                        ? 'bg-green-100 text-green-600'
                                        : installment.status === 'overdue'
                                            ? 'bg-red-100 text-red-600'
                                            : 'bg-gray-200 text-gray-600'
                                        }`}>
                                        {installment.installment_number}
                                    </div>
                                    <div>
                                        <p className="font-semibold text-gray-800">Installment {installment.installment_number}</p>
                                        <p className="text-sm text-gray-500">Due: {new Date(installment.due_date).toLocaleDateString()}</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <p className="font-bold text-gray-800">₹{installment.amount.toLocaleString()}</p>
                                    <Badge
                                        variant={installment.status === 'paid' ? 'default' : 'outline'}
                                        className={
                                            installment.status === 'paid'
                                                ? 'bg-green-100 text-green-700 border-green-300'
                                                : installment.status === 'overdue'
                                                    ? 'bg-red-100 text-red-700 border-red-300'
                                                    : 'bg-yellow-100 text-yellow-700 border-yellow-300'
                                        }
                                    >
                                        {installment.status.toUpperCase()}
                                    </Badge>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Payment History Card */}
            <Card>
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold mb-4 text-gray-800">Payment History</h3>
                    {feeSummary.payments.length === 0 ? (
                        <p className="text-center text-gray-500 py-4">No payments recorded yet.</p>
                    ) : (
                        <div className="space-y-3">
                            {feeSummary.payments.map((payment) => (
                                <div
                                    key={payment.id}
                                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                                >
                                    <div>
                                        <p className="font-semibold text-gray-800">₹{payment.amount.toLocaleString()}</p>
                                        <p className="text-sm text-gray-500">
                                            {payment.payment_date
                                                ? new Date(payment.payment_date).toLocaleDateString()
                                                : 'Pending'}
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <Badge
                                            variant={payment.status === 'SUCCESS' ? 'default' : 'outline'}
                                            className={
                                                payment.status === 'SUCCESS'
                                                    ? 'bg-green-100 text-green-700 border-green-300'
                                                    : payment.status === 'FAILED'
                                                        ? 'bg-red-100 text-red-700 border-red-300'
                                                        : 'bg-yellow-100 text-yellow-700 border-yellow-300'
                                            }
                                        >
                                            {payment.status}
                                        </Badge>
                                        <p className="text-xs text-gray-500 mt-1">{payment.payment_mode}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
