'use client';

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { feeService } from '@/utils/fee-service';
import type {
    FeeDefaulter,
    FeePaymentCreate,
    FeeConcessionCreate,
    FeeFineCreate
} from '@/types/fee';
import {
    DollarSign,
    Users,
    AlertTriangle,
    TrendingUp,
    Search,
    Plus,
    FileText
} from 'lucide-react';

export function AdminFeePanel() {
    const queryClient = useQueryClient();
    const [selectedAcademicYear, setSelectedAcademicYear] = useState('2024-2025');
    const [searchQuery, setSearchQuery] = useState('');

    // Fetch defaulters
    const { data: defaulters = [], isLoading } = useQuery({
        queryKey: ['fee-defaulters', selectedAcademicYear],
        queryFn: () => feeService.defaulters.list(selectedAcademicYear),
    });

    // Filter defaulters by search query
    const filteredDefaulters = defaulters.filter(
        (defaulter) =>
            defaulter.student_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            defaulter.admission_number.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Calculate statistics
    const totalDefaulters = defaulters.length;
    const totalDue = defaulters.reduce((sum, d) => sum + d.total_due, 0);
    const avgDue = totalDefaulters > 0 ? totalDue / totalDefaulters : 0;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gray-800">Fee Management</h1>
                    <p className="text-gray-600">Manage fee structures, payments, and defaulters</p>
                </div>
                <div className="flex space-x-3">
                    <Button variant="outline" className="border-blue-200 text-blue-600 hover:bg-blue-50">
                        <FileText className="w-4 h-4 mr-2" />
                        Export Report
                    </Button>
                    <Link href="/fees/structures/new">
                        <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                            <Plus className="w-4 h-4 mr-2" />
                            Create Fee Structure
                        </Button>
                    </Link>
                </div>
            </div>

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="border-blue-200 bg-gradient-to-br from-blue-50 to-white">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600 mb-1">Total Defaulters</p>
                                <p className="text-3xl font-bold text-blue-600">{totalDefaulters}</p>
                            </div>
                            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                                <Users className="w-6 h-6 text-blue-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-red-200 bg-gradient-to-br from-red-50 to-white">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600 mb-1">Total Due</p>
                                <p className="text-3xl font-bold text-red-600">₹{totalDue.toLocaleString()}</p>
                            </div>
                            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                                <AlertTriangle className="w-6 h-6 text-red-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-green-200 bg-gradient-to-br from-green-50 to-white">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600 mb-1">Average Due</p>
                                <p className="text-3xl font-bold text-green-600">₹{avgDue.toLocaleString(undefined, { maximumFractionDigits: 0 })}</p>
                            </div>
                            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                                <TrendingUp className="w-6 h-6 text-green-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-purple-200 bg-gradient-to-br from-purple-50 to-white">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600 mb-1">Collection Rate</p>
                                <p className="text-3xl font-bold text-purple-600">
                                    {totalDefaulters > 0 ? '75%' : '100%'}
                                </p>
                            </div>
                            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                                <DollarSign className="w-6 h-6 text-purple-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Filters and Search */}
            <Card>
                <CardContent className="p-6">
                    <div className="flex items-center space-x-4">
                        <div className="flex-1">
                            <div className="relative">
                                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                                <Input
                                    placeholder="Search by name or admission number..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="pl-10"
                                />
                            </div>
                        </div>
                        <select
                            value={selectedAcademicYear}
                            onChange={(e) => setSelectedAcademicYear(e.target.value)}
                            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="2024-2025">2024-2025</option>
                            <option value="2023-2024">2023-2024</option>
                            <option value="2022-2023">2022-2023</option>
                        </select>
                    </div>
                </CardContent>
            </Card>

            {/* Defaulters Table */}
            <Card>
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold mb-4 text-gray-800">Fee Defaulters</h3>
                    {isLoading ? (
                        <div className="text-center py-8 text-gray-500">Loading defaulters...</div>
                    ) : filteredDefaulters.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                            {searchQuery ? 'No defaulters found matching your search.' : 'No fee defaulters found. Great!'}
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-gray-50 border-b">
                                    <tr>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Student</th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Program</th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Year</th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Total Due</th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Overdue</th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Last Payment</th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200">
                                    {filteredDefaulters.map((defaulter) => (
                                        <tr key={defaulter.student_id} className="hover:bg-gray-50">
                                            <td className="px-4 py-4">
                                                <div>
                                                    <p className="font-semibold text-gray-800">{defaulter.student_name}</p>
                                                    <p className="text-sm text-gray-500">{defaulter.admission_number}</p>
                                                </div>
                                            </td>
                                            <td className="px-4 py-4 text-sm text-gray-600">{defaulter.program}</td>
                                            <td className="px-4 py-4 text-sm text-gray-600">Year {defaulter.year}</td>
                                            <td className="px-4 py-4">
                                                <span className="font-bold text-red-600">₹{defaulter.total_due.toLocaleString()}</span>
                                            </td>
                                            <td className="px-4 py-4">
                                                <Badge variant="danger">
                                                    {defaulter.overdue_installments} installments
                                                </Badge>
                                            </td>
                                            <td className="px-4 py-4 text-sm text-gray-600">
                                                {defaulter.last_payment_date
                                                    ? new Date(defaulter.last_payment_date).toLocaleDateString()
                                                    : 'Never'}
                                            </td>
                                            <td className="px-4 py-4">
                                                <div className="flex space-x-2">
                                                    <Button
                                                        variant="outline"
                                                        size="sm"
                                                        className="text-blue-600 border-blue-200 hover:bg-blue-50"
                                                    >
                                                        View Details
                                                    </Button>
                                                    <Button
                                                        variant="outline"
                                                        size="sm"
                                                        className="text-green-600 border-green-200 hover:bg-green-50"
                                                    >
                                                        Record Payment
                                                    </Button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
