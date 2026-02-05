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
    Briefcase, RefreshCw 
} from 'lucide-react';
import { institutionalService } from '@/utils/institutional-service';
import { Designation, DesignationCreateData } from '@/types/institutional';
import { Card, CardContent } from '@/components/ui/card';

export function DesignationMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingDesig, setEditingDesig] = useState<Designation | null>(null);

    const { data: designations = [], isLoading, refetch } = institutionalService.useDesignations();
    const { data: departments = [] } = institutionalService.useDepartments();
    
    const createMutation = institutionalService.useCreateDesignation();
    const updateMutation = institutionalService.useUpdateDesignation();
    const deleteMutation = institutionalService.useDeleteDesignation();

    const filteredDesignations = designations.filter(desig => 
        desig.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        desig.code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>, isUpdate = false) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        
        const data: DesignationCreateData = {
            name: formData.get('name') as string,
            code: (formData.get('code') as string).toUpperCase(),
            level: parseInt(formData.get('level') as string) || 1,
            department_id: formData.get('department_id') ? parseInt(formData.get('department_id') as string) : undefined,
            min_experience_years: parseInt(formData.get('min_exp') as string) || 0,
            min_qualification: formData.get('qualification') as string || undefined,
            is_teaching: formData.get('is_teaching') === 'on',
            display_order: parseInt(formData.get('display_order') as string) || 0,
        };

        if (isUpdate && editingDesig) {
            await updateMutation.mutateAsync({ id: editingDesig.id, data });
            setEditingDesig(null);
        } else {
            await createMutation.mutateAsync(data);
            setIsCreateOpen(false);
        }
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Are you sure you want to delete this designation?')) {
            await deleteMutation.mutateAsync(id);
        }
    };

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center gap-4">
                <div className="relative flex-1 max-w-sm">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                    <Input
                        placeholder="Search designations..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-9"
                    />
                </div>
                <div className="flex items-center gap-2">
                    <Button 
                        variant="outline" 
                        size="icon" 
                        onClick={() => refetch()}
                        disabled={isLoading}
                    >
                        <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
                    </Button>
                    <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
                        <DialogTrigger asChild>
                            <Button className="bg-blue-600 hover:bg-blue-700">
                                <Plus className="h-4 w-4 mr-2" />
                                Add Designation
                            </Button>
                        </DialogTrigger>
                        <DialogContent className="max-w-md">
                            <form onSubmit={(e) => handleSubmit(e)}>
                                <DialogHeader>
                                    <DialogTitle>Add New Designation</DialogTitle>
                                    <DialogDescription>
                                        Define a new job role or academic title.
                                    </DialogDescription>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="grid gap-2">
                                            <Label htmlFor="name">Name</Label>
                                            <Input id="name" name="name" placeholder="e.g. Professor" required />
                                        </div>
                                        <div className="grid gap-2">
                                            <Label htmlFor="code">Code</Label>
                                            <Input id="code" name="code" placeholder="e.g. PROF" required className="uppercase" />
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="grid gap-2">
                                            <Label htmlFor="level">Level</Label>
                                            <Input id="level" name="level" type="number" defaultValue="1" required />
                                        </div>
                                        <div className="grid gap-2">
                                            <Label htmlFor="display_order">Display Order</Label>
                                            <Input id="display_order" name="display_order" type="number" defaultValue="0" />
                                        </div>
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="department_id">Department (Optional)</Label>
                                        <Select name="department_id">
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select department" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="">General / All</SelectItem>
                                                {departments.map(dept => (
                                                    <SelectItem key={dept.id} value={dept.id.toString()}>
                                                        {dept.department_name}
                                                    </SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="qualification">Min. Qualification</Label>
                                        <Input id="qualification" name="qualification" placeholder="e.g. PhD" />
                                    </div>
                                    <div className="flex items-center space-x-2 pt-2">
                                        <Checkbox id="is_teaching" name="is_teaching" defaultChecked />
                                        <div className="grid gap-1.5 leading-none">
                                            <Label htmlFor="is_teaching" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                                Teaching Staff
                                            </Label>
                                            <p className="text-xs text-slate-500">
                                                Determines if this role appears in academic scheduling.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <DialogFooter>
                                    <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)}>
                                        Cancel
                                    </Button>
                                    <Button type="submit" disabled={createMutation.isPending}>
                                        {createMutation.isPending ? 'Creating...' : 'Create Designation'}
                                    </Button>
                                </DialogFooter>
                            </form>
                        </DialogContent>
                    </Dialog>
                </div>
            </div>

            <Card>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Designation</TableHead>
                            <TableHead>Code</TableHead>
                            <TableHead>Type</TableHead>
                            <TableHead>Level</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={5} className="text-center py-8 text-slate-500">
                                    Loading designations...
                                </TableCell>
                            </TableRow>
                        ) : filteredDesignations.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={5} className="text-center py-8 text-slate-500">
                                    No designations found.
                                </TableCell>
                            </TableRow>
                        ) : (
                            filteredDesignations.map((desig) => (
                                <TableRow key={desig.id}>
                                    <TableCell className="font-medium">
                                        <div className="flex items-center gap-2">
                                            <Briefcase className="h-4 w-4 text-slate-400" />
                                            {desig.name}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant="outline" className="font-mono">
                                            {desig.code}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant={desig.is_teaching ? "default" : "secondary"}>
                                            {desig.is_teaching ? 'Teaching' : 'Non-Teaching'}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>{desig.level}</TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                onClick={() => setEditingDesig(desig)}
                                            >
                                                <Edit2 className="h-4 w-4" />
                                            </Button>
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                className="text-red-600 hover:text-red-700 hover:bg-red-50"
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
            </Card>

            {/* Edit Dialog */}
            <Dialog open={!!editingDesig} onOpenChange={(open) => !open && setEditingDesig(null)}>
                <DialogContent className="max-w-md">
                    {editingDesig && (
                        <form onSubmit={(e) => handleSubmit(e, true)}>
                            <DialogHeader>
                                <DialogTitle>Edit Designation</DialogTitle>
                                <DialogDescription>
                                    Update information for {editingDesig.name}.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="grid gap-2">
                                        <Label htmlFor="edit-name">Name</Label>
                                        <Input id="edit-name" name="name" defaultValue={editingDesig.name} required />
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="edit-code">Code</Label>
                                        <Input id="edit-code" name="code" defaultValue={editingDesig.code} required className="uppercase" />
                                    </div>
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="grid gap-2">
                                        <Label htmlFor="edit-level">Level</Label>
                                        <Input id="edit-level" name="level" type="number" defaultValue={editingDesig.level} required />
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="edit-display_order">Display Order</Label>
                                        <Input id="edit-display_order" name="display_order" type="number" defaultValue={editingDesig.display_order} />
                                    </div>
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-qualification">Min. Qualification</Label>
                                    <Input id="edit-qualification" name="qualification" defaultValue={editingDesig.min_qualification || ''} />
                                </div>
                            </div>
                            <DialogFooter>
                                <Button type="button" variant="outline" onClick={() => setEditingDesig(null)}>
                                    Cancel
                                </Button>
                                <Button type="submit" disabled={updateMutation.isPending}>
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
