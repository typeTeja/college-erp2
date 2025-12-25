'use client';

import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { feeService } from '@/utils/fee-service';
import type { FeeStructureCreate, FeeComponent, FeeInstallment, FeeCategory } from '@/types/fee';
import { Plus, Trash2, Save } from 'lucide-react';

interface FeeStructureFormProps {
    onSuccess?: () => void;
}

export function FeeStructureForm({ onSuccess }: FeeStructureFormProps) {
    const queryClient = useQueryClient();
    const [formData, setFormData] = useState<FeeStructureCreate>({
        program_id: 0,
        academic_year: '2024-2025',
        year: 1,
        category: 'GENERAL' as FeeCategory,
        components: [
            { name: 'Tuition Fee', amount: 0, is_refundable: false },
        ],
        installments: [
            { installment_number: 1, amount: 0, due_date: '' },
        ],
    });

    const createMutation = useMutation({
        mutationFn: (data: FeeStructureCreate) => feeService.structures.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['fee-structures'] });
            alert('Fee structure created successfully!');
            onSuccess?.();
        },
        onError: (error) => {
            console.error('Failed to create fee structure:', error);
            alert('Failed to create fee structure. Please try again.');
        },
    });

    const addComponent = () => {
        setFormData({
            ...formData,
            components: [
                ...formData.components,
                { name: '', amount: 0, is_refundable: false },
            ],
        });
    };

    const removeComponent = (index: number) => {
        setFormData({
            ...formData,
            components: formData.components.filter((_, i) => i !== index),
        });
    };

    const updateComponent = (index: number, field: keyof FeeComponent, value: any) => {
        const updated = [...formData.components];
        updated[index] = { ...updated[index], [field]: value };
        setFormData({ ...formData, components: updated });
    };

    const addInstallment = () => {
        setFormData({
            ...formData,
            installments: [
                ...formData.installments,
                {
                    installment_number: formData.installments.length + 1,
                    amount: 0,
                    due_date: ''
                },
            ],
        });
    };

    const removeInstallment = (index: number) => {
        setFormData({
            ...formData,
            installments: formData.installments.filter((_, i) => i !== index),
        });
    };

    const updateInstallment = (index: number, field: keyof FeeInstallment, value: any) => {
        const updated = [...formData.installments];
        updated[index] = { ...updated[index], [field]: value };
        setFormData({ ...formData, installments: updated });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        // Validate
        if (formData.program_id === 0) {
            alert('Please select a program');
            return;
        }

        if (formData.components.length === 0) {
            alert('Please add at least one fee component');
            return;
        }

        if (formData.installments.length === 0) {
            alert('Please add at least one installment');
            return;
        }

        createMutation.mutate(formData);
    };

    const totalAmount = formData.components.reduce((sum, c) => sum + Number(c.amount), 0);
    const totalInstallments = formData.installments.reduce((sum, i) => sum + Number(i.amount), 0);
    const isBalanced = totalAmount === totalInstallments;

    return (
        <form onSubmit={handleSubmit} className="space-y-6" method="POST">
            {/* Basic Information */}
            <Card>
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold mb-4 text-gray-800">Basic Information</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Program ID
                            </label>
                            <Input
                                type="number"
                                value={formData.program_id || ''}
                                onChange={(e) => setFormData({ ...formData, program_id: parseInt(e.target.value) || 0 })}
                                placeholder="Enter program ID"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Academic Year
                            </label>
                            <Input
                                type="text"
                                value={formData.academic_year}
                                onChange={(e) => setFormData({ ...formData, academic_year: e.target.value })}
                                placeholder="e.g., 2024-2025"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Year
                            </label>
                            <select
                                value={formData.year}
                                onChange={(e) => setFormData({ ...formData, year: parseInt(e.target.value) })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            >
                                <option value={1}>1st Year</option>
                                <option value={2}>2nd Year</option>
                                <option value={3}>3rd Year</option>
                                <option value={4}>4th Year</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Category
                            </label>
                            <select
                                value={formData.category}
                                onChange={(e) => setFormData({ ...formData, category: e.target.value as FeeCategory })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            >
                                <option value="GENERAL">General</option>
                                <option value="MANAGEMENT">Management</option>
                                <option value="NRI">NRI</option>
                                <option value="SCHOLARSHIP">Scholarship</option>
                            </select>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Fee Components */}
            <Card>
                <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-gray-800">Fee Components</h3>
                        <Button type="button" onClick={addComponent} variant="outline" size="sm">
                            <Plus className="w-4 h-4 mr-2" />
                            Add Component
                        </Button>
                    </div>
                    <div className="space-y-3">
                        {formData.components.map((component, index) => (
                            <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                                <Input
                                    placeholder="Component name"
                                    value={component.name}
                                    onChange={(e) => updateComponent(index, 'name', e.target.value)}
                                    className="flex-1"
                                    required
                                />
                                <Input
                                    type="number"
                                    placeholder="Amount"
                                    value={component.amount || ''}
                                    onChange={(e) => updateComponent(index, 'amount', parseFloat(e.target.value) || 0)}
                                    className="w-32"
                                    required
                                />
                                <label className="flex items-center space-x-2 text-sm">
                                    <input
                                        type="checkbox"
                                        checked={component.is_refundable}
                                        onChange={(e) => updateComponent(index, 'is_refundable', e.target.checked)}
                                        className="rounded"
                                    />
                                    <span>Refundable</span>
                                </label>
                                {formData.components.length > 1 && (
                                    <Button
                                        type="button"
                                        onClick={() => removeComponent(index)}
                                        variant="outline"
                                        size="sm"
                                        className="text-red-600 border-red-200 hover:bg-red-50"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </Button>
                                )}
                            </div>
                        ))}
                    </div>
                    <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                        <p className="text-sm font-semibold text-blue-800">
                            Total Fee: ₹{totalAmount.toLocaleString()}
                        </p>
                    </div>
                </CardContent>
            </Card>

            {/* Installments */}
            <Card>
                <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-gray-800">Installment Schedule</h3>
                        <Button type="button" onClick={addInstallment} variant="outline" size="sm">
                            <Plus className="w-4 h-4 mr-2" />
                            Add Installment
                        </Button>
                    </div>
                    <div className="space-y-3">
                        {formData.installments.map((installment, index) => (
                            <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                                <div className="w-32">
                                    <p className="text-sm font-medium text-gray-700">Installment {installment.installment_number}</p>
                                </div>
                                <Input
                                    type="number"
                                    placeholder="Amount"
                                    value={installment.amount || ''}
                                    onChange={(e) => updateInstallment(index, 'amount', parseFloat(e.target.value) || 0)}
                                    className="w-32"
                                    required
                                />
                                <Input
                                    type="date"
                                    value={installment.due_date}
                                    onChange={(e) => updateInstallment(index, 'due_date', e.target.value)}
                                    className="flex-1"
                                    required
                                />
                                {formData.installments.length > 1 && (
                                    <Button
                                        type="button"
                                        onClick={() => removeInstallment(index)}
                                        variant="outline"
                                        size="sm"
                                        className="text-red-600 border-red-200 hover:bg-red-50"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </Button>
                                )}
                            </div>
                        ))}
                    </div>
                    <div className={`mt-4 p-3 rounded-lg ${isBalanced ? 'bg-green-50' : 'bg-red-50'}`}>
                        <p className={`text-sm font-semibold ${isBalanced ? 'text-green-800' : 'text-red-800'}`}>
                            Total Installments: ₹{totalInstallments.toLocaleString()}
                            {!isBalanced && ' (Does not match total fee!)'}
                        </p>
                    </div>
                </CardContent>
            </Card>

            {/* Submit Button */}
            <div className="flex justify-end">
                <Button
                    type="submit"
                    disabled={!isBalanced || createMutation.isPending}
                    className="bg-blue-600 hover:bg-blue-700 text-white"
                >
                    <Save className="w-4 h-4 mr-2" />
                    {createMutation.isPending ? 'Creating...' : 'Create Fee Structure'}
                </Button>
            </div>
        </form>
    );
}
