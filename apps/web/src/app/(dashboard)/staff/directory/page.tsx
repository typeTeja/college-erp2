"use client";

import { useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { useStaff, useShifts, useCreateStaff, useUpdateStaff, useDeleteStaff } from "@/hooks/use-staff";
import { Staff, StaffCreateDTO } from "@/types/staff";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { staffSchema, StaffFormValues } from "@/schemas/staff-schema";
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

    const form = useForm<StaffFormValues>({
        resolver: zodResolver(staffSchema),
        defaultValues: {
            name: "", email: "", mobile: "", department: "", designation: "", join_date: "", shift_id: undefined
        }
    });

    const { data: staffList, isLoading, error } = useStaff();
    const { data: shifts } = useShifts();

    const createMutation = useCreateStaff();
    const updateMutation = useUpdateStaff();
    const deleteMutation = useDeleteStaff();

    const onSubmit = (data: StaffFormValues) => {
        if (editingId) {
            updateMutation.mutate({ id: editingId, data }, {
                onSuccess: () => {
                    setIsOpen(false);
                    form.reset();
                    setEditingId(null);
                    toast({ title: "Success", description: "Staff profile updated" });
                },
                onError: (err: any) => {
                    toast({ title: "Error", description: "Failed to update staff", variant: "destructive" });
                }
            });
        } else {
            createMutation.mutate(data, {
                onSuccess: () => {
                    setIsOpen(false);
                    form.reset();
                    toast({ title: "Success", description: "Staff member added successfully" });
                },
                onError: (err: any) => {
                    toast({ title: "Error", description: "Failed to add staff", variant: "destructive" });
                }
            });
        }
    };

    const handleEdit = (staff: Staff) => {
        form.reset({
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
        form.reset({
            name: "", email: "", mobile: "", department: "", designation: "", join_date: "", shift_id: undefined
        });
        setEditingId(null);
        setIsOpen(true);
    }

    // Derived state for search filtering
    const filteredStaff = staffList?.filter((s: Staff) =>
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
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 py-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Full Name</Label>
                                    <Input {...form.register("name")} />
                                    {form.formState.errors.name && <p className="text-red-500 text-xs">{form.formState.errors.name.message}</p>}
                                </div>
                                <div className="space-y-2">
                                    <Label>Designation</Label>
                                    <Input {...form.register("designation")} placeholder="e.g. Lab Assistant" />
                                    {form.formState.errors.designation && <p className="text-red-500 text-xs">{form.formState.errors.designation.message}</p>}
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Email</Label>
                                    <Input {...form.register("email")} type="email" />
                                    {form.formState.errors.email && <p className="text-red-500 text-xs">{form.formState.errors.email.message}</p>}
                                </div>
                                <div className="space-y-2">
                                    <Label>Mobile</Label>
                                    <Input {...form.register("mobile")} />
                                    {form.formState.errors.mobile && <p className="text-red-500 text-xs">{form.formState.errors.mobile.message}</p>}
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Department (Optional)</Label>
                                    <Input {...form.register("department")} />
                                </div>
                                <div className="space-y-2">
                                    <Label>Joining Date</Label>
                                    <Input {...form.register("join_date")} type="date" />
                                    {form.formState.errors.join_date && <p className="text-red-500 text-xs">{form.formState.errors.join_date.message}</p>}
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label>Assigned Shift</Label>
                                <select
                                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background disabled:cursor-not-allowed disabled:opacity-50"
                                    {...form.register("shift_id")}
                                >
                                    <option value="">No Shift Assigned</option>
                                    {shifts?.map((s: any) => (
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
