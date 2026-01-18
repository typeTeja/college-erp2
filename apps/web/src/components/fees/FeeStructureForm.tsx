'use client';

import React, { useState, useEffect } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { feeService } from '@/utils/fee-service';
import { getFeeHeads, type FeeHead } from '@/utils/fee-heads-service';
import { getScholarshipSlabs, type ScholarshipSlab } from '@/utils/scholarship-service';
import type { FeeStructureCreate, FeeComponent, FeeInstallment, FeeCategory } from '@/types/fee';
import { Plus, Trash2, Save, Settings as SettingsIcon, Award } from 'lucide-react';
import Link from 'next/link';
import { toast } from 'sonner';
import { api } from '@/utils/api';

interface FeeStructureFormProps {
    onSuccess?: () => void;
}

export function FeeStructureForm({ onSuccess }: FeeStructureFormProps) {
    const queryClient = useQueryClient();
    const [feeHeads, setFeeHeads] = useState<FeeHead[]>([]);
    const [loadingFeeHeads, setLoadingFeeHeads] = useState(true);
    const [scholarshipSlabs, setScholarshipSlabs] = useState<ScholarshipSlab[]>([]);
    const [selectedSlab, setSelectedSlab] = useState<string>('GENERAL');
    const [originalComponents, setOriginalComponents] = useState<FeeComponent[]>([]);
    const [numberOfInstallments, setNumberOfInstallments] = useState(4);
    const [programs, setPrograms] = useState<any[]>([]);
    const [loadingPrograms, setLoadingPrograms] = useState(true);
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

    // Fetch fee heads, scholarship slabs, and programs on mount
    useEffect(() => {
        const fetchData = async () => {
            try {
                const [heads, slabs, programsData] = await Promise.all([
                    getFeeHeads(true),
                    getScholarshipSlabs(true),
                    api.get('/programs/')
                ]);
                setFeeHeads(heads);
                setScholarshipSlabs(slabs);
                setPrograms(programsData.data);
            } catch (error) {
                console.error('Failed to load data:', error);
                toast.error('Failed to load data');
            } finally {
                setLoadingFeeHeads(false);
                setLoadingPrograms(false);
            }
        };
        fetchData();
    }, []);

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

    const calculateSlabDiscount = (slabCode: string) => {
        if (slabCode === 'GENERAL') {
            // Restore original amounts
            if (originalComponents.length > 0) {
                setFormData({ ...formData, components: [...originalComponents] });
            }
            return;
        }

        const slab = scholarshipSlabs.find(s => s.code === slabCode);
        if (!slab) return;

        // Save original components if not already saved
        if (originalComponents.length === 0) {
            setOriginalComponents([...formData.components]);
        }

        const updatedComponents = formData.components.map(component => {
            // Check if this fee head is applicable for discount
            const componentFeeHeadId = (component as any).fee_head_id;
            const isApplicable = slab.applicable_fee_heads.length === 0 ||
                slab.applicable_fee_heads.includes(componentFeeHeadId);

            if (!isApplicable) return component;

            const originalAmount = component.amount;
            let discountedAmount = originalAmount;

            if (slab.discount_type === 'PERCENTAGE') {
                const discount = (originalAmount * slab.discount_value) / 100;
                const maxDiscount = slab.max_discount_amount || Infinity;
                discountedAmount = originalAmount - Math.min(discount, maxDiscount);
            } else {
                // FIXED discount
                discountedAmount = Math.max(0, originalAmount - slab.discount_value);
            }

            return { ...component, amount: Math.round(discountedAmount) };
        });

        setFormData({ ...formData, components: updatedComponents });
        toast.success(`Applied ${slab.name} discount`);
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

    const generateInstallments = (count: number) => {
        const totalAmount = formData.components.reduce((sum, c) => sum + Number(c.amount), 0);
        const installmentAmount = Math.floor(totalAmount / count);
        const remainder = totalAmount - (installmentAmount * count);

        const today = new Date();
        const newInstallments = [];

        for (let i = 0; i < count; i++) {
            const dueDate = new Date(today);
            dueDate.setMonth(today.getMonth() + (i * 3)); // 3 months apart

            newInstallments.push({
                installment_number: i + 1,
                amount: i === 0 ? installmentAmount + remainder : installmentAmount, // Add remainder to first installment
                due_date: dueDate.toISOString().split('T')[0]
            });
        }

        setFormData({ ...formData, installments: newInstallments });
        toast.success(`Generated ${count} installments automatically`);
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

    // Calculate discount summary
    const originalTotal = originalComponents.length > 0
        ? originalComponents.reduce((sum, c) => sum + Number(c.amount), 0)
        : totalAmount;
    const discountAmount = originalTotal - totalAmount;
    const hasDiscount = selectedSlab !== 'GENERAL' && discountAmount > 0;

    return (
        <form onSubmit={handleSubmit} className="space-y-6" method="POST">
            {/* Basic Information */}
            <Card>
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold mb-4 text-gray-800">Basic Information</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Program *
                            </label>
                            {loadingPrograms ? (
                                <div className="text-sm text-gray-500">Loading programs...</div>
                            ) : (
                                <select
                                    value={formData.program_id || ''}
                                    onChange={(e) => setFormData({ ...formData, program_id: parseInt(e.target.value) })}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    required
                                >
                                    <option value="">Select a program</option>
                                    {programs.map((program) => (
                                        <option key={program.id} value={program.id}>
                                            {program.name} ({program.code})
                                        </option>
                                    ))}
                                </select>
                            )}
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
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                <Award className="w-4 h-4 inline mr-1" />
                                Scholarship Slab
                            </label>
                            <select
                                value={selectedSlab}
                                onChange={(e) => {
                                    const slabCode = e.target.value;
                                    setSelectedSlab(slabCode);
                                    setFormData({ ...formData, slab: slabCode } as any);
                                    calculateSlabDiscount(slabCode);
                                }}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="GENERAL">General (No Discount)</option>
                                {scholarshipSlabs.map(slab => (
                                    <option key={slab.id} value={slab.code}>
                                        {slab.name} - {slab.discount_value}{slab.discount_type === 'PERCENTAGE' ? '%' : '₹'} off
                                    </option>
                                ))}
                            </select>
                            {selectedSlab !== 'GENERAL' && (
                                <p className="text-xs text-green-600 mt-1">
                                    ✓ Scholarship discount will be applied to eligible fee components
                                </p>
                            )}
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Fee Components */}
            <Card>
                <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-gray-800">Fee Components</h3>
                        <div className="flex space-x-2">
                            <Link href="/settings?tab=fee-heads">
                                <Button type="button" variant="outline" size="sm">
                                    <SettingsIcon className="w-4 h-4 mr-2" />
                                    Manage Fee Heads
                                </Button>
                            </Link>
                            <Button type="button" onClick={addComponent} variant="outline" size="sm">
                                <Plus className="w-4 h-4 mr-2" />
                                Add Component
                            </Button>
                        </div>
                    </div>
                    <div className="space-y-3">
                        {formData.components.map((component, index) => (
                            <div key={index} className="p-3 bg-gray-50 rounded-lg space-y-3">
                                <div className="flex items-center space-x-3">
                                    <div className="flex-1">
                                        <label className="block text-xs font-medium text-gray-600 mb-1">
                                            Fee Head
                                        </label>
                                        <select
                                            value={(component as any).fee_head_id || ''}
                                            onChange={(e) => {
                                                const feeHeadId = e.target.value ? parseInt(e.target.value) : null;
                                                const selectedHead = feeHeads.find(h => h.id === feeHeadId);
                                                const updated = [...formData.components];
                                                updated[index] = {
                                                    ...updated[index],
                                                    fee_head_id: feeHeadId,
                                                    name: selectedHead?.name || '',
                                                    is_refundable: selectedHead?.is_refundable || false
                                                } as any;
                                                setFormData({ ...formData, components: updated });
                                            }}
                                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                            required
                                            disabled={loadingFeeHeads}
                                        >
                                            <option value="">
                                                {loadingFeeHeads ? 'Loading...' : 'Select Fee Head'}
                                            </option>
                                            {feeHeads.map(head => (
                                                <option key={head.id} value={head.id}>
                                                    {head.name} ({head.code})
                                                </option>
                                            ))}
                                        </select>
                                        {(component as any).fee_head_id && (
                                            <p className="text-xs text-gray-500 mt-1">
                                                {feeHeads.find(h => h.id === (component as any).fee_head_id)?.description}
                                            </p>
                                        )}
                                    </div>
                                    <div className="w-32">
                                        <label className="block text-xs font-medium text-gray-600 mb-1">
                                            Amount
                                        </label>
                                        <Input
                                            type="number"
                                            placeholder="Amount"
                                            value={component.amount || ''}
                                            onChange={(e) => updateComponent(index, 'amount', parseFloat(e.target.value) || 0)}
                                            required
                                        />
                                    </div>
                                    <div className="flex items-end pb-2">
                                        <label className="flex items-center space-x-2 text-sm">
                                            <input
                                                type="checkbox"
                                                checked={component.is_refundable}
                                                onChange={(e) => updateComponent(index, 'is_refundable', e.target.checked)}
                                                className="rounded"
                                            />
                                            <span>Refundable</span>
                                        </label>
                                    </div>
                                    {formData.components.length > 1 && (
                                        <div className="flex items-end pb-2">
                                            <Button
                                                type="button"
                                                onClick={() => removeComponent(index)}
                                                variant="outline"
                                                size="sm"
                                                className="text-red-600 border-red-200 hover:bg-red-50"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                    {hasDiscount ? (
                        <div className="mt-4 p-4 bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg">
                            <h4 className="font-semibold text-green-900 mb-2 flex items-center">
                                <Award className="w-4 h-4 mr-2" />
                                Scholarship Discount Applied
                            </h4>
                            <div className="space-y-1 text-sm">
                                <div className="flex justify-between">
                                    <span className="text-gray-700">Original Total:</span>
                                    <span className="font-semibold text-gray-900">₹{originalTotal.toLocaleString()}</span>
                                </div>
                                <div className="flex justify-between text-green-700">
                                    <span>Scholarship Discount:</span>
                                    <span className="font-semibold">-₹{discountAmount.toLocaleString()}</span>
                                </div>
                                <div className="flex justify-between text-lg font-bold text-blue-900 border-t border-green-200 pt-2 mt-2">
                                    <span>Final Total:</span>
                                    <span>₹{totalAmount.toLocaleString()}</span>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                            <p className="text-sm font-semibold text-blue-800">
                                Total Fee: ₹{totalAmount.toLocaleString()}
                            </p>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Installments */}
            <Card>
                <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-gray-800">Installment Schedule</h3>
                        <div className="flex items-center space-x-3">
                            <div className="flex items-center space-x-2">
                                <label className="text-sm font-medium text-gray-700">
                                    Number of Installments:
                                </label>
                                <Input
                                    type="number"
                                    min="1"
                                    max="12"
                                    value={numberOfInstallments}
                                    onChange={(e) => setNumberOfInstallments(parseInt(e.target.value) || 1)}
                                    className="w-20"
                                />
                                <Button
                                    type="button"
                                    onClick={() => generateInstallments(numberOfInstallments)}
                                    variant="default"
                                    size="sm"
                                    className="bg-green-600 hover:bg-green-700 text-white"
                                >
                                    Auto-Generate
                                </Button>
                            </div>
                            <Button type="button" onClick={addInstallment} variant="outline" size="sm">
                                <Plus className="w-4 h-4 mr-2" />
                                Add Manually
                            </Button>
                        </div>
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
