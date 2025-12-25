"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { staffService } from "@/utils/staff-service";
import { Shift } from "@/types/staff";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { useToast } from "@/hooks/use-toast";
import { Loader2, Plus, Clock } from "lucide-react";
import { api } from "@/utils/api";

export default function ShiftManagementPage() {
    const { toast } = useToast();
    const queryClient = useQueryClient();
    const [isOpen, setIsOpen] = useState(false);

    const [formData, setFormData] = useState({
        name: "", start_time: "", end_time: "", description: ""
    });

    const { data: shifts, isLoading } = useQuery({
        queryKey: ["shifts"],
        queryFn: staffService.getShifts,
    });

    const createMutation = useMutation({
        mutationFn: async (data: any) => {
            // Append seconds if missing, as Time field expects HH:MM:SS
            const payload = {
                ...data,
                start_time: data.start_time.length === 5 ? data.start_time + ":00" : data.start_time,
                end_time: data.end_time.length === 5 ? data.end_time + ":00" : data.end_time,
            };
            const res = await api.post("/operations/shifts", payload);
            return res.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["shifts"] });
            setIsOpen(false);
            setFormData({ name: "", start_time: "", end_time: "", description: "" });
            toast({ title: "Shift Created", description: "New shift added to system." });
        }
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        createMutation.mutate(formData);
    };

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Shift Management</h1>
                    <p className="text-muted-foreground">Define work shifts for staff members.</p>
                </div>
                <Dialog open={isOpen} onOpenChange={setIsOpen}>
                    <DialogTrigger asChild>
                        <Button><Plus className="mr-2 h-4 w-4" /> Create Shift</Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Add New Shift</DialogTitle>
                        </DialogHeader>
                        <form onSubmit={handleSubmit} className="space-y-4 py-4">
                            <div className="space-y-2">
                                <Label>Shift Name</Label>
                                <Input required placeholder="e.g. Morning Shift" value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Start Time</Label>
                                    <Input required type="time" value={formData.start_time} onChange={e => setFormData({ ...formData, start_time: e.target.value })} />
                                </div>
                                <div className="space-y-2">
                                    <Label>End Time</Label>
                                    <Input required type="time" value={formData.end_time} onChange={e => setFormData({ ...formData, end_time: e.target.value })} />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <Label>Description (Optional)</Label>
                                <Input value={formData.description} onChange={e => setFormData({ ...formData, description: e.target.value })} />
                            </div>
                            <Button type="submit" className="w-full" disabled={createMutation.isPending}>
                                {createMutation.isPending ? "Creating..." : "Save Shift"}
                            </Button>
                        </form>
                    </DialogContent>
                </Dialog>
            </div>

            {isLoading ? <Loader2 className="animate-spin" /> : (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {shifts?.map((shift) => (
                        <Card key={shift.id}>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">
                                    {shift.name}
                                </CardTitle>
                                <Clock className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">
                                    {shift.start_time.slice(0, 5)} - {shift.end_time.slice(0, 5)}
                                </div>
                                <p className="text-xs text-muted-foreground mt-1">
                                    {shift.description || "Standard shift"}
                                </p>
                            </CardContent>
                        </Card>
                    ))}
                    {shifts?.length === 0 && <div className="text-muted-foreground col-span-full text-center py-10">No shifts defined.</div>}
                </div>
            )}
        </div>
    );
}
