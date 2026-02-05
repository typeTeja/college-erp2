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
    Users, RefreshCw 
} from 'lucide-react';
import { admissionService } from '@/utils/admission-service';
import { ReservationCategory } from '@/utils/master-data-service';
import { Card } from '@/components/ui/card';

export function ReservationCategoryMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingCategory, setEditingCategory] = useState<ReservationCategory | null>(null);

    const { data: categories = [], isLoading, refetch } = admissionService.useReservationCategories();
    const createMutation = admissionService.useCreateReservationCategory();
    const updateMutation = admissionService.useUpdateReservationCategory();
    const deleteMutation = admissionService.useDeleteReservationCategory();

    const filteredCategories = categories.filter(cat => 
        cat.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        cat.code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleCreate = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const data: Partial<ReservationCategory> = {
            name: formData.get('name') as string,
            code: (formData.get('code') as string).toUpperCase(),
            description: formData.get('description') as string || undefined,
        };

        await createMutation.mutateAsync(data);
        setIsCreateOpen(false);
    };

    const handleUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!editingCategory) return;
        const formData = new FormData(e.currentTarget);
        const data: Partial<ReservationCategory> = {
            name: formData.get('name') as string,
            code: (formData.get('code') as string).toUpperCase(),
            description: formData.get('description') as string || undefined,
        };

        await updateMutation.mutateAsync({ id: editingCategory.id, data });
        setEditingCategory(null);
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Are you sure you want to delete this category?')) {
            await deleteMutation.mutateAsync(id);
        }
    };

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center gap-4">
                <div className="relative flex-1 max-w-sm">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                    <Input
                        placeholder="Search categories..."
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
                                Add Category
                            </Button>
                        </DialogTrigger>
                        <DialogContent>
                            <form onSubmit={handleCreate}>
                                <DialogHeader>
                                    <DialogTitle>Add New Reservation Category</DialogTitle>
                                    <DialogDescription>
                                        Add social reservation categories (e.g., General, SC, ST, OBC).
                                    </DialogDescription>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div className="grid gap-2">
                                        <Label htmlFor="name">Category Name</Label>
                                        <Input id="name" name="name" placeholder="e.g. Scheduled Caste" required />
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="code">Code</Label>
                                        <Input id="code" name="code" placeholder="e.g. SC" required className="uppercase" />
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="description">Description</Label>
                                        <Input id="description" name="description" placeholder="Optional description" />
                                    </div>
                                </div>
                                <DialogFooter>
                                    <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)}>
                                        Cancel
                                    </Button>
                                    <Button type="submit" disabled={createMutation.isPending}>
                                        {createMutation.isPending ? 'Creating...' : 'Create Category'}
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
                            <TableHead>Category</TableHead>
                            <TableHead>Code</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-8 text-slate-500">
                                    Loading categories...
                                </TableCell>
                            </TableRow>
                        ) : filteredCategories.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-8 text-slate-500">
                                    No categories found.
                                </TableCell>
                            </TableRow>
                        ) : (
                            filteredCategories.map((cat) => (
                                <TableRow key={cat.id}>
                                    <TableCell className="font-medium">
                                        <div className="flex items-center gap-2">
                                            <Users className="h-4 w-4 text-slate-400" />
                                            {cat.name}
                                        </div>
                                        {cat.description && (
                                            <p className="text-xs text-slate-500 mt-1">{cat.description}</p>
                                        )}
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant="outline" className="font-mono">
                                            {cat.code}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant={cat.is_active ? "success" : "secondary"}>
                                            {cat.is_active ? 'Active' : 'Inactive'}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                onClick={() => setEditingCategory(cat)}
                                            >
                                                <Edit2 className="h-4 w-4" />
                                            </Button>
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                                onClick={() => handleDelete(cat.id)}
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
            <Dialog open={!!editingCategory} onOpenChange={(open) => !open && setEditingCategory(null)}>
                <DialogContent>
                    {editingCategory && (
                        <form onSubmit={handleUpdate}>
                            <DialogHeader>
                                <DialogTitle>Edit Category</DialogTitle>
                                <DialogDescription>
                                    Update category information for {editingCategory.name}.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-name">Category Name</Label>
                                    <Input id="edit-name" name="name" defaultValue={editingCategory.name} required />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-code">Code</Label>
                                    <Input id="edit-code" name="code" defaultValue={editingCategory.code} required className="uppercase" />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-description">Description</Label>
                                    <Input id="edit-description" name="description" defaultValue={editingCategory.description || ''} />
                                </div>
                            </div>
                            <DialogFooter>
                                <Button type="button" variant="outline" onClick={() => setEditingCategory(null)}>
                                    Cancel
                                </Button>
                                <Button type="submit" disabled={updateMutation.isPending}>
                                    {updateMutation.isPending ? 'Updating...' : 'Update Category'}
                                </Button>
                            </DialogFooter>
                        </form>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    );
}
