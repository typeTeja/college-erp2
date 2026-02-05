'use client';

import React, { useState } from 'react';
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
import { Plus, Edit, Trash2, Search } from 'lucide-react';
import { programService } from '@/utils/program-service';
import { institutionalService } from '@/utils/institutional-service';
import { Program, ProgramCreateData } from '@/types/program';
import { ProgramType, ProgramStatus } from '@/types/academic-base';
import { toast } from 'sonner';

export function ProgramMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingProgram, setEditingProgram] = useState<Program | null>(null);

    const { data: programs = [], isLoading } = programService.usePrograms();
    const { data: departments = [] } = institutionalService.useDepartments();
    const createMutation = programService.useCreateProgram();
    const updateMutation = programService.useUpdateProgram();

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
            duration_years: parseInt(formData.get('duration_years') as string),
            number_of_semesters: parseInt(formData.get('number_of_semesters') as string),
            status: formData.get('status') as ProgramStatus || ProgramStatus.ACTIVE,
        };

        try {
            if (editingProgram) {
                await updateMutation.mutateAsync({ id: editingProgram.id, data });
                toast.success('Program updated successfully');
            } else {
                await createMutation.mutateAsync(data);
                toast.success('Program created successfully');
            }
            setIsCreateOpen(false);
            setEditingProgram(null);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to save program');
        }
    };

    if (isLoading) {
        return <div className="p-8 text-center animate-pulse text-slate-500">Loading programs...</div>;
    }

    return (
        <div className="space-y-4">
            {/* ... search input code ... */}
            <div className="flex justify-between items-center bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
                <div className="relative w-72">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                    <Input 
                        placeholder="Search programs..." 
                        className="pl-9"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <Dialog open={isCreateOpen} onOpenChange={(open) => {
                    setIsCreateOpen(open);
                    if (!open) setEditingProgram(null);
                }}>
                    <DialogTrigger asChild>
                        <Button className="bg-blue-600 hover:bg-blue-700">
                            <Plus className="h-4 w-4 mr-2" />
                            Add Program
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[425px]">
                        <form onSubmit={handleSave}>
                            <DialogHeader>
                                <DialogTitle>{editingProgram ? 'Edit Program' : 'Add New Program'}</DialogTitle>
                                <DialogDescription>
                                    Enter the details of the degree program. Click save when you're done.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="name" className="text-right">Name</Label>
                                    <Input id="name" name="name" defaultValue={editingProgram?.name} className="col-span-3" required />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="code" className="text-right">Code</Label>
                                    <Input id="code" name="code" defaultValue={editingProgram?.code} className="col-span-3" required />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="department_id" className="text-right">Department</Label>
                                    <select 
                                        id="department_id" 
                                        name="department_id" 
                                        defaultValue={editingProgram?.department_id || ''}
                                        className="col-span-3 flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    >
                                        <option value="">Select Department</option>
                                        {departments.map((dept) => (
                                            <option key={dept.id} value={dept.id}>{dept.department_name} ({dept.department_code})</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="program_type" className="text-right">Type</Label>
                                    <select 
                                        id="program_type" 
                                        name="program_type" 
                                        defaultValue={editingProgram?.program_type || ProgramType.UG}
                                        className="col-span-3 flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    >
                                        {Object.values(ProgramType).map(type => (
                                            <option key={type} value={type}>{type}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="duration_years" className="text-right">Years</Label>
                                    <Input 
                                        id="duration_years" 
                                        name="duration_years" 
                                        type="number" 
                                        defaultValue={editingProgram?.duration_years || 4} 
                                        className="col-span-3" 
                                        required 
                                    />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="number_of_semesters" className="text-right">Semesters</Label>
                                    <Input 
                                        id="number_of_semesters" 
                                        name="number_of_semesters" 
                                        type="number" 
                                        defaultValue={editingProgram?.number_of_semesters || 8} 
                                        className="col-span-3" 
                                        required 
                                    />
                                </div>
                            </div>
                            <DialogFooter>
                                <Button type="submit" disabled={createMutation.isPending || updateMutation.isPending}>
                                    {editingProgram ? 'Update Program' : 'Create Program'}
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
                                <TableHead>Program Name</TableHead>
                                <TableHead>Code</TableHead>
                                <TableHead>Department</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Duration</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredPrograms.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={7} className="text-center py-12 text-slate-500">
                                        No programs found.
                                    </TableCell>
                                </TableRow>
                            ) : (
                                filteredPrograms.map((program) => (
                                    <TableRow key={program.id}>
                                        <TableCell className="font-medium text-slate-900">{program.name}</TableCell>
                                        <TableCell className="font-mono text-xs">{program.code}</TableCell>
                                        <TableCell>
                                            {departments.find(d => d.id === program.department_id)?.department_name || '-'}
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="outline" className="bg-slate-50">
                                                {program.program_type}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-sm text-slate-600">
                                            {program.duration_years} Years ({program.number_of_semesters} Sems)
                                        </TableCell>
                                        <TableCell>
                                            <Badge className={program.status === ProgramStatus.ACTIVE ? "bg-green-100 text-green-700 hover:bg-green-100" : "bg-slate-100 text-slate-700 hover:bg-slate-100"}>
                                                {program.status}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                onClick={() => {
                                                    setEditingProgram(program);
                                                    setIsCreateOpen(true);
                                                }}
                                            >
                                                <Edit className="h-4 w-4 text-slate-500" />
                                            </Button>
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
