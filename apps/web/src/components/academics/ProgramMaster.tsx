'use client';

import React, { useState, useEffect } from 'react';
import { 
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow 
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { 
    Dialog, DialogContent, DialogDescription, DialogFooter, 
    DialogHeader, DialogTitle, DialogTrigger 
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Checkbox } from '@/components/ui/checkbox';
import { 
    Plus, Edit, Trash2, Search, Info, CheckCircle2, XCircle
} from 'lucide-react';
import { programService } from '@/utils/program-service';
import { institutionalService } from '@/utils/institutional-service';
import { Program, ProgramCreateData } from '@/types/program';
import { ProgramType, ProgramStatus } from '@/types/academic-base';
import { toast } from 'sonner';

export function ProgramMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingProgram, setEditingProgram] = useState<Program | null>(null);

    // Form state (managed for real-time calculation & spec helper texts)
    const [semesterSystem, setSemesterSystem] = useState(true);
    const [durationYears, setDurationYears] = useState(4);
    const [rnetRequired, setRnetRequired] = useState(true);
    const [allowInstallments, setAllowInstallments] = useState(true);
    const [isActive, setIsActive] = useState(true);

    const { data: programs = [], isLoading } = programService.usePrograms();
    const { data: departments = [] } = institutionalService.useDepartments();
    const createMutation = programService.useCreateProgram();
    const updateMutation = programService.useUpdateProgram();

    // Reset/Sync form state when modal opens or editingProgram changes
    useEffect(() => {
        if (editingProgram) {
            setSemesterSystem(editingProgram.semester_system);
            setDurationYears(editingProgram.duration_years);
            setRnetRequired(editingProgram.rnet_required);
            setAllowInstallments(editingProgram.allow_installments);
            setIsActive(editingProgram.is_active);
        } else {
            setSemesterSystem(true);
            setDurationYears(4);
            setRnetRequired(true);
            setAllowInstallments(true);
            setIsActive(true);
        }
    }, [editingProgram, isCreateOpen]);

    const filteredPrograms = programs.filter(p => 
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
        p.code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleSave = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        
        const data: ProgramCreateData = {
            name: formData.get('name') as string,
            code: formData.get('code') as string,
            alias: formData.get('alias') as string || null,
            program_type: formData.get('program_type') as ProgramType,
            department_id: formData.get('department_id') ? parseInt(formData.get('department_id') as string) : null,
            duration_years: durationYears,
            semester_system: semesterSystem,
            rnet_required: rnetRequired,
            allow_installments: allowInstallments,
            status: isActive ? ProgramStatus.ACTIVE : ProgramStatus.INACTIVE,
            is_active: isActive
        };

        try {
            if (editingProgram) {
                await updateMutation.mutateAsync({ id: editingProgram.id, data });
                toast.success('Course updated successfully');
            } else {
                await createMutation.mutateAsync(data);
                toast.success('Course created successfully');
            }
            setIsCreateOpen(false);
            setEditingProgram(null);
        } catch (error: any) {
            const detail = error.response?.data?.detail;
            const message = Array.isArray(detail) 
                ? detail.map((d: any) => d.msg).join(", ") 
                : typeof detail === 'string' ? detail : 'Failed to save program';
            toast.error(message);
        }
    };

    const calculatedSemesters = semesterSystem ? durationYears * 2 : 0;

    if (isLoading) {
        return <div className="p-8 text-center animate-pulse text-slate-500 font-medium">Loading courses...</div>;
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <div className="relative w-80">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                    <Input 
                        placeholder="Search courses by name or code..." 
                        className="pl-10 h-11 border-slate-200 focus:ring-blue-500 rounded-lg"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <Dialog open={isCreateOpen} onOpenChange={(open) => {
                    setIsCreateOpen(open);
                    if (!open) setEditingProgram(null);
                }}>
                    <DialogTrigger asChild>
                        <Button className="bg-blue-600 hover:bg-blue-700 h-11 px-6 shadow-md transition-all active:scale-95">
                            <Plus className="h-4 w-4 mr-2" />
                            Add Program
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[700px] gap-0 p-0 overflow-hidden">
                        <form onSubmit={handleSave}>
                            <DialogHeader className="p-6 bg-slate-50 border-b border-slate-200">
                                <DialogTitle className="text-xl font-bold text-slate-900">
                                    {editingProgram ? 'Update Course' : 'Add New Program'}
                                </DialogTitle>
                                <DialogDescription className="text-slate-500">
                                    Configure the academic structure and logic for this program.
                                </DialogDescription>
                            </DialogHeader>
                            
                            <div className="p-6 grid grid-cols-2 gap-x-8 gap-y-6">
                                {/* Row 1: Course Code & Short Name */}
                                <div className="space-y-2">
                                    <Label htmlFor="code" className="text-sm font-semibold text-slate-700">Course Code <span className="text-red-500">*</span></Label>
                                    <Input id="code" name="code" placeholder="e.g. BHM" defaultValue={editingProgram?.code} required className="h-10" />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="alias" className="text-sm font-semibold text-slate-700">Short Name <span className="text-red-500">*</span></Label>
                                    <Input id="alias" name="alias" placeholder="e.g. B.H.M" defaultValue={editingProgram?.alias || ''} required className="h-10" />
                                </div>

                                {/* Row 2: Course Name (Full Width) */}
                                <div className="col-span-2 space-y-2">
                                    <Label htmlFor="name" className="text-sm font-semibold text-slate-700">Course Name <span className="text-red-500">*</span></Label>
                                    <Input id="name" name="name" placeholder="e.g. Bachelor of Hotel Management" defaultValue={editingProgram?.name} required className="h-10" />
                                </div>

                                {/* Row 3: Department & Type */}
                                <div className="space-y-2">
                                    <Label htmlFor="department_id" className="text-sm font-semibold text-slate-700">Department</Label>
                                    <select 
                                        id="department_id" 
                                        name="department_id" 
                                        defaultValue={editingProgram?.department_id || ''}
                                        className="w-full flex h-10 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    >
                                        <option value="">Select Department</option>
                                        {departments.map((dept) => (
                                            <option key={dept.id} value={dept.id}>{dept.department_name}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="program_type" className="text-sm font-semibold text-slate-700">Course Level</Label>
                                    <select 
                                        id="program_type" 
                                        name="program_type" 
                                        defaultValue={editingProgram?.program_type || ProgramType.UG}
                                        className="w-full flex h-10 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    >
                                        {Object.values(ProgramType).map(type => (
                                            <option key={type} value={type}>{type}</option>
                                        ))}
                                    </select>
                                </div>

                                {/* Row 4: Duration & Preview */}
                                <div className="space-y-2">
                                    <Label htmlFor="duration_years" className="text-sm font-semibold text-slate-700">Duration (Years) <span className="text-red-500">*</span></Label>
                                    <Input 
                                        id="duration_years" 
                                        name="duration_years" 
                                        type="number" 
                                        value={durationYears}
                                        onChange={(e) => setDurationYears(parseInt(e.target.value) || 1)}
                                        min={1}
                                        max={6}
                                        required 
                                        className="h-10" 
                                    />
                                    <p className="text-[11px] text-slate-500 italic flex items-center gap-1">
                                        <Info className="h-3 w-3" />
                                        Calculates batch: {new Date().getFullYear()}–{new Date().getFullYear() + durationYears}
                                    </p>
                                </div>
                                <div className="flex items-center gap-4 pt-8">
                                    <Badge variant="outline" className="h-10 px-4 bg-blue-50 border-blue-200 text-blue-700 flex items-center gap-2 text-xs">
                                        Preview: {calculatedSemesters} Semesters
                                    </Badge>
                                </div>

                                {/* Row 5: Logic Toggles (Horizontal Row as per Spec) */}
                                <div className="col-span-2 bg-slate-50 p-4 rounded-lg border border-slate-200 grid grid-cols-4 gap-4">
                                    <div className="space-y-3">
                                        <div className="flex items-center space-x-2">
                                            <Switch 
                                                id="sem_system" 
                                                checked={semesterSystem}
                                                onCheckedChange={setSemesterSystem}
                                            />
                                            <Label htmlFor="sem_system" className="text-xs font-bold leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                                Semester System
                                            </Label>
                                        </div>
                                        <p className="text-[10px] leading-tight text-slate-500">
                                            {semesterSystem ? (
                                                <span className="text-green-600 font-medium flex items-center gap-1"><CheckCircle2 className="h-2 w-2" /> Divided into semesters</span>
                                            ) : (
                                                <span className="text-slate-500 flex items-center gap-1"><XCircle className="h-2 w-2" /> Continuous year system</span>
                                            )}
                                        </p>
                                    </div>

                                    <div className="space-y-3">
                                        <div className="flex items-center space-x-2">
                                            <Checkbox 
                                                id="rnet" 
                                                checked={rnetRequired}
                                                onCheckedChange={(checked) => setRnetRequired(checked as boolean)}
                                            />
                                            <Label htmlFor="rnet" className="text-xs font-bold leading-none">
                                                RNET Required
                                            </Label>
                                        </div>
                                        <p className="text-[10px] leading-tight text-slate-500">
                                            Skips entrance test if unchecked
                                        </p>
                                    </div>

                                    <div className="space-y-3">
                                        <div className="flex items-center space-x-2">
                                            <Checkbox 
                                                id="installments" 
                                                checked={allowInstallments}
                                                onCheckedChange={(checked) => setAllowInstallments(checked as boolean)}
                                            />
                                            <Label htmlFor="installments" className="text-xs font-bold leading-none">
                                                Installments
                                            </Label>
                                        </div>
                                        <p className="text-[10px] leading-tight text-slate-500">
                                            Allow partial fee payments
                                        </p>
                                    </div>

                                    <div className="space-y-3">
                                        <div className="flex items-center space-x-2">
                                            <Checkbox 
                                                id="active" 
                                                checked={isActive}
                                                onCheckedChange={(checked) => setIsActive(checked as boolean)}
                                            />
                                            <Label htmlFor="active" className="text-xs font-bold leading-none">
                                                Active
                                            </Label>
                                        </div>
                                        <p className="text-[10px] leading-tight text-slate-500">
                                            Visibility across ERP
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <DialogFooter className="p-6 bg-slate-50 border-t border-slate-200">
                                <Button 
                                    type="button" 
                                    variant="outline" 
                                    onClick={() => {
                                        setIsCreateOpen(false);
                                        setEditingProgram(null);
                                    }}
                                    className="border-slate-300"
                                >
                                    Cancel
                                </Button>
                                <Button 
                                    type="submit" 
                                    disabled={createMutation.isPending || updateMutation.isPending}
                                    className="bg-blue-600 hover:bg-blue-700 min-w-[120px]"
                                >
                                    {editingProgram ? 'Update Course' : 'Create Course'}
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
                                <TableHead className="font-bold py-4">Course Details</TableHead>
                                <TableHead className="font-bold py-4">Structure</TableHead>
                                <TableHead className="font-bold py-4">Type</TableHead>
                                <TableHead className="font-bold py-4">Policies</TableHead>
                                <TableHead className="font-bold py-4">Status</TableHead>
                                <TableHead className="text-right py-4 pr-6">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredPrograms.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={6} className="text-center py-20 text-slate-400 font-medium">
                                        No courses found matching your criteria.
                                    </TableCell>
                                </TableRow>
                            ) : (
                                filteredPrograms.map((program) => (
                                    <TableRow key={program.id} className="hover:bg-slate-50/50 transition-colors">
                                        <TableCell className="py-4">
                                            <div className="flex flex-col">
                                                <span className="font-bold text-slate-900">{program.name}</span>
                                                <div className="flex items-center gap-2 mt-1">
                                                    <span className="text-[11px] font-mono bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded border border-slate-200">
                                                        {program.code}
                                                    </span>
                                                    <span className="text-xs text-slate-500">
                                                        {departments.find(d => d.id === program.department_id)?.department_name || 'No Dept'}
                                                    </span>
                                                </div>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex flex-col gap-1">
                                                <span className="text-sm font-medium text-slate-700">
                                                    {program.duration_years} Years
                                                </span>
                                                <span className="text-[10px] text-slate-500">
                                                    {program.semester_system ? `${program.number_of_semesters} Semesters` : 'Year System'}
                                                </span>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="outline" className="bg-slate-50 border-slate-200 text-slate-600 font-medium">
                                                {program.program_type}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex gap-1.5">
                                                {program.rnet_required && (
                                                    <Badge className="bg-orange-50 text-orange-700 border-orange-100 font-bold text-[10px]">RNET</Badge>
                                                )}
                                                {program.allow_installments && (
                                                    <Badge className="bg-indigo-50 text-indigo-700 border-indigo-100 font-bold text-[10px]">FIX</Badge>
                                                )}
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                <div className={`h-2 w-2 rounded-full ${program.is_active ? 'bg-green-500' : 'bg-slate-300'}`} />
                                                <span className={`text-xs font-bold ${program.is_active ? 'text-green-700' : 'text-slate-500'}`}>
                                                    {program.is_active ? 'ACTIVE' : 'INACTIVE'}
                                                </span>
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-right pr-6">
                                            <div className="flex justify-end gap-1">
                                                <Button 
                                                    variant="ghost" 
                                                    size="icon"
                                                    className="h-8 w-8 hover:bg-blue-50 hover:text-blue-600 transition-colors"
                                                    onClick={() => {
                                                        setEditingProgram(program);
                                                        setIsCreateOpen(true);
                                                    }}
                                                >
                                                    <Edit className="h-4 w-4" />
                                                </Button>
                                                <Button 
                                                    variant="ghost" 
                                                    size="icon" 
                                                    className="h-8 w-8 text-slate-400 hover:text-red-500 hover:bg-red-50 transition-colors"
                                                >
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
