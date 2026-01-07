'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { toast } from 'sonner';
import { Plus, Trash2, Lock, Search, FileText, AlertTriangle } from 'lucide-react';
import { getRegulations, createRegulation, deleteRegulation, lockRegulation } from '@/utils/regulation-service';
import { getProgramsList, ProgramInfo } from '@/utils/master-data-service';
import { Regulation, RegulationCreate } from '@/types/regulation';

// ============================================================================
// Generic Data Table Component (Local Copy)
// ============================================================================

interface Column<T> {
    key: keyof T | string;
    label: string;
    render?: (item: T) => React.ReactNode;
}

interface DataTableProps<T> {
    title: string;
    icon: React.ReactNode;
    data: T[];
    columns: Column<T>[];
    onAdd: () => void;
    onDelete: (item: T) => void;
    loading?: boolean;
}

function DataTable<T extends { id: number }>({
    title, icon, data, columns, onAdd, onDelete, loading
}: DataTableProps<T>) {
    const [search, setSearch] = useState('');

    const filteredData = data.filter(item =>
        JSON.stringify(item).toLowerCase().includes(search.toLowerCase())
    );

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-lg flex items-center gap-2">
                    {icon}
                    {title}
                </CardTitle>
                <div className="flex items-center gap-2">
                    <div className="relative">
                        <Search className="absolute left-2 top-2.5 h-4 w-4 text-slate-400" />
                        <Input
                            placeholder="Search..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            className="pl-8 w-48"
                        />
                    </div>
                    <Button onClick={onAdd} size="sm" className="bg-blue-600 hover:bg-blue-700">
                        <Plus className="h-4 w-4 mr-1" /> Create
                    </Button>
                </div>
            </CardHeader>
            <CardContent>
                {loading ? (
                    <div className="flex justify-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
                    </div>
                ) : filteredData.length === 0 ? (
                    <div className="text-center py-8 text-slate-500">
                        No data found. Click "Create" to add a new entry.
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="border-b bg-slate-50">
                                    {columns.map((col) => (
                                        <th key={String(col.key)} className="px-4 py-3 text-left font-medium text-slate-600">
                                            {col.label}
                                        </th>
                                    ))}
                                    <th className="px-4 py-3 text-right font-medium text-slate-600">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredData.map((item) => (
                                    <tr key={item.id} className="border-b hover:bg-slate-50">
                                        {columns.map((col) => (
                                            <td key={String(col.key)} className="px-4 py-3">
                                                {col.render ? col.render(item) : String((item as any)[col.key] ?? '-')}
                                            </td>
                                        ))}
                                        <td className="px-4 py-3">
                                            <div className="flex justify-end gap-1">
                                                <Button variant="ghost" size="sm" onClick={() => onDelete(item)}>
                                                    <Trash2 className="h-4 w-4 text-red-600" />
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
    );
}

// ============================================================================
// Regulations Tab
// ============================================================================

export function RegulationsTab() {
    const [data, setData] = useState<Regulation[]>([]);
    const [programs, setPrograms] = useState<ProgramInfo[]>([]);
    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);

    // Form State
    const [formData, setFormData] = useState<RegulationCreate>({
        regulation_code: '',
        regulation_name: '',
        program_id: 0,
        promotion_model: 'CREDIT_BASED',
        min_internal_pass: 12,
        min_external_pass: 28,
        min_total_pass: 40,
        theory_max_marks: 100,
        theory_internal_max: 60,
        theory_external_max: 40,
        theory_pass_percentage: 40,
        practical_max_marks: 100,
        practical_internal_max: 40,
        practical_external_max: 60,
        practical_pass_percentage: 50,
        is_active: true
    });

    const fetchData = async () => {
        try {
            const [regResult, progResult] = await Promise.all([
                getRegulations(),
                getProgramsList()
            ]);
            setData(regResult);
            setPrograms(progResult);
        } catch (e) {
            toast.error('Failed to load data');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async () => {
        if (!formData.regulation_code || !formData.regulation_name || !formData.program_id) {
            toast.error("Please fill all required fields");
            return;
        }

        try {
            await createRegulation(formData);
            toast.success('Regulation created successfully');
            setDialogOpen(false);
            fetchData();
        } catch (e: any) {
            toast.error(e?.response?.data?.detail || 'Operation failed');
        }
    };

    const handleDelete = async (item: Regulation) => {
        if (item.is_locked) {
            toast.error("Cannot delete a locked regulation");
            return;
        }
        if (confirm(`Delete regulation "${item.regulation_name}"?`)) {
            try {
                await deleteRegulation(item.id);
                toast.success('Regulation deleted');
                fetchData();
            } catch (e: any) {
                toast.error(e?.response?.data?.detail || 'Failed to delete');
            }
        }
    };

    const handleLock = async (item: Regulation) => {
        if (confirm(`Lock regulation "${item.regulation_name}"? THIS ACTION IS IRREVERSIBLE. Locked regulations cannot be edited.`)) {
            try {
                await lockRegulation(item.id);
                toast.success('Regulation locked');
                fetchData();
            } catch (e: any) {
                toast.error(e?.response?.data?.detail || 'Failed to lock');
            }
        }
    };

    const openAdd = () => {
        setFormData({
            regulation_code: '',
            regulation_name: '',
            program_id: programs[0]?.id || 0,
            promotion_model: 'CREDIT_BASED',
            min_internal_pass: 12,
            min_external_pass: 28,
            min_total_pass: 40,
            theory_max_marks: 100,
            theory_internal_max: 60,
            theory_external_max: 40,
            theory_pass_percentage: 40,
            practical_max_marks: 100,
            practical_internal_max: 40,
            practical_external_max: 60,
            practical_pass_percentage: 50,
            is_active: true
        });
        setDialogOpen(true);
    };

    return (
        <>
            <DataTable
                title="Academic Regulations"
                icon={<FileText className="h-5 w-5 text-blue-600" />}
                data={data}
                loading={loading}
                columns={[
                    { key: 'regulation_code', label: 'Code' },
                    { key: 'regulation_name', label: 'Name' },
                    {
                        key: 'program_id',
                        label: 'Program',
                        render: (item) => {
                            const p = programs.find(p => p.id === item.program_id);
                            return p ? p.code : `ID: ${item.program_id}`;
                        }
                    },
                    {
                        key: 'is_locked',
                        label: 'Status',
                        render: (item) => (
                            <div className="flex gap-2">
                                <Badge variant={item.is_active ? 'default' : 'secondary'}>
                                    {item.is_active ? 'Active' : 'Inactive'}
                                </Badge>
                                {item.is_locked && (
                                    <Badge variant="secondary" className="bg-amber-100 text-amber-800 border-amber-200">
                                        <Lock size={10} className="mr-1" /> Locked
                                    </Badge>
                                )}
                            </div>
                        )
                    },
                    {
                        key: 'actions',
                        label: 'Actions',
                        render: (item) => (
                            !item.is_locked && (
                                <Button variant="ghost" size="sm" onClick={() => handleLock(item)} className="text-amber-600 hover:text-amber-700 hover:bg-amber-50">
                                    <Lock size={14} className="mr-1" /> Lock
                                </Button>
                            )
                        )
                    }
                ]}
                onAdd={openAdd}
                onDelete={handleDelete}
            />

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent className="max-w-lg">
                    <DialogHeader>
                        <DialogTitle>Create New Regulation</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4 max-h-[70vh] overflow-y-auto p-1">
                        <div className="bg-amber-50 border border-amber-200 rounded p-3 text-xs text-amber-800 flex items-start gap-2">
                            <AlertTriangle size={16} className="shrink-0 mt-0.5" />
                            <p>Regulations define the curriculum structure. Once locked (automatically after first batch creation), they cannot be modified.</p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Regulation Code *</Label>
                                <Input
                                    value={formData.regulation_code}
                                    onChange={(e) => setFormData({ ...formData, regulation_code: e.target.value.toUpperCase() })}
                                    placeholder="e.g., R24"
                                />
                            </div>
                            <div>
                                <Label>Program *</Label>
                                <Select
                                    value={formData.program_id.toString()}
                                    onValueChange={(v) => setFormData({ ...formData, program_id: parseInt(v) })}
                                >
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select Program" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {programs.map(p => (
                                            <SelectItem key={p.id} value={p.id.toString()}>{p.code} - {p.name}</SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                        </div>

                        <div>
                            <Label>Regulation Name *</Label>
                            <Input
                                value={formData.regulation_name}
                                onChange={(e) => setFormData({ ...formData, regulation_name: e.target.value })}
                                placeholder="e.g., Regulation 2024 for B.Tech"
                            />
                        </div>

                        {/* Theory Configuration */}
                        <div className="bg-slate-50 p-3 rounded-lg border border-slate-100 space-y-3">
                            <h4 className="font-medium text-sm text-slate-700">Theory Evaluation Schema</h4>
                            <div className="grid grid-cols-4 gap-3">
                                <div>
                                    <Label className="text-xs">Max Marks</Label>
                                    <Input
                                        type="number"
                                        value={formData.theory_max_marks}
                                        onChange={(e) => setFormData({ ...formData, theory_max_marks: parseInt(e.target.value) || 0 })}
                                    />
                                </div>
                                <div>
                                    <Label className="text-xs">Internal Max</Label>
                                    <Input
                                        type="number"
                                        value={formData.theory_internal_max}
                                        onChange={(e) => setFormData({ ...formData, theory_internal_max: parseInt(e.target.value) || 0 })}
                                    />
                                </div>
                                <div>
                                    <Label className="text-xs">External Max</Label>
                                    <Input
                                        type="number"
                                        value={formData.theory_external_max}
                                        onChange={(e) => setFormData({ ...formData, theory_external_max: parseInt(e.target.value) || 0 })}
                                    />
                                </div>
                                <div>
                                    <Label className="text-xs">Pass %</Label>
                                    <div className="relative">
                                        <Input
                                            type="number"
                                            value={formData.theory_pass_percentage}
                                            onChange={(e) => setFormData({ ...formData, theory_pass_percentage: parseInt(e.target.value) || 0 })}
                                            className="pr-6"
                                        />
                                        <span className="absolute right-2 top-2.5 text-xs text-slate-400">%</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Practical Configuration */}
                        <div className="bg-slate-50 p-3 rounded-lg border border-slate-100 space-y-3">
                            <h4 className="font-medium text-sm text-slate-700">Practical Evaluation Schema</h4>
                            <div className="grid grid-cols-4 gap-3">
                                <div>
                                    <Label className="text-xs">Max Marks</Label>
                                    <Input
                                        type="number"
                                        value={formData.practical_max_marks}
                                        onChange={(e) => setFormData({ ...formData, practical_max_marks: parseInt(e.target.value) || 0 })}
                                    />
                                </div>
                                <div>
                                    <Label className="text-xs">Internal Max</Label>
                                    <Input
                                        type="number"
                                        value={formData.practical_internal_max}
                                        onChange={(e) => setFormData({ ...formData, practical_internal_max: parseInt(e.target.value) || 0 })}
                                    />
                                </div>
                                <div>
                                    <Label className="text-xs">External Max</Label>
                                    <Input
                                        type="number"
                                        value={formData.practical_external_max}
                                        onChange={(e) => setFormData({ ...formData, practical_external_max: parseInt(e.target.value) || 0 })}
                                    />
                                </div>
                                <div>
                                    <Label className="text-xs">Pass %</Label>
                                    <div className="relative">
                                        <Input
                                            type="number"
                                            value={formData.practical_pass_percentage}
                                            onChange={(e) => setFormData({ ...formData, practical_pass_percentage: parseInt(e.target.value) || 0 })}
                                            className="pr-6"
                                        />
                                        <span className="absolute right-2 top-2.5 text-xs text-slate-400">%</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Global Passing Defaults (Hidden or minimized if not needed, but keeping for now as secondary) */}
                        <div className="grid grid-cols-3 gap-4 border-t pt-2">
                            <div>
                                <Label>Overall Pass Marks</Label>
                                <Input
                                    type="number"
                                    value={formData.min_total_pass}
                                    onChange={(e) => setFormData({ ...formData, min_total_pass: parseInt(e.target.value) })}
                                />
                            </div>
                        </div>

                        <div className="flex items-center gap-2 pt-2">
                            <Switch
                                checked={formData.is_active}
                                onCheckedChange={(v) => setFormData({ ...formData, is_active: v })}
                            />
                            <Label>Active Status</Label>
                        </div>

                        <div className="flex justify-end gap-2 pt-4">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleSubmit} className="bg-blue-600 hover:bg-blue-700">Create Regulation</Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}
