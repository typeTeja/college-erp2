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
    Plus, Search, Edit2, Trash2, 
    Building2, RefreshCw 
} from 'lucide-react';
import { institutionalService } from '@/utils/institutional-service';
import { Department, DepartmentCreateData } from '@/types/institutional';
import { Card, CardContent } from '@/components/ui/card';

export function DepartmentMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingDept, setEditingDept] = useState<Department | null>(null);

    const { data: departments = [], isLoading, refetch } = institutionalService.useDepartments();
    const createMutation = institutionalService.useCreateDepartment();
    const updateMutation = institutionalService.useUpdateDepartment();
    const deleteMutation = institutionalService.useDeleteDepartment();

    const filteredDepartments = departments.filter(dept => 
        dept.department_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        dept.department_code?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleCreate = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const data: DepartmentCreateData = {
            department_name: formData.get('department_name') as string,
            department_code: (formData.get('department_code') as string).toUpperCase(),
            description: formData.get('description') as string || undefined,
        };

        await createMutation.mutateAsync(data);
        setIsCreateOpen(false);
    };

    const handleUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!editingDept) return;
        const formData = new FormData(e.currentTarget);
        const data: Partial<DepartmentCreateData> = {
            department_name: formData.get('department_name') as string,
            department_code: (formData.get('department_code') as string).toUpperCase(),
            description: formData.get('description') as string || undefined,
        };

        await updateMutation.mutateAsync({ id: editingDept.id, data });
        setEditingDept(null);
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Are you sure you want to delete this department?')) {
            await deleteMutation.mutateAsync(id);
        }
    };

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center gap-4">
                <div className="relative flex-1 max-w-sm">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                    <Input
                        placeholder="Search departments..."
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
                                Add Department
                            </Button>
                        </DialogTrigger>
                        <DialogContent>
                            <form onSubmit={handleCreate}>
                                <DialogHeader>
                                    <DialogTitle>Add New Department</DialogTitle>
                                    <DialogDescription>
                                        Create a new academic or functional department.
                                    </DialogDescription>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div className="grid gap-2">
                                        <Label htmlFor="department_name">Department Name</Label>
                                        <Input id="department_name" name="department_name" placeholder="e.g. Computer Science & Engineering" required />
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="department_code">Department Code</Label>
                                        <Input id="department_code" name="department_code" placeholder="e.g. CSE" required className="uppercase" />
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="description">Description (Optional)</Label>
                                        <Input id="description" name="description" placeholder="Department description..." />
                                    </div>
                                </div>
                                <DialogFooter>
                                    <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)}>
                                        Cancel
                                    </Button>
                                    <Button type="submit" disabled={createMutation.isPending}>
                                        {createMutation.isPending ? 'Creating...' : 'Create Department'}
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
                            <TableHead>Department</TableHead>
                            <TableHead>Code</TableHead>
                            <TableHead>Description</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={5} className="text-center py-8 text-slate-500">
                                    Loading departments...
                                </TableCell>
                            </TableRow>
                        ) : filteredDepartments.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={5} className="text-center py-8 text-slate-500">
                                    No departments found.
                                </TableCell>
                            </TableRow>
                        ) : (
                            filteredDepartments.map((dept) => (
                                <TableRow key={dept.id}>
                                    <TableCell className="font-medium">
                                        <div className="flex items-center gap-2">
                                            <Building2 className="h-4 w-4 text-slate-400" />
                                            {dept.department_name}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant="outline" className="font-mono">
                                            {dept.department_code}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>{dept.description || '-'}</TableCell>
                                    <TableCell>
                                        <Badge variant={dept.is_active ? "success" : "secondary"}>
                                            {dept.is_active ? 'Active' : 'Inactive'}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                onClick={() => setEditingDept(dept)}
                                            >
                                                <Edit2 className="h-4 w-4" />
                                            </Button>
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                                onClick={() => handleDelete(dept.id)}
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
            <Dialog open={!!editingDept} onOpenChange={(open) => !open && setEditingDept(null)}>
                <DialogContent>
                    {editingDept && (
                        <form onSubmit={handleUpdate}>
                            <DialogHeader>
                                <DialogTitle>Edit Department</DialogTitle>
                                <DialogDescription>
                                    Update department information for {editingDept.department_name}.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-department_name">Department Name</Label>
                                    <Input id="edit-department_name" name="department_name" defaultValue={editingDept.department_name} required />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-department_code">Department Code</Label>
                                    <Input id="edit-department_code" name="department_code" defaultValue={editingDept.department_code} required className="uppercase" />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-description">Description</Label>
                                    <Input id="edit-description" name="description" defaultValue={editingDept.description || ''} />
                                </div>
                            </div>
                            <DialogFooter>
                                <Button type="button" variant="outline" onClick={() => setEditingDept(null)}>
                                    Cancel
                                </Button>
                                <Button type="submit" disabled={updateMutation.isPending}>
                                    {updateMutation.isPending ? 'Updating...' : 'Update Department'}
                                </Button>
                            </DialogFooter>
                        </form>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    );
}
