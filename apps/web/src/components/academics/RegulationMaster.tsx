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
import { Plus, Edit, Trash2, Search, Lock, Unlock, ShieldCheck } from 'lucide-react';
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
            const detail = error.response?.data?.detail;
            const message = Array.isArray(detail) 
                ? detail.map((d: any) => d.msg).join(", ") 
                : typeof detail === 'string' ? detail : 'Failed to save regulation';
            toast.error(message);
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
        return <div className="p-8 text-center animate-pulse text-slate-500 font-medium tracking-tight">Loading regulations...</div>;
    }

    return (
        <div className="space-y-6">
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <div className="flex flex-1 flex-col md:flex-row gap-4 w-full">
                    <div className="relative w-full md:w-80">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                        <Input 
                            placeholder="Search regulations..." 
                            className="pl-10 h-11 border-slate-200 rounded-lg"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <select 
                        className="h-11 w-full md:w-64 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value={selectedProgramId || ''}
                        onChange={(e) => setSelectedProgramId(e.target.value ? parseInt(e.target.value) : undefined)}
                    >
                        <option value="">All Programs Filter</option>
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
                        <Button className="bg-blue-600 hover:bg-blue-700 h-11 px-6 shadow-md transition-all active:scale-95 whitespace-nowrap">
                            <Plus className="h-4 w-4 mr-2" />
                            Add Regulation
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[700px] gap-0 p-0 overflow-hidden">
                        <form onSubmit={handleSave}>
                            <DialogHeader className="p-6 bg-slate-50 border-b border-slate-200">
                                <DialogTitle className="text-xl font-bold text-slate-900">
                                    {editingRegulation ? 'Edit Regulation' : 'New Academic Regulation'}
                                </DialogTitle>
                                <DialogDescription className="text-slate-500">
                                    Define credits, passing thresholds, and detention logic.
                                </DialogDescription>
                            </DialogHeader>

                            <div className="p-6 grid grid-cols-2 gap-x-8 gap-y-6 max-h-[70vh] overflow-y-auto">
                                {/* Section 1: Identification */}
                                <div className="col-span-2">
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Identification</h4>
                                    <div className="grid grid-cols-2 gap-6">
                                        <div className="space-y-2">
                                            <Label htmlFor="program_id" className="text-sm font-semibold text-slate-700">Target Program <span className="text-red-500">*</span></Label>
                                            <select 
                                                id="program_id" 
                                                name="program_id" 
                                                defaultValue={editingRegulation?.program_id || selectedProgramId || ''}
                                                className="w-full h-11 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                                required
                                            >
                                                <option value="">Select a program</option>
                                                {programs.map(p => (
                                                    <option key={p.id} value={p.id}>{p.name}</option>
                                                ))}
                                            </select>
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="program_type" className="text-sm font-semibold text-slate-700">Level</Label>
                                            <select 
                                                id="program_type" 
                                                name="program_type" 
                                                defaultValue={editingRegulation?.program_type || ProgramType.UG}
                                                className="w-full h-11 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                            >
                                                {Object.values(ProgramType).map(type => (
                                                    <option key={type} value={type}>{type}</option>
                                                ))}
                                            </select>
                                        </div>
                                        <div className="col-span-2 space-y-2">
                                            <Label htmlFor="name" className="text-sm font-semibold text-slate-700">Regulation Name <span className="text-red-500">*</span></Label>
                                            <Input id="name" name="name" placeholder="e.g. R24 Academic Rules" defaultValue={editingRegulation?.name} className="h-11 shadow-sm" required />
                                        </div>
                                    </div>
                                </div>

                                {/* Section 2: Credits & Duration */}
                                <div className="col-span-2 pt-2">
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Structure & Credits</h4>
                                    <div className="grid grid-cols-2 gap-6 bg-slate-50 p-6 rounded-xl border border-slate-200">
                                        <div className="space-y-2">
                                            <Label htmlFor="total_credits" className="text-sm font-semibold text-slate-700 font-mono">Total Degree Credits</Label>
                                            <Input id="total_credits" name="total_credits" type="number" defaultValue={editingRegulation?.total_credits || 160} className="h-11 bg-white font-bold text-blue-600" required />
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="duration_years" className="text-sm font-semibold text-slate-700 font-mono">Standard Duration (Years)</Label>
                                            <Input id="duration_years" name="duration_years" type="number" defaultValue={editingRegulation?.duration_years || 4} className="h-11 bg-white font-bold" required />
                                        </div>
                                    </div>
                                </div>

                                {/* Section 3: Passing Criteria */}
                                <div className="col-span-2 pt-2">
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Passing Thresholds (%)</h4>
                                    <div className="grid grid-cols-3 gap-6">
                                        <div className="space-y-2">
                                            <Label htmlFor="internal_pass_percentage" className="text-xs font-semibold text-slate-600">Internal Pass</Label>
                                            <Input id="internal_pass_percentage" name="internal_pass_percentage" type="number" defaultValue={editingRegulation?.internal_pass_percentage || 40} className="h-11" required />
                                            <p className="text-[10px] text-slate-400 font-medium">Mid-term/Sessionals</p>
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="external_pass_percentage" className="text-xs font-semibold text-slate-600">External Pass</Label>
                                            <Input id="external_pass_percentage" name="external_pass_percentage" type="number" defaultValue={editingRegulation?.external_pass_percentage || 40} className="h-11" required />
                                            <p className="text-[10px] text-slate-400 font-medium">University/Final Exam</p>
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="total_pass_percentage" className="text-xs font-semibold text-slate-600">Aggregate Pass</Label>
                                            <Input id="total_pass_percentage" name="total_pass_percentage" type="number" defaultValue={editingRegulation?.total_pass_percentage || 40} className="h-11" required />
                                            <p className="text-[10px] text-slate-400 font-medium">Combined Score</p>
                                        </div>
                                    </div>
                                </div>

                                {/* Section 4: Logic Toggles */}
                                <div className="col-span-2 pt-2">
                                    <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 flex items-center justify-between">
                                        <div className="flex items-center gap-3">
                                            <div className="p-2 bg-amber-100 rounded-lg text-amber-600">
                                                <ShieldCheck className="h-5 w-5" />
                                            </div>
                                            <div className="space-y-0.5">
                                                <Label htmlFor="has_credit_based_detention" className="text-sm font-bold text-slate-900 leading-none">Credit-based Detention</Label>
                                                <p className="text-[10px] text-slate-500">Enforce min credits to promote to next year</p>
                                            </div>
                                        </div>
                                        <Switch 
                                            id="has_credit_based_detention" 
                                            name="has_credit_based_detention" 
                                            defaultChecked={editingRegulation?.has_credit_based_detention}
                                            className="data-[state=checked]:bg-blue-600"
                                        />
                                    </div>
                                </div>
                            </div>
                            <DialogFooter className="p-6 bg-slate-50 border-t border-slate-200">
                                <Button 
                                    type="button" 
                                    variant="outline" 
                                    onClick={() => {
                                        setIsCreateOpen(false);
                                        setEditingRegulation(null);
                                    }}
                                    className="h-11 border-slate-300"
                                >
                                    Cancel
                                </Button>
                                <Button 
                                    type="submit" 
                                    disabled={createMutation.isPending || updateMutation.isPending}
                                    className="bg-blue-600 hover:bg-blue-700 h-11 min-w-[150px]"
                                >
                                    {editingRegulation ? 'Update Regulation' : 'Commit Regulation'}
                                </Button>
                            </DialogFooter>
                        </form>
                    </DialogContent>
                </Dialog>
            </div>

            <Card className="rounded-xl overflow-hidden shadow-sm border-slate-200">
                <CardContent className="p-0">
                    <Table>
                        <TableHeader className="bg-slate-50">
                            <TableRow>
                                <TableHead className="py-4 pl-6 font-bold">Policy Name</TableHead>
                                <TableHead className="py-4 font-bold">Program</TableHead>
                                <TableHead className="py-4 font-bold">Degree Credits</TableHead>
                                <TableHead className="py-4 font-bold">Passing Criteria</TableHead>
                                <TableHead className="py-4 font-bold">Status</TableHead>
                                <TableHead className="text-right py-4 pr-6 font-bold">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredRegulations.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={6} className="text-center py-20 text-slate-400 font-medium">
                                        No academic regulations found.
                                    </TableCell>
                                </TableRow>
                            ) : (
                                filteredRegulations.map((reg) => (
                                    <TableRow key={reg.id} className="hover:bg-slate-50/50 transition-colors">
                                        <TableCell className="py-4 pl-6">
                                            <div className="flex items-center gap-3">
                                                <div className={`p-2 rounded-lg ${reg.is_locked ? 'bg-slate-100 text-slate-500' : 'bg-blue-50 text-blue-600'}`}>
                                                    {reg.is_locked ? <Lock className="h-4 w-4" /> : <Unlock className="h-4 w-4" />}
                                                </div>
                                                <span className="font-bold text-slate-900">{reg.name}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-sm font-medium text-slate-600">
                                            {programs.find(p => p.id === reg.program_id)?.name || 'Unknown'}
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="outline" className="font-mono font-bold text-blue-700 bg-blue-50 border-blue-100">
                                                {reg.total_credits} C
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex flex-col gap-0.5 text-[11px] font-medium text-slate-600">
                                                <span>Int: {reg.internal_pass_percentage}%</span>
                                                <span>Ext: {reg.external_pass_percentage}%</span>
                                                <span className="text-slate-400">Agg: {reg.total_pass_percentage}%</span>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge className={`font-bold text-[10px] px-2 py-0.5 ${reg.is_locked ? "bg-slate-100 text-slate-600 border-slate-200" : "bg-indigo-50 text-indigo-700 border-indigo-100"}`}>
                                                {reg.is_locked ? 'LOCKED' : 'DRAFT'}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right pr-6">
                                            <div className="flex justify-end gap-1">
                                                {!reg.is_locked && (
                                                    <>
                                                        <Button 
                                                            variant="ghost" 
                                                            size="icon"
                                                            className="h-8 w-8 hover:bg-blue-50 hover:text-blue-600"
                                                            onClick={() => {
                                                                setEditingRegulation(reg);
                                                                setIsCreateOpen(true);
                                                            }}
                                                        >
                                                            <Edit className="h-4 w-4" />
                                                        </Button>
                                                        <Button 
                                                            variant="ghost" 
                                                            size="icon"
                                                            className="h-8 w-8 text-amber-500 hover:text-amber-600 hover:bg-amber-50"
                                                            onClick={() => handleLock(reg.id)}
                                                        >
                                                            <Unlock className="h-4 w-4" />
                                                        </Button>
                                                    </>
                                                )}
                                                <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-300 hover:text-red-500 hover:bg-red-50">
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            </div>
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
