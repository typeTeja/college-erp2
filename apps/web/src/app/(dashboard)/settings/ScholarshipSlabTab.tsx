'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
    getScholarshipSlabs,
    createScholarshipSlab,
    updateScholarshipSlab,
    deleteScholarshipSlab,
    type ScholarshipSlab,
    type ScholarshipSlabCreate
} from '@/utils/scholarship-service';
import { getFeeHeads, type FeeHead } from '@/utils/fee-heads-service';
import { Plus, Edit, Trash2, Award, Save, X } from 'lucide-react';
import { toast } from 'sonner';

export function ScholarshipSlabTab() {
    const queryClient = useQueryClient();
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [editingSlab, setEditingSlab] = useState<ScholarshipSlab | null>(null);

    // Fetch scholarship slabs
    const { data: slabs = [], isLoading } = useQuery({
        queryKey: ['scholarship-slabs'],
        queryFn: () => getScholarshipSlabs(),
    });

    // Fetch fee heads for the form
    const { data: feeHeads = [] } = useQuery({
        queryKey: ['fee-heads'],
        queryFn: () => getFeeHeads(true),
    });

    // Delete mutation
    const deleteMutation = useMutation({
        mutationFn: deleteScholarshipSlab,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['scholarship-slabs'] });
            toast.success('Scholarship slab deleted successfully');
        },
        onError: () => {
            toast.error('Failed to delete scholarship slab');
        },
    });

    const handleEdit = (slab: ScholarshipSlab) => {
        setEditingSlab(slab);
        setIsFormOpen(true);
    };

    const handleDelete = async (id: number) => {
        if (confirm('Are you sure you want to delete this scholarship slab?')) {
            deleteMutation.mutate(id);
        }
    };

    const handleFormClose = () => {
        setIsFormOpen(false);
        setEditingSlab(null);
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                        <Award className="w-6 h-6 mr-2 text-blue-600" />
                        Scholarship Slabs
                    </h2>
                    <p className="text-gray-600 mt-1">
                        Manage merit-based and category-based fee discounts
                    </p>
                </div>
                <Button
                    onClick={() => setIsFormOpen(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white"
                >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Scholarship Slab
                </Button>
            </div>

            {/* Slabs List */}
            <Card>
                <CardHeader>
                    <CardTitle>Active Scholarship Slabs</CardTitle>
                </CardHeader>
                <CardContent>
                    {isLoading ? (
                        <div className="text-center py-8 text-gray-500">Loading...</div>
                    ) : slabs.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                            No scholarship slabs found. Create one to get started.
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-gray-50 border-b">
                                    <tr>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                                            Name
                                        </th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                                            Code
                                        </th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                                            Eligibility
                                        </th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                                            Discount
                                        </th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                                            Status
                                        </th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                                            Actions
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200">
                                    {slabs.map((slab) => (
                                        <tr key={slab.id} className="hover:bg-gray-50">
                                            <td className="px-4 py-4">
                                                <div>
                                                    <p className="font-semibold text-gray-900">{slab.name}</p>
                                                    {slab.description && (
                                                        <p className="text-sm text-gray-500">{slab.description}</p>
                                                    )}
                                                </div>
                                            </td>
                                            <td className="px-4 py-4">
                                                <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm font-medium">
                                                    {slab.code}
                                                </span>
                                            </td>
                                            <td className="px-4 py-4 text-sm text-gray-600">
                                                {slab.min_percentage}% - {slab.max_percentage}%
                                            </td>
                                            <td className="px-4 py-4">
                                                <span className="font-semibold text-green-600">
                                                    {slab.discount_value}
                                                    {slab.discount_type === 'PERCENTAGE' ? '%' : '₹'}
                                                </span>
                                                {slab.max_discount_amount && (
                                                    <p className="text-xs text-gray-500">
                                                        Max: ₹{slab.max_discount_amount.toLocaleString()}
                                                    </p>
                                                )}
                                            </td>
                                            <td className="px-4 py-4">
                                                <span
                                                    className={`px-2 py-1 rounded text-xs font-medium ${slab.is_active
                                                        ? 'bg-green-100 text-green-800'
                                                        : 'bg-gray-100 text-gray-800'
                                                        }`}
                                                >
                                                    {slab.is_active ? 'Active' : 'Inactive'}
                                                </span>
                                            </td>
                                            <td className="px-4 py-4">
                                                <div className="flex space-x-2">
                                                    <Button
                                                        variant="outline"
                                                        size="sm"
                                                        onClick={() => handleEdit(slab)}
                                                        className="text-blue-600 border-blue-200 hover:bg-blue-50"
                                                    >
                                                        <Edit className="w-4 h-4" />
                                                    </Button>
                                                    <Button
                                                        variant="outline"
                                                        size="sm"
                                                        onClick={() => handleDelete(slab.id)}
                                                        className="text-red-600 border-red-200 hover:bg-red-50"
                                                    >
                                                        <Trash2 className="w-4 h-4" />
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

            {/* Form Modal */}
            {isFormOpen && (
                <ScholarshipSlabForm
                    slab={editingSlab}
                    feeHeads={feeHeads}
                    onClose={handleFormClose}
                />
            )}
        </div>
    );
}

interface ScholarshipSlabFormProps {
    slab: ScholarshipSlab | null;
    feeHeads: FeeHead[];
    onClose: () => void;
}

function ScholarshipSlabForm({ slab, feeHeads, onClose }: ScholarshipSlabFormProps) {
    const queryClient = useQueryClient();
    const [formData, setFormData] = useState<ScholarshipSlabCreate>({
        name: slab?.name || '',
        code: slab?.code || '',
        description: slab?.description || '',
        min_percentage: slab?.min_percentage ?? 0,
        max_percentage: slab?.max_percentage ?? 100,
        discount_type: slab?.discount_type || 'PERCENTAGE',
        discount_value: slab?.discount_value ?? 0,
        max_discount_amount: slab?.max_discount_amount ?? undefined,
        applicable_fee_heads: slab?.applicable_fee_heads || [],
    });

    const createMutation = useMutation({
        mutationFn: createScholarshipSlab,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['scholarship-slabs'] });
            toast.success('Scholarship slab created successfully');
            onClose();
        },
        onError: () => {
            toast.error('Failed to create scholarship slab');
        },
    });

    const updateMutation = useMutation({
        mutationFn: (data: { id: number; updates: Partial<ScholarshipSlabCreate> }) =>
            updateScholarshipSlab(data.id, data.updates),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['scholarship-slabs'] });
            toast.success('Scholarship slab updated successfully');
            onClose();
        },
        onError: () => {
            toast.error('Failed to update scholarship slab');
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (slab) {
            updateMutation.mutate({ id: slab.id, updates: formData });
        } else {
            createMutation.mutate(formData);
        }
    };

    const toggleFeeHead = (feeHeadId: number) => {
        const current = formData.applicable_fee_heads || [];
        const updated = current.includes(feeHeadId)
            ? current.filter(id => id !== feeHeadId)
            : [...current, feeHeadId];
        setFormData({ ...formData, applicable_fee_heads: updated });
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle>
                            {slab ? 'Edit Scholarship Slab' : 'Create Scholarship Slab'}
                        </CardTitle>
                        <Button variant="ghost" size="sm" onClick={onClose}>
                            <X className="w-4 h-4" />
                        </Button>
                    </div>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {/* Basic Information */}
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label htmlFor="name">Name *</Label>
                                <Input
                                    id="name"
                                    value={formData.name}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    placeholder="e.g., Merit Scholarship - Grade A"
                                    required
                                />
                            </div>
                            <div>
                                <Label htmlFor="code">Code *</Label>
                                <Input
                                    id="code"
                                    value={formData.code}
                                    onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })}
                                    placeholder="e.g., SLAB_A"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <Label htmlFor="description">Description</Label>
                            <Input
                                id="description"
                                value={formData.description}
                                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                placeholder="Brief description of this scholarship"
                            />
                        </div>

                        {/* Eligibility Criteria */}
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label htmlFor="min_percentage">Minimum Percentage *</Label>
                                <Input
                                    id="min_percentage"
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    max="100"
                                    value={formData.min_percentage}
                                    onChange={(e) => setFormData({ ...formData, min_percentage: parseFloat(e.target.value) })}
                                    required
                                />
                            </div>
                            <div>
                                <Label htmlFor="max_percentage">Maximum Percentage *</Label>
                                <Input
                                    id="max_percentage"
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    max="100"
                                    value={formData.max_percentage}
                                    onChange={(e) => setFormData({ ...formData, max_percentage: parseFloat(e.target.value) })}
                                    required
                                />
                            </div>
                        </div>

                        {/* Discount Configuration */}
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label htmlFor="discount_type">Discount Type *</Label>
                                <select
                                    id="discount_type"
                                    value={formData.discount_type}
                                    onChange={(e) => setFormData({ ...formData, discount_type: e.target.value as 'PERCENTAGE' | 'FIXED' })}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                    required
                                >
                                    <option value="PERCENTAGE">Percentage</option>
                                    <option value="FIXED">Fixed Amount</option>
                                </select>
                            </div>
                            <div>
                                <Label htmlFor="discount_value">
                                    Discount Value * ({formData.discount_type === 'PERCENTAGE' ? '%' : '₹'})
                                </Label>
                                <Input
                                    id="discount_value"
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    value={formData.discount_value}
                                    onChange={(e) => setFormData({ ...formData, discount_value: parseFloat(e.target.value) })}
                                    required
                                />
                            </div>
                        </div>

                        {formData.discount_type === 'PERCENTAGE' && (
                            <div>
                                <Label htmlFor="max_discount_amount">Maximum Discount Amount (₹)</Label>
                                <Input
                                    id="max_discount_amount"
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    value={formData.max_discount_amount || ''}
                                    onChange={(e) => setFormData({
                                        ...formData,
                                        max_discount_amount: e.target.value ? parseFloat(e.target.value) : undefined
                                    })}
                                    placeholder="Optional cap on discount amount"
                                />
                            </div>
                        )}

                        {/* Applicable Fee Heads */}
                        <div>
                            <Label>Applicable Fee Heads (Leave empty for all)</Label>
                            <div className="mt-2 space-y-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg p-3">
                                {feeHeads.map((feeHead) => (
                                    <label key={feeHead.id} className="flex items-center space-x-2 cursor-pointer">
                                        <input
                                            type="checkbox"
                                            checked={formData.applicable_fee_heads?.includes(feeHead.id) || false}
                                            onChange={() => toggleFeeHead(feeHead.id)}
                                            className="rounded"
                                        />
                                        <span className="text-sm">{feeHead.name} ({feeHead.code})</span>
                                    </label>
                                ))}
                            </div>
                            <p className="text-xs text-gray-500 mt-1">
                                If no fee heads are selected, discount will apply to all fee components
                            </p>
                        </div>

                        {/* Actions */}
                        <div className="flex justify-end space-x-3 pt-4 border-t">
                            <Button type="button" variant="outline" onClick={onClose}>
                                Cancel
                            </Button>
                            <Button
                                type="submit"
                                className="bg-blue-600 hover:bg-blue-700 text-white"
                                disabled={createMutation.isPending || updateMutation.isPending}
                            >
                                <Save className="w-4 h-4 mr-2" />
                                {slab ? 'Update' : 'Create'} Scholarship Slab
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
