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
    Megaphone, RefreshCw 
} from 'lucide-react';
import { admissionService } from '@/utils/admission-service';
import { LeadSource } from '@/utils/master-data-service';
import { Card } from '@/components/ui/card';

export function LeadSourceMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingSource, setEditingSource] = useState<LeadSource | null>(null);

    const { data: sources = [], isLoading, refetch } = admissionService.useLeadSources();
    const createMutation = admissionService.useCreateLeadSource();
    const updateMutation = admissionService.useUpdateLeadSource();
    const deleteMutation = admissionService.useDeleteLeadSource();

    const filteredSources = sources.filter(source => 
        source.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        source.code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleCreate = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const data: Partial<LeadSource> = {
            name: formData.get('name') as string,
            code: (formData.get('code') as string).toUpperCase(),
        };

        await createMutation.mutateAsync(data);
        setIsCreateOpen(false);
    };

    const handleUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!editingSource) return;
        const formData = new FormData(e.currentTarget);
        const data: Partial<LeadSource> = {
            name: formData.get('name') as string,
            code: (formData.get('code') as string).toUpperCase(),
        };

        await updateMutation.mutateAsync({ id: editingSource.id, data });
        setEditingSource(null);
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Are you sure you want to delete this source?')) {
            await deleteMutation.mutateAsync(id);
        }
    };

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center gap-4">
                <div className="relative flex-1 max-w-sm">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                    <Input
                        placeholder="Search sources..."
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
                                Add Source
                            </Button>
                        </DialogTrigger>
                        <DialogContent>
                            <form onSubmit={handleCreate}>
                                <DialogHeader>
                                    <DialogTitle>Add New Lead Source</DialogTitle>
                                    <DialogDescription>
                                        Add admission lead sources (e.g., Website, Referral, Social Media).
                                    </DialogDescription>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div className="grid gap-2">
                                        <Label htmlFor="name">Source Name</Label>
                                        <Input id="name" name="name" placeholder="e.g. Website" required />
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="code">Code</Label>
                                        <Input id="code" name="code" placeholder="e.g. WEB" required className="uppercase" />
                                    </div>
                                </div>
                                <DialogFooter>
                                    <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)}>
                                        Cancel
                                    </Button>
                                    <Button type="submit" disabled={createMutation.isPending}>
                                        {createMutation.isPending ? 'Creating...' : 'Create Source'}
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
                            <TableHead>Source</TableHead>
                            <TableHead>Code</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-8 text-slate-500">
                                    Loading sources...
                                </TableCell>
                            </TableRow>
                        ) : filteredSources.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-8 text-slate-500">
                                    No sources found.
                                </TableCell>
                            </TableRow>
                        ) : (
                            filteredSources.map((source) => (
                                <TableRow key={source.id}>
                                    <TableCell className="font-medium">
                                        <div className="flex items-center gap-2">
                                            <Megaphone className="h-4 w-4 text-slate-400" />
                                            {source.name}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant="outline" className="font-mono">
                                            {source.code}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant={source.is_active ? "success" : "secondary"}>
                                            {source.is_active ? 'Active' : 'Inactive'}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                onClick={() => setEditingSource(source)}
                                            >
                                                <Edit2 className="h-4 w-4" />
                                            </Button>
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                                onClick={() => handleDelete(source.id)}
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
            <Dialog open={!!editingSource} onOpenChange={(open) => !open && setEditingSource(null)}>
                <DialogContent>
                    {editingSource && (
                        <form onSubmit={handleUpdate}>
                            <DialogHeader>
                                <DialogTitle>Edit Source</DialogTitle>
                                <DialogDescription>
                                    Update source information for {editingSource.name}.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-name">Source Name</Label>
                                    <Input id="edit-name" name="name" defaultValue={editingSource.name} required />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-code">Code</Label>
                                    <Input id="edit-code" name="code" defaultValue={editingSource.code} required className="uppercase" />
                                </div>
                            </div>
                            <DialogFooter>
                                <Button type="button" variant="outline" onClick={() => setEditingSource(null)}>
                                    Cancel
                                </Button>
                                <Button type="submit" disabled={updateMutation.isPending}>
                                    {updateMutation.isPending ? 'Updating...' : 'Update Source'}
                                </Button>
                            </DialogFooter>
                        </form>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    );
}
