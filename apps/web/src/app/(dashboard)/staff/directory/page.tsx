"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { staffService } from "@/utils/staff-service";
import { Staff, StaffCreateDTO } from "@/types/staff";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast"; // Fixed import path
import { Plus, Search, Trash2, Edit } from "lucide-react";

export default function StaffDirectoryPage() {
    const { toast } = useToast();
    const queryClient = useQueryClient();
    const [search, setSearch] = useState("");
    const [isOpen, setIsOpen] = useState(false);
    const [editingId, setEditingId] = useState<number | null>(null);

    // Form State
    const [formData, setFormData] = useState<StaffCreateDTO>({
        name: "", email: "", mobile: "", department: "", designation: "", join_date: "", shift_id: undefined
    });

    const { data: staffList, isLoading } = useQuery({
        queryKey: ["staff"],
        queryFn: () => staffService.getAll(),
    });

    const { data: shifts } = useQuery({
        queryKey: ["shifts"],
        queryFn: staffService.getShifts,
    });

    const createMutation = useMutation({
        mutationFn: staffService.create,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["staff"] });
            setIsOpen(false);
            resetForm();
            toast({ title: "Success", description: "Staff member added successfully" });
        },
        onError: (err: any) => {
            toast({ title: "Error", description: err.response?.data?.detail || "Failed to add staff", variant: "destructive" });
        }
    });

    const updateMutation = useMutation({
        mutationFn: ({ id, data }: { id: number, data: any }) => staffService.update(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["staff"] });
            setIsOpen(false);
            resetForm();
            toast({ title: "Success", description: "Staff profile updated" });
        },
        onError: (err: any) => {
            toast({ title: "Error", description: err.response?.data?.detail || "Failed to update staff", variant: "destructive" });
        }
    });

    const deleteMutation = useMutation({
        mutationFn: staffService.delete,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["staff"] });
            toast({ title: "Deleted", description: "Staff member deactivated" });
        }
    });

    const resetForm = () => {
        setFormData({ name: "", email: "", mobile: "", department: "", designation: "", join_date: "", shift_id: undefined });
        setEditingId(null);
    }

    const handleEdit = (staff: Staff) => {
        setFormData({
            name: staff.name,
            email: staff.email,
            mobile: staff.mobile,
            department: staff.department || "",
            designation: staff.designation,
            join_date: staff.join_date,
            shift_id: staff.shift_id
        });
        setEditingId(staff.id);
        setIsOpen(true);
    };

    const handleAdd = () => {
        resetForm();
        setIsOpen(true);
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (editingId) {
            updateMutation.mutate({ id: editingId, data: formData });
        } else {
            createMutation.mutate(formData);
        }
    };

    const filteredStaff = staffList?.filter(s =>
        s.name.toLowerCase().includes(search.toLowerCase()) ||
        s.email.toLowerCase().includes(search.toLowerCase()) ||
        s.designation.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Staff Directory</h1>
                    <p className="text-muted-foreground">Manage non-teaching staff profiles.</p>
                </div>
                <Dialog open={isOpen} onOpenChange={setIsOpen}>
                    <DialogTrigger asChild>
                        <Button onClick={handleAdd}><Plus className="mr-2 h-4 w-4" /> Add Staff</Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[500px]">
                        <DialogHeader>
                            <DialogTitle>{editingId ? "Edit Staff Profile" : "Add New Staff Member"}</DialogTitle>
                        </DialogHeader>
                        <form onSubmit={handleSubmit} className="space-y-4 py-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Full Name</Label>
                                    <Input required value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} />
                                </div>
                                <div className="space-y-2">
                                    <Label>Designation</Label>
                                    <Input required placeholder="e.g. Lab Assistant" value={formData.designation} onChange={e => setFormData({ ...formData, designation: e.target.value })} />
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Email</Label>
                                    <Input required type="email" value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} />
                                </div>
                                <div className="space-y-2">
                                    <Label>Mobile</Label>
                                    <Input required value={formData.mobile} onChange={e => setFormData({ ...formData, mobile: e.target.value })} />
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Department (Optional)</Label>
                                    <Input value={formData.department} onChange={e => setFormData({ ...formData, department: e.target.value })} />
                                </div>
                                <div className="space-y-2">
                                    <Label>Joining Date</Label>
                                    <Input required type="date" value={formData.join_date} onChange={e => setFormData({ ...formData, join_date: e.target.value })} />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label>Assigned Shift</Label>
                                <select
                                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    value={formData.shift_id || ""}
                                    onChange={(e) => setFormData({ ...formData, shift_id: e.target.value ? parseInt(e.target.value) : undefined })}
                                >
                                    <option value="">No Shift Assigned</option>
                                    {shifts?.map(s => (
                                        <option key={s.id} value={s.id}>{s.name} ({s.start_time.slice(0, 5)} - {s.end_time.slice(0, 5)})</option>
                                    ))}
                                </select>
                            </div>

                            <Button type="submit" className="w-full" disabled={createMutation.isPending || updateMutation.isPending}>
                                {editingId ? "Update Profile" : "Create Staff Profile"}
                            </Button>
                        </form>
                    </DialogContent>
                </Dialog>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center gap-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search by name, email or role..."
                                className="pl-8 max-w-sm"
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                            />
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Role</TableHead>
                                <TableHead>Department</TableHead>
                                <TableHead>Shift</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {isLoading ? (
                                <TableRow>
                                    <TableCell colSpan={6} className="text-center h-24">Loading...</TableCell>
                                </TableRow>
                            ) : filteredStaff?.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={6} className="text-center h-24 text-muted-foreground">No staff found.</TableCell>
                                </TableRow>
                            ) : (
                                filteredStaff?.map((staff) => (
                                    <TableRow key={staff.id}>
                                        <TableCell className="font-medium">{staff.name}</TableCell>
                                        <TableCell>{staff.designation}</TableCell>
                                        <TableCell>{staff.department || "-"}</TableCell>
                                        <TableCell>
                                            {shifts?.find(s => s.id === staff.shift_id)?.name || <span className="text-muted-foreground italic">None</span>}
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant={staff.is_active ? "default" : "secondary"}>
                                                {staff.is_active ? "Active" : "Inactive"}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right flex justify-end gap-2">
                                            <Button variant="outline" size="sm" className="h-8 w-8 p-0" onClick={() => handleEdit(staff)}>
                                                <Edit className="h-4 w-4" />
                                            </Button>
                                            <Button variant="outline" size="icon" onClick={() => deleteMutation.mutate(staff.id)}>
                                                <Trash2 className="h-4 w-4 text-red-500" />
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
