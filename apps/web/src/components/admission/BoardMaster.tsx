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
    GraduationCap, RefreshCw 
} from 'lucide-react';
import { admissionService } from '@/utils/admission-service';
import { Board } from '@/utils/master-data-service';
import { Card } from '@/components/ui/card';

export function BoardMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingBoard, setEditingBoard] = useState<Board | null>(null);

    const { data: boards = [], isLoading, refetch } = admissionService.useBoards();
    const createMutation = admissionService.useCreateBoard();
    const updateMutation = admissionService.useUpdateBoard();
    const deleteMutation = admissionService.useDeleteBoard();

    const filteredBoards = boards.filter(board => 
        board.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        board.code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleCreate = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const data: Partial<Board> = {
            name: formData.get('name') as string,
            code: (formData.get('code') as string).toUpperCase(),
        };

        await createMutation.mutateAsync(data);
        setIsCreateOpen(false);
    };

    const handleUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!editingBoard) return;
        const formData = new FormData(e.currentTarget);
        const data: Partial<Board> = {
            name: formData.get('name') as string,
            code: (formData.get('code') as string).toUpperCase(),
        };

        await updateMutation.mutateAsync({ id: editingBoard.id, data });
        setEditingBoard(null);
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Are you sure you want to delete this board?')) {
            await deleteMutation.mutateAsync(id);
        }
    };

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center gap-4">
                <div className="relative flex-1 max-w-sm">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                    <Input
                        placeholder="Search boards..."
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
                                Add Board
                            </Button>
                        </DialogTrigger>
                        <DialogContent>
                            <form onSubmit={handleCreate}>
                                <DialogHeader>
                                    <DialogTitle>Add New Education Board</DialogTitle>
                                    <DialogDescription>
                                        Add education boards (e.g., CBSE, ICSE, SSC).
                                    </DialogDescription>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div className="grid gap-2">
                                        <Label htmlFor="name">Board Name</Label>
                                        <Input id="name" name="name" placeholder="e.g. Central Board of Secondary Education" required />
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="code">Code</Label>
                                        <Input id="code" name="code" placeholder="e.g. CBSE" required className="uppercase" />
                                    </div>
                                </div>
                                <DialogFooter>
                                    <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)}>
                                        Cancel
                                    </Button>
                                    <Button type="submit" disabled={createMutation.isPending}>
                                        {createMutation.isPending ? 'Creating...' : 'Create Board'}
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
                            <TableHead>Board</TableHead>
                            <TableHead>Code</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-8 text-slate-500">
                                    Loading boards...
                                </TableCell>
                            </TableRow>
                        ) : filteredBoards.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-8 text-slate-500">
                                    No boards found.
                                </TableCell>
                            </TableRow>
                        ) : (
                            filteredBoards.map((board) => (
                                <TableRow key={board.id}>
                                    <TableCell className="font-medium">
                                        <div className="flex items-center gap-2">
                                            <GraduationCap className="h-4 w-4 text-slate-400" />
                                            {board.name}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant="outline" className="font-mono">
                                            {board.code}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant={board.is_active ? "success" : "secondary"}>
                                            {board.is_active ? 'Active' : 'Inactive'}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                onClick={() => setEditingBoard(board)}
                                            >
                                                <Edit2 className="h-4 w-4" />
                                            </Button>
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                                onClick={() => handleDelete(board.id)}
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
            <Dialog open={!!editingBoard} onOpenChange={(open) => !open && setEditingBoard(null)}>
                <DialogContent>
                    {editingBoard && (
                        <form onSubmit={handleUpdate}>
                            <DialogHeader>
                                <DialogTitle>Edit Board</DialogTitle>
                                <DialogDescription>
                                    Update board information for {editingBoard.name}.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-name">Board Name</Label>
                                    <Input id="edit-name" name="name" defaultValue={editingBoard.name} required />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="edit-code">Code</Label>
                                    <Input id="edit-code" name="code" defaultValue={editingBoard.code} required className="uppercase" />
                                </div>
                            </div>
                            <DialogFooter>
                                <Button type="button" variant="outline" onClick={() => setEditingBoard(null)}>
                                    Cancel
                                </Button>
                                <Button type="submit" disabled={updateMutation.isPending}>
                                    {updateMutation.isPending ? 'Updating...' : 'Update Board'}
                                </Button>
                            </DialogFooter>
                        </form>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    );
}
