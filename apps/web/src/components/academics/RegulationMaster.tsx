'use client';

import React, { useState } from 'react';
import { 
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow 
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { 
    Dialog, DialogContent, DialogDescription, DialogFooter, 
    DialogHeader, DialogTitle, DialogTrigger 
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Plus, Edit, Trash2, Search, Lock, Unlock } from 'lucide-react';
import { regulationService } from '@/utils/regulation-service';
import { programService } from '@/utils/program-service';
import { Regulation, RegulationCreateData } from '@/types/regulation';
import { ProgramType } from '@/types/academic-base';
import { toast } from 'sonner';

export function RegulationMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedProgramId, setSelectedProgramId] = useState<number | undefined>(undefined);
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingRegulation, setEditingRegulation] = useState<Regulation | null>(null);

    const { data: programs = [] } = programService.usePrograms();
    const { data: regulations = [], isLoading } = regulationService.useRegulations(selectedProgramId);
    
    const createMutation = regulationService.useCreateRegulation();
    const updateMutation = regulationService.useUpdateRegulation();
    const lockMutation = regulationService.useLockRegulation();

    const filteredRegulations = regulations.filter(r => 
        r.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleSave = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        
        const data: RegulationCreateData = {
            name: formData.get('name') as string,
            program_id: parseInt(formData.get('program_id') as string),
            program_type: formData.get('program_type') as ProgramType,
            total_credits: parseInt(formData.get('total_credits') as string) || 0,
            duration_years: parseInt(formData.get('duration_years') as string) || 4,
            has_credit_based_detention: formData.get('has_credit_based_detention') === 'on',
            min_sgpa: parseFloat(formData.get('min_sgpa') as string) || 0,
            min_cgpa: parseFloat(formData.get('min_cgpa') as string) || 0,
            internal_pass_percentage: parseInt(formData.get('internal_pass_percentage') as string) || 40,
            external_pass_percentage: parseInt(formData.get('external_pass_percentage') as string) || 40,
            total_pass_percentage: parseInt(formData.get('total_pass_percentage') as string) || 40,
        };

        try {
            if (editingRegulation) {
                await updateMutation.mutateAsync({ id: editingRegulation.id, data });
                toast.success('Regulation updated successfully');
            } else {
                await createMutation.mutateAsync(data);
                toast.success('Regulation created successfully');
            }
            setIsCreateOpen(false);
            setEditingRegulation(null);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to save regulation');
        }
    };

    const handleLock = async (id: number) => {
        if (!confirm('Are you sure you want to lock this regulation? It cannot be edited after locking.')) return;
        try {
            await lockMutation.mutateAsync(id);
            toast.success('Regulation locked successfully');
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to lock regulation');
        }
    };

    if (isLoading) {
        return <div className="p-8 text-center animate-pulse text-slate-500">Loading regulations...</div>;
    }

    return (
        <div className="space-y-4">
            <div className="flex flex-col md:flex-row justify-between gap-4 bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
                <div className="flex flex-1 gap-4">
                    <div className="relative w-64">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                        <Input 
                            placeholder="Search regulations..." 
                            className="pl-9"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <select 
                        className="flex h-10 w-64 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value={selectedProgramId || ''}
                        onChange={(e) => setSelectedProgramId(e.target.value ? parseInt(e.target.value) : undefined)}
                    >
                        <option value="">All Programs</option>
                        {programs.map(p => (
                            <option key={p.id} value={p.id}>{p.name}</option>
                        ))}
                    </select>
                </div>
                
                <Dialog open={isCreateOpen} onOpenChange={(open) => {
                    setIsCreateOpen(open);
                    if (!open) setEditingRegulation(null);
                }}>
                    <DialogTrigger asChild>
                        <Button className="bg-blue-600 hover:bg-blue-700">
                            <Plus className="h-4 w-4 mr-2" />
                            Add Regulation
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[550px] max-h-[90vh] overflow-y-auto">
                        <form onSubmit={handleSave}>
                            <DialogHeader>
                                <DialogTitle>{editingRegulation ? 'Edit Regulation' : 'Add New Regulation'}</DialogTitle>
                                <DialogDescription>
                                    Define academic rules, credits, and passing criteria.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="program_id" className="text-right">Program</Label>
                                    <select 
                                        id="program_id" 
                                        name="program_id" 
                                        defaultValue={editingRegulation?.program_id || selectedProgramId || ''}
                                        className="col-span-3 flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        required
                                    >
                                        <option value="">Select a program</option>
                                        {programs.map(p => (
                                            <option key={p.id} value={p.id}>{p.name}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="name" className="text-right">Name</Label>
                                    <Input id="name" name="name" defaultValue={editingRegulation?.name} className="col-span-3" required />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="program_type" className="text-right">Type</Label>
                                    <select 
                                        id="program_type" 
                                        name="program_type" 
                                        defaultValue={editingRegulation?.program_type || ProgramType.UG}
                                        className="col-span-3 flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    >
                                        {Object.values(ProgramType).map(type => (
                                            <option key={type} value={type}>{type}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="total_credits">Total Credits</Label>
                                        <Input id="total_credits" name="total_credits" type="number" defaultValue={editingRegulation?.total_credits || 160} required />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="duration_years">Duration (Years)</Label>
                                        <Input id="duration_years" name="duration_years" type="number" defaultValue={editingRegulation?.duration_years || 4} required />
                                    </div>
                                </div>
                                <div className="grid grid-cols-3 gap-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="internal_pass_percentage">Internal Pass %</Label>
                                        <Input id="internal_pass_percentage" name="internal_pass_percentage" type="number" defaultValue={editingRegulation?.internal_pass_percentage || 40} required />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="external_pass_percentage">External Pass %</Label>
                                        <Input id="external_pass_percentage" name="external_pass_percentage" type="number" defaultValue={editingRegulation?.external_pass_percentage || 40} required />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="total_pass_percentage">Total Pass %</Label>
                                        <Input id="total_pass_percentage" name="total_pass_percentage" type="number" defaultValue={editingRegulation?.total_pass_percentage || 40} required />
                                    </div>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <Switch id="has_credit_based_detention" name="has_credit_based_detention" defaultChecked={editingRegulation?.has_credit_based_detention} />
                                    <Label htmlFor="has_credit_based_detention">Enable Credit-based Detention</Label>
                                </div>
                            </div>
                            <DialogFooter>
                                <Button type="submit" disabled={createMutation.isPending || updateMutation.isPending}>
                                    {editingRegulation ? 'Update Regulation' : 'Create Regulation'}
                                </Button>
                            </DialogFooter>
                        </form>
                    </DialogContent>
                </Dialog>
            </div>

            <Card>
                <CardContent className="p-0">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Regulation Name</TableHead>
                                <TableHead>Program</TableHead>
                                <TableHead>Credits</TableHead>
                                <TableHead>Pass Criteria</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredRegulations.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={6} className="text-center py-12 text-slate-500">
                                        No regulations found.
                                    </TableCell>
                                </TableRow>
                            ) : (
                                filteredRegulations.map((reg) => (
                                    <TableRow key={reg.id}>
                                        <TableCell className="font-medium text-slate-900">
                                            <div className="flex items-center">
                                                {reg.name}
                                                {reg.is_locked && <Lock className="h-3 w-3 ml-2 text-slate-400" />}
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-sm">
                                            {programs.find(p => p.id === reg.program_id)?.name || 'Unknown'}
                                        </TableCell>
                                        <TableCell>{reg.total_credits} Credits</TableCell>
                                        <TableCell className="text-xs text-slate-600">
                                            Int: {reg.internal_pass_percentage}% | Ext: {reg.external_pass_percentage}% | Tot: {reg.total_pass_percentage}%
                                        </TableCell>
                                        <TableCell>
                                            <Badge className={reg.is_locked ? "bg-slate-100 text-slate-700" : "bg-blue-100 text-blue-700"}>
                                                {reg.is_locked ? 'Locked' : 'Draft'}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            {!reg.is_locked && (
                                                <>
                                                    <Button 
                                                        variant="ghost" 
                                                        size="icon"
                                                        onClick={() => {
                                                            setEditingRegulation(reg);
                                                            setIsCreateOpen(true);
                                                        }}
                                                    >
                                                        <Edit className="h-4 w-4 text-slate-500" />
                                                    </Button>
                                                    <Button 
                                                        variant="ghost" 
                                                        size="icon"
                                                        className="text-amber-600 hover:text-amber-700 hover:bg-amber-50"
                                                        onClick={() => handleLock(reg.id)}
                                                    >
                                                        <Unlock className="h-4 w-4" />
                                                    </Button>
                                                </>
                                            )}
                                            <Button variant="ghost" size="icon" className="text-red-500 hover:text-red-600 hover:bg-red-50">
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
