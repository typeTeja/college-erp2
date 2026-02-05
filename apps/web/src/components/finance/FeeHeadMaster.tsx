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
    Coins, RefreshCw 
} from 'lucide-react';
import { Switch } from '@/components/ui/switch';
import { financeService } from '@/utils/finance-service';
import { FeeHead } from '@/utils/master-data-service';
import { Card } from '@/components/ui/card';

export function FeeHeadMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingHead, setEditingHead] = useState<FeeHead | null>(null);

    const { data: feeHeads = [], isLoading, refetch } = financeService.useFeeHeads();
    const createMutation = financeService.useCreateFeeHead();
    const updateMutation = financeService.useUpdateFeeHead();
    const deleteMutation = financeService.useDeleteFeeHead();

    const filteredHeads = feeHeads.filter(head => 
        head.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        head.code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleCreate = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const data: Partial<FeeHead> = {
            name: formData.get('name') as string,
            code: (formData.get('code') as string).toUpperCase(),
            description: formData.get('description') as string || undefined,
            is_active: formData.get('is_active') === 'on',
            is_refundable: formData.get('is_refundable') === 'on',
            is_recurring: formData.get('is_recurring') === 'on',
            is_mandatory: formData.get('is_mandatory') === 'on',
        };

        await createMutation.mutateAsync(data);
        setIsCreateOpen(false);
    };

    const handleUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!editingHead) return;
        const formData = new FormData(e.currentTarget);
        const data: Partial<FeeHead> = {
            name: formData.get('name') as string,
            code: (formData.get('code') as string).toUpperCase(),
            description: formData.get('description') as string || undefined,
            is_active: formData.get('is_active') === 'on',
            is_refundable: formData.get('is_refundable') === 'on',
            is_recurring: formData.get('is_recurring') === 'on',
            is_mandatory: formData.get('is_mandatory') === 'on',
        };

        await updateMutation.mutateAsync({ id: editingHead.id, data });
        setEditingHead(null);
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Are you sure you want to delete this fee head?')) {
            await deleteMutation.mutateAsync(id);
        }
    };

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center gap-4">
                <div className="relative flex-1 max-w-sm">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                    <Input
                        placeholder="Search fee heads..."
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
                                Add Fee Head
                            </Button>
                        </DialogTrigger>
                        <DialogContent className="max-w-xl">
                            <form onSubmit={handleCreate}>
                                <DialogHeader>
                                    <DialogTitle>Add New Fee Head</DialogTitle>
                                    <DialogDescription>
                                        Create a new fee configuration head (e.g., Tuition Fee, Library Fee).
                                    </DialogDescription>
                                </DialogHeader>
                                <div className="grid gap-6 py-4">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="grid gap-2">
                                            <Label htmlFor="name">Fee Head Name *</Label>
                                            <Input id="name" name="name" placeholder="e.g. Tuition Fee" required />
                                        </div>
                                        <div className="grid gap-2">
                                            <Label htmlFor="code">Code *</Label>
                                            <Input id="code" name="code" placeholder="e.g. TF" required className="uppercase" />
                                        </div>
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="description">Description</Label>
                                        <Input id="description" name="description" placeholder="Description of what this fee covers" />
                                    </div>
                                    
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="flex items-center justify-between rounded-lg border p-3">
                                            <Label htmlFor="is_refundable">Refundable</Label>
                                            <Switch id="is_refundable" name="is_refundable" />
                                        </div>
                                        <div className="flex items-center justify-between rounded-lg border p-3">
                                            <Label htmlFor="is_recurring">Recurring (Yearly)</Label>
                                            <Switch id="is_recurring" name="is_recurring" defaultChecked />
                                        </div>
                                        <div className="flex items-center justify-between rounded-lg border p-3">
                                            <Label htmlFor="is_mandatory">Mandatory</Label>
                                            <Switch id="is_mandatory" name="is_mandatory" defaultChecked />
                                        </div>
                                        <div className="flex items-center justify-between rounded-lg border p-3">
                                            <Label htmlFor="is_active">Active Status</Label>
                                            <Switch id="is_active" name="is_active" defaultChecked />
                                        </div>
                                    </div>
                                </div>
                                <DialogFooter>
                                    <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)}>
                                        Cancel
                                    </Button>
                                    <Button type="submit" disabled={createMutation.isPending}>
                                        {createMutation.isPending ? 'Creating...' : 'Create Fee Head'}
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
                            <TableHead>Fee Head</TableHead>
                            <TableHead>Code</TableHead>
                            <TableHead>Attributes</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={5} className="text-center py-8 text-slate-500">
                                    Loading fee heads...
                                </TableCell>
                            </TableRow>
                        ) : filteredHeads.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={5} className="text-center py-8 text-slate-500">
                                    No fee heads found.
                                </TableCell>
                            </TableRow>
                        ) : (
                            filteredHeads.map((head) => (
                                <TableRow key={head.id}>
                                    <TableCell className="font-medium">
                                        <div className="flex items-center gap-2">
                                            <Coins className="h-4 w-4 text-slate-400" />
                                            {head.name}
                                        </div>
                                        {head.description && (
                                            <p className="text-xs text-slate-500 mt-1">{head.description}</p>
                                        )}
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant="outline" className="font-mono">
                                            {head.code}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex flex-wrap gap-1">
                                            {head.is_mandatory && <Badge variant="secondary" className="text-xs">Mandatory</Badge>}
                                            {head.is_refundable && <Badge variant="secondary" className="text-xs">Refundable</Badge>}
                                            {head.is_recurring && <Badge variant="secondary" className="text-xs">Recurring</Badge>}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant={head.is_active ? "success" : "secondary"}>
                                            {head.is_active ? 'Active' : 'Inactive'}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                onClick={() => setEditingHead(head)}
                                            >
                                                <Edit2 className="h-4 w-4" />
                                            </Button>
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                                onClick={() => handleDelete(head.id)}
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
            <Dialog open={!!editingHead} onOpenChange={(open) => !open && setEditingHead(null)}>
                <DialogContent className="max-w-xl">
                    {editingHead && (
                        <form onSubmit={handleUpdate}>
                            <DialogHeader>
                                <DialogTitle>Edit Fee Head</DialogTitle>
                                <DialogDescription>
                                    Update fee head information for {editingHead.name}.
                                </DialogDescription>
                            </DialogHeader>
                             <div className="grid gap-6 py-4">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="grid gap-2">
                                            <Label htmlFor="edit-name">Fee Head Name *</Label>
                                            <Input id="edit-name" name="name" defaultValue={editingHead.name} required />
                                        </div>
                                        <div className="grid gap-2">
                                            <Label htmlFor="edit-code">Code *</Label>
                                            <Input id="edit-code" name="code" defaultValue={editingHead.code} required className="uppercase" />
                                        </div>
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="edit-description">Description</Label>
                                        <Input id="edit-description" name="description" defaultValue={editingHead.description || ''} />
                                    </div>
                                    
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="flex items-center justify-between rounded-lg border p-3">
                                            <Label htmlFor="edit-is_refundable">Refundable</Label>
                                            <Switch id="edit-is_refundable" name="is_refundable" defaultChecked={editingHead.is_refundable} />
                                        </div>
                                        <div className="flex items-center justify-between rounded-lg border p-3">
                                            <Label htmlFor="edit-is_recurring">Recurring (Yearly)</Label>
                                            <Switch id="edit-is_recurring" name="is_recurring" defaultChecked={editingHead.is_recurring} />
                                        </div>
                                        <div className="flex items-center justify-between rounded-lg border p-3">
                                            <Label htmlFor="edit-is_mandatory">Mandatory</Label>
                                            <Switch id="edit-is_mandatory" name="is_mandatory" defaultChecked={editingHead.is_mandatory} />
                                        </div>
                                        <div className="flex items-center justify-between rounded-lg border p-3">
                                            <Label htmlFor="edit-is_active">Active Status</Label>
                                            <Switch id="edit-is_active" name="is_active" defaultChecked={editingHead.is_active} />
                                        </div>
                                    </div>
                                </div>
                            <DialogFooter>
                                <Button type="button" variant="outline" onClick={() => setEditingHead(null)}>
                                    Cancel
                                </Button>
                                <Button type="submit" disabled={updateMutation.isPending}>
                                    {updateMutation.isPending ? 'Updating...' : 'Update Fee Head'}
                                </Button>
                            </DialogFooter>
                        </form>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    );
}
