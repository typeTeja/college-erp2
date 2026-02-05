"use client";

import React, { useState, useEffect } from 'react';
import {
    getScholarshipSlabs,
    createScholarshipSlab,
    updateScholarshipSlab,
    deleteScholarshipSlab,
    ScholarshipSlab
} from '@/utils/scholarship-service';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogFooter
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { Plus, Edit2, Trash2, Search, Loader2 } from 'lucide-react';

export default function ScholarshipSlabTab() {
    const { toast } = useToast();
    const [slabs, setSlabs] = useState<ScholarshipSlab[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [editingSlab, setEditingSlab] = useState<ScholarshipSlab | null>(null);
    const [formData, setFormData] = useState({
        name: '',
        code: '',
        discount_type: 'PERCENTAGE' as 'PERCENTAGE' | 'FIXED',
        discount_value: 0,
        min_percentage: 0,
        max_percentage: 100,
        description: ''
    });

    const fetchSlabs = async () => {
        try {
            setIsLoading(true);
            const data = await getScholarshipSlabs();
            setSlabs(data);
        } catch (error) {
            console.error('Error fetching slabs:', error);
            toast({
                title: 'Error',
                description: 'Failed to fetch scholarship slabs',
                variant: 'destructive',
            });
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchSlabs();
    }, []);

    const handleOpenDialog = (slab: ScholarshipSlab | null = null) => {
        if (slab) {
            setEditingSlab(slab);
            setFormData({
                name: slab.name,
                code: slab.code,
                discount_type: slab.discount_type,
                discount_value: slab.discount_value,
                min_percentage: slab.min_percentage,
                max_percentage: slab.max_percentage,
                description: slab.description || ''
            });
        } else {
            setEditingSlab(null);
            setFormData({
                name: '',
                code: '',
                discount_type: 'PERCENTAGE',
                discount_value: 0,
                min_percentage: 0,
                max_percentage: 100,
                description: ''
            });
        }
        setIsDialogOpen(true);
    };

    const handleSave = async () => {
        try {
            if (editingSlab) {
                await updateScholarshipSlab(editingSlab.id, formData);
                toast({ title: 'Success', description: 'Scholarship slab updated successfully' });
            } else {
                await createScholarshipSlab(formData);
                toast({ title: 'Success', description: 'Scholarship slab created successfully' });
            }
            setIsDialogOpen(false);
            fetchSlabs();
        } catch (error) {
            console.error('Error saving slab:', error);
            toast({
                title: 'Error',
                description: 'Failed to save scholarship slab',
                variant: 'destructive',
            });
        }
    };

    const handleDelete = async (id: number) => {
        if (!confirm('Are you sure you want to delete this slab?')) return;
        try {
            await deleteScholarshipSlab(id);
            toast({ title: 'Success', description: 'Scholarship slab deleted successfully' });
            fetchSlabs();
        } catch (error) {
            console.error('Error deleting slab:', error);
            toast({
                title: 'Error',
                description: 'Failed to delete scholarship slab',
                variant: 'destructive',
            });
        }
    };

    const filteredSlabs = slabs.filter(slab =>
        slab.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        slab.code.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <Card className="border-none shadow-none">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4 px-0">
                <CardTitle className="text-xl font-bold">Scholarship Slabs</CardTitle>
                <div className="flex items-center gap-4">
                    <div className="relative">
                        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Search slabs..."
                            className="pl-8 w-[250px]"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                    <Button onClick={() => handleOpenDialog()} className="bg-primary hover:bg-primary/90">
                        <Plus className="mr-2 h-4 w-4" /> Add Slab
                    </Button>
                </div>
            </CardHeader>
            <CardContent className="px-0">
                {isLoading ? (
                    <div className="flex items-center justify-center p-12">
                        <Loader2 className="h-8 w-8 animate-spin text-primary" />
                    </div>
                ) : (
                    <div className="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Name</TableHead>
                                    <TableHead>Code</TableHead>
                                    <TableHead>Eligibility (%)</TableHead>
                                    <TableHead>Discount</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredSlabs.length === 0 ? (
                                    <TableRow>
                                        <TableCell colSpan={6} className="h-24 text-center">
                                            No scholarship slabs found.
                                        </TableCell>
                                    </TableRow>
                                ) : (
                                    filteredSlabs.map((slab) => (
                                        <TableRow key={slab.id}>
                                            <TableCell className="font-medium">{slab.name}</TableCell>
                                            <TableCell>{slab.code}</TableCell>
                                            <TableCell>
                                                {slab.min_percentage}% - {slab.max_percentage}%
                                            </TableCell>
                                            <TableCell>
                                                {slab.discount_type === 'PERCENTAGE'
                                                    ? `${slab.discount_value}%`
                                                    : `₹${slab.discount_value.toLocaleString()}`
                                                }
                                            </TableCell>
                                            <TableCell>
                                                <Badge variant={slab.is_active ? "default" : "secondary"}>
                                                    {slab.is_active ? 'Active' : 'Inactive'}
                                                </Badge>
                                            </TableCell>
                                            <TableCell className="text-right">
                                                <div className="flex justify-end gap-2">
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        onClick={() => handleOpenDialog(slab)}
                                                    >
                                                        <Edit2 className="h-4 w-4" />
                                                    </Button>
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        className="text-destructive hover:text-destructive"
                                                        onClick={() => handleDelete(slab.id)}
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
                    </div>
                )}
            </CardContent>

            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                <DialogContent className="sm:max-w-[500px]">
                    <DialogHeader>
                        <DialogTitle>{editingSlab ? 'Edit Scholarship Slab' : 'Add Scholarship Slab'}</DialogTitle>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div className="grid gap-2">
                                <Label htmlFor="name">Slab Name</Label>
                                <Input
                                    id="name"
                                    value={formData.name}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    placeholder="e.g. Merit Gold"
                                />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="code">Code</Label>
                                <Input
                                    id="code"
                                    value={formData.code}
                                    onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })}
                                    placeholder="GOLD"
                                />
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="grid gap-2">
                                <Label htmlFor="min">Min Percentage (%)</Label>
                                <Input
                                    id="min"
                                    type="number"
                                    value={formData.min_percentage}
                                    onChange={(e) => setFormData({ ...formData, min_percentage: parseFloat(e.target.value) })}
                                />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="max">Max Percentage (%)</Label>
                                <Input
                                    id="max"
                                    type="number"
                                    value={formData.max_percentage}
                                    onChange={(e) => setFormData({ ...formData, max_percentage: parseFloat(e.target.value) })}
                                />
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="grid gap-2">
                                <Label htmlFor="type">Discount Type</Label>
                                <select
                                    id="type"
                                    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                                    value={formData.discount_type}
                                    onChange={(e) => setFormData({ ...formData, discount_type: e.target.value as any })}
                                >
                                    <option value="PERCENTAGE">Percentage (%)</option>
                                    <option value="FIXED">Fixed Amount (₹)</option>
                                </select>
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="value">Discount Value</Label>
                                <Input
                                    id="value"
                                    type="number"
                                    value={formData.discount_value}
                                    onChange={(e) => setFormData({ ...formData, discount_value: parseFloat(e.target.value) })}
                                />
                            </div>
                        </div>
                        <div className="grid gap-2">
                            <Label htmlFor="desc">Description</Label>
                            <Input
                                id="desc"
                                value={formData.description}
                                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
                        <Button onClick={handleSave}>Save Slab</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </Card>
    );
}
