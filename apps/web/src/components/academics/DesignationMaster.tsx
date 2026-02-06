"use client"

import React, { useState } from 'react';
import {
    Table, TableBody, TableCell, TableHead,
    TableHeader, TableRow
} from '@/components/ui/table';
import {
    Dialog, DialogContent, DialogDescription,
    DialogFooter, DialogHeader, DialogTitle, DialogTrigger
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import {
    Select, SelectContent, SelectItem,
    SelectTrigger, SelectValue
} from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import {
    Plus, Search, Edit2, Trash2,
    Briefcase, RefreshCw, Filter
} from 'lucide-react';
import { institutionalService } from '@/utils/institutional-service';
import { Designation, DesignationCreateData } from '@/types/institutional';
import { Card, CardContent } from '@/components/ui/card';
import { toast } from 'sonner';

export function DesignationMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingDesig, setEditingDesig] = useState<Designation | null>(null);

    // Form state for Select components
    const [selectedDeptId, setSelectedDeptId] = useState<string>("none");
    const [isTeaching, setIsTeaching] = useState<boolean>(true);

    const { data: designations = [], isLoading, refetch } = institutionalService.useDesignations();
    const { data: departments = [] } = institutionalService.useDepartments();

    const createMutation = institutionalService.useCreateDesignation();
    const updateMutation = institutionalService.useUpdateDesignation();
    const deleteMutation = institutionalService.useDeleteDesignation();

    const filteredDesignations = designations.filter(desig =>
        desig.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        desig.code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleSave = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);

        const data: DesignationCreateData = {
            name: formData.get('name') as string,
            code: (formData.get('code') as string).toUpperCase(),
            level: parseInt(formData.get('level') as string) || 1,
            department_id: selectedDeptId !== "none" ? parseInt(selectedDeptId) : undefined,
            min_experience_years: parseInt(formData.get('min_exp') as string) || 0,
            min_qualification: formData.get('qualification') as string || undefined,
            is_teaching: isTeaching,
            display_order: parseInt(formData.get('display_order') as string) || 0,
        };

        try {
            if (editingDesig) {
                await updateMutation.mutateAsync({ id: editingDesig.id, data });
                toast.success('Designation updated successfully');
                setEditingDesig(null);
            } else {
                await createMutation.mutateAsync(data);
                toast.success('Designation created successfully');
                setIsCreateOpen(false);
            }
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to save designation');
        }
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Are you sure you want to delete this designation?')) {
            try {
                await deleteMutation.mutateAsync(id);
                toast.success('Designation deleted successfully');
            } catch (error: any) {
                toast.error(error.response?.data?.detail || 'Failed to delete designation');
            }
        }
    };

    if (isLoading) {
        return <div className="p-8 text-center animate-pulse text-slate-500">Loading designations...</div>;
    }

    return (
        <div className="space-y-4">
            <div className="flex flex-col md:flex-row justify-between gap-4 bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
                <div className="flex flex-1 gap-4">
                    <div className="relative w-64">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                        <Input
                            placeholder="Search designations..."
                            className="pl-9"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <Button
                        variant="outline"
                        size="icon"
                        onClick={() => refetch()}
                        disabled={isLoading}
                        className="transition-all active:scale-95"
                    >
                        <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
                    </Button>
                    <Dialog open={isCreateOpen} onOpenChange={(open) => {
                        setIsCreateOpen(open);
                        if (open) {
                            setSelectedDeptId("none");
                            setIsTeaching(true);
                        }
                    }}>
                        <DialogTrigger asChild>
                            <Button className="bg-blue-600 hover:bg-blue-700 shadow-sm transition-all active:scale-95">
                                <Plus className="h-4 w-4 mr-2" />
                                Add Designation
                            </Button>
                        </DialogTrigger>
                        <DialogContent className="sm:max-w-[425px] border-none shadow-2xl bg-white/95 backdrop-blur-sm">
                            <form onSubmit={handleSave}>
                                <DialogHeader>
                                    <DialogTitle className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                                        Add New Designation
                                    </DialogTitle>
                                    <DialogDescription className="text-slate-500">
                                        Define a new job role or academic title.
                                    </DialogDescription>
                                </DialogHeader>
                                <div className="flex flex-col gap-5 py-6">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <Label htmlFor="name" className="text-slate-700 font-semibold">Name</Label>
                                            <Input id="name" name="name" placeholder="e.g. Professor" required className="border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all" />
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="code" className="text-slate-700 font-semibold">Code</Label>
                                            <Input id="code" name="code" placeholder="e.g. PROF" required className="uppercase font-mono border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all" />
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <Label htmlFor="level" className="text-slate-700 font-semibold">Level</Label>
                                            <Input id="level" name="level" type="number" defaultValue="1" required className="border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all" />
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="display_order" className="text-slate-700 font-semibold">Display Order</Label>
                                            <Input id="display_order" name="display_order" type="number" defaultValue="0" className="border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all" />
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="department_id" className="text-slate-700 font-semibold">Department</Label>
                                        <Select value={selectedDeptId} onValueChange={setSelectedDeptId}>
                                            <SelectTrigger className="border-slate-200 focus:border-blue-500 focus:ring-blue-500">
                                                <SelectValue placeholder="Select department" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="none">General / All</SelectItem>
                                                {departments.map(dept => (
                                                    <SelectItem key={dept.id} value={dept.id.toString()}>
                                                        {dept.department_name}
                                                    </SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="qualification" className="text-slate-700 font-semibold">Min. Qualification</Label>
                                        <Input id="qualification" name="qualification" placeholder="e.g. PhD" className="border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all" />
                                    </div>

                                    <div className="flex items-center space-x-2 pt-2">
                                        <Checkbox
                                            id="is_teaching"
                                            name="is_teaching"
                                            checked={isTeaching}
                                            onCheckedChange={(checked) => setIsTeaching(!!checked)}
                                        />
                                        <div className="grid gap-1.5 leading-none">
                                            <Label htmlFor="is_teaching" className="text-sm font-medium leading-none cursor-pointer">
                                                Teaching Staff
                                            </Label>
                                            <p className="text-xs text-slate-500">
                                                Determines if this role appears in academic scheduling.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <DialogFooter>
                                    <Button
                                        type="submit"
                                        className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-md transition-all active:scale-95"
                                        disabled={createMutation.isPending}
                                    >
                                        {createMutation.isPending ? 'Creating...' : 'Create Designation'}
                                    </Button>
                                </DialogFooter>
                            </form>
                        </DialogContent>
                    </Dialog>
                </div>
            </div>

            <Card className="border-slate-200 shadow-sm overflow-hidden">
                <CardContent className="p-0">
                    <Table>
                        <TableHeader className="bg-slate-50">
                            <TableRow>
                                <TableHead className="font-semibold text-slate-700">Designation</TableHead>
                                <TableHead className="font-semibold text-slate-700">Code</TableHead>
                                <TableHead className="font-semibold text-slate-700">Type</TableHead>
                                <TableHead className="font-semibold text-slate-700">Level</TableHead>
                                <TableHead className="text-right font-semibold text-slate-700">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredDesignations.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={5} className="text-center py-12 text-slate-500">
                                        <div className="flex flex-col items-center">
                                            <Briefcase className="h-10 w-10 text-slate-300 mb-2" />
                                            <p>No designations found.</p>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ) : (
                                filteredDesignations.map((desig) => (
                                    <TableRow key={desig.id} className="hover:bg-slate-50/50 transition-colors">
                                        <TableCell className="font-medium">
                                            <div className="flex items-center gap-2 text-slate-900">
                                                <Briefcase className="h-4 w-4 text-blue-500" />
                                                {desig.name}
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="outline" className="font-mono bg-slate-50 text-slate-600 border-slate-200">
                                                {desig.code}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <Badge
                                                className={desig.is_teaching
                                                    ? "bg-green-100 text-green-700 hover:bg-green-100 border-none px-2 shadow-none"
                                                    : "bg-slate-100 text-slate-600 hover:bg-slate-100 border-none px-2 shadow-none"}
                                            >
                                                {desig.is_teaching ? 'Teaching' : 'Non-Teaching'}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <span className="text-sm font-medium text-slate-600">L{desig.level}</span>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <div className="flex justify-end gap-1">
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    onClick={() => {
                                                        setEditingDesig(desig);
                                                        setSelectedDeptId(desig.department_id?.toString() || "none");
                                                        setIsTeaching(desig.is_teaching);
                                                    }}
                                                    className="h-8 w-8 text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors"
                                                >
                                                    <Edit2 className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-8 w-8 text-slate-400 hover:text-red-600 hover:bg-red-50 transition-colors"
                                                    onClick={() => handleDelete(desig.id)}
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

            {/* Edit Dialog */}
            <Dialog open={!!editingDesig} onOpenChange={(open) => !open && setEditingDesig(null)}>
                <DialogContent className="sm:max-w-[425px] border-none shadow-2xl bg-white/95 backdrop-blur-sm">
                    {editingDesig && (
                        <form onSubmit={handleSave}>
                            <DialogHeader>
                                <DialogTitle className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                                    Edit Designation
                                </DialogTitle>
                                <DialogDescription className="text-slate-500">
                                    Update information for {editingDesig.name}.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="flex flex-col gap-5 py-6">
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="edit-name" className="text-slate-700 font-semibold">Name</Label>
                                        <Input id="edit-name" name="name" defaultValue={editingDesig.name} required className="border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all" />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="edit-code" className="text-slate-700 font-semibold">Code</Label>
                                        <Input id="edit-code" name="code" defaultValue={editingDesig.code} required className="uppercase font-mono border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all" />
                                    </div>
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="edit-level" className="text-slate-700 font-semibold">Level</Label>
                                        <Input id="edit-level" name="level" type="number" defaultValue={editingDesig.level} required className="border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all" />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="edit-display_order" className="text-slate-700 font-semibold">Display Order</Label>
                                        <Input id="edit-display_order" name="display_order" type="number" defaultValue={editingDesig.display_order} className="border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all" />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="edit-department_id" className="text-slate-700 font-semibold">Department</Label>
                                    <Select value={selectedDeptId} onValueChange={setSelectedDeptId}>
                                        <SelectTrigger className="border-slate-200 focus:border-blue-500 focus:ring-blue-500">
                                            <SelectValue placeholder="Select department" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="none">General / All</SelectItem>
                                            {departments.map(dept => (
                                                <SelectItem key={dept.id} value={dept.id.toString()}>
                                                    {dept.department_name}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="edit-qualification" className="text-slate-700 font-semibold">Min. Qualification</Label>
                                    <Input id="edit-qualification" name="qualification" defaultValue={editingDesig.min_qualification || ''} className="border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all" />
                                </div>

                                <div className="flex items-center space-x-2 pt-2">
                                    <Checkbox
                                        id="edit-is_teaching"
                                        name="is_teaching"
                                        checked={isTeaching}
                                        onCheckedChange={(checked) => setIsTeaching(!!checked)}
                                    />
                                    <div className="grid gap-1.5 leading-none">
                                        <Label htmlFor="edit-is_teaching" className="text-sm font-medium leading-none cursor-pointer">
                                            Teaching Staff
                                        </Label>
                                    </div>
                                </div>
                            </div>
                            <DialogFooter>
                                <Button
                                    type="submit"
                                    className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-md transition-all active:scale-95"
                                    disabled={updateMutation.isPending}
                                >
                                    {updateMutation.isPending ? 'Updating...' : 'Update Designation'}
                                </Button>
                            </DialogFooter>
                        </form>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    );
}
