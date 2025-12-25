"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { staffService } from "@/utils/staff-service";
import { MaintenanceTicket, TicketStatus, TicketPriority, MaintenanceTicketCreateDTO } from "@/types/staff";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Loader2, AlertTriangle, CheckCircle, Clock } from "lucide-react";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";

export default function MaintenanceTicketsPage() {
    const { toast } = useToast();
    const queryClient = useQueryClient();
    const [isOpen, setIsOpen] = useState(false);
    const [statusFilter, setStatusFilter] = useState<string>("ALL");

    const [formData, setFormData] = useState<MaintenanceTicketCreateDTO>({
        title: "", description: "", location: "", priority: TicketPriority.MEDIUM
    });

    const { data: tickets, isLoading } = useQuery({
        queryKey: ["tickets", statusFilter],
        queryFn: () => staffService.getTickets(statusFilter === "ALL" ? undefined : statusFilter),
    });

    const createMutation = useMutation({
        mutationFn: staffService.createTicket,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["tickets"] });
            setIsOpen(false);
            setFormData({ title: "", description: "", location: "", priority: TicketPriority.MEDIUM });
            toast({ title: "Ticket Created", description: "Maintenance team notified." });
        }
    });

    const updateStatusMutation = useMutation({
        mutationFn: ({ id, status }: { id: number, status: string }) => staffService.updateTicket(id, status),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["tickets"] });
            toast({ title: "Updated", description: "Ticket status updated." });
        }
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        createMutation.mutate(formData);
    };

    const getStatusColor = (status: TicketStatus) => {
        switch (status) {
            case TicketStatus.OPEN: return "bg-red-100 text-red-800 hover:bg-red-100";
            case TicketStatus.IN_PROGRESS: return "bg-yellow-100 text-yellow-800 hover:bg-yellow-100";
            case TicketStatus.RESOLVED: return "bg-green-100 text-green-800 hover:bg-green-100";
            default: return "bg-gray-100 text-gray-800";
        }
    };

    const getPriorityIcon = (priority: TicketPriority) => {
        if (priority === TicketPriority.HIGH || priority === TicketPriority.CRITICAL)
            return <AlertTriangle className="h-4 w-4 text-red-500" />;
        return <Clock className="h-4 w-4 text-blue-500" />;
    };

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-start">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Maintenance Helpdesk</h1>
                    <p className="text-muted-foreground">Report and track facility issues.</p>
                </div>
                <Dialog open={isOpen} onOpenChange={setIsOpen}>
                    <DialogTrigger asChild>
                        <Button variant="danger"><AlertTriangle className="mr-2 h-4 w-4" /> Report Issue</Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Report Maintenance Issue</DialogTitle>
                        </DialogHeader>
                        <form onSubmit={handleSubmit} className="space-y-4 py-4">
                            <div className="space-y-2">
                                <Label>Issue Title</Label>
                                <Input required placeholder="e.g. Broken Fan" value={formData.title} onChange={e => setFormData({ ...formData, title: e.target.value })} />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Location</Label>
                                    <Input required placeholder="Room No / Area" value={formData.location} onChange={e => setFormData({ ...formData, location: e.target.value })} />
                                </div>
                                <div className="space-y-2">
                                    <Label>Priority</Label>
                                    <Select value={formData.priority} onValueChange={(val: any) => setFormData({ ...formData, priority: val })}>
                                        <SelectTrigger>
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value={TicketPriority.LOW}>Low</SelectItem>
                                            <SelectItem value={TicketPriority.MEDIUM}>Medium</SelectItem>
                                            <SelectItem value={TicketPriority.HIGH}>High</SelectItem>
                                            <SelectItem value={TicketPriority.CRITICAL}>Critical</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>
                            <div className="space-y-2">
                                <Label>Description</Label>
                                <Textarea placeholder="Details..." value={formData.description} onChange={e => setFormData({ ...formData, description: e.target.value })} />
                            </div>
                            <Button type="submit" className="w-full" disabled={createMutation.isPending}>Submit Ticket</Button>
                        </form>
                    </DialogContent>
                </Dialog>
            </div>

            <div className="flex gap-2 pb-4 overflow-x-auto">
                {["ALL", "OPEN", "IN_PROGRESS", "RESOLVED"].map(status => (
                    <Button
                        key={status}
                        variant={statusFilter === status ? "primary" : "outline"}
                        size="sm"
                        onClick={() => setStatusFilter(status)}
                    >
                        {status.replace("_", " ")}
                    </Button>
                ))}
            </div>

            {isLoading ? <Loader2 className="animate-spin" /> : (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {tickets?.map((ticket: MaintenanceTicket) => (
                        <Card key={ticket.id} className="relative">
                            <CardHeader className="pb-2">
                                <div className="flex justify-between items-start">
                                    <Badge className={`${getStatusColor(ticket.status)} border-0`}>
                                        {ticket.status.replace("_", " ")}
                                    </Badge>
                                    {getPriorityIcon(ticket.priority)}
                                </div>
                                <CardTitle className="text-lg mt-2">{ticket.title}</CardTitle>
                                <CardDescription>{ticket.location}</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm text-gray-600 mb-4 line-clamp-2">{ticket.description || "No details provided."}</p>
                                <div className="flex justify-between items-center text-xs text-muted-foreground border-t pt-3">
                                    <span>{new Date(ticket.created_at).toLocaleDateString()}</span>
                                    {ticket.status === TicketStatus.OPEN && (
                                        <Button
                                            size="sm" variant="outline" className="h-7"
                                            onClick={() => updateStatusMutation.mutate({ id: ticket.id, status: TicketStatus.IN_PROGRESS })}
                                        >
                                            Mark In-Progress
                                        </Button>
                                    )}
                                    {ticket.status === TicketStatus.IN_PROGRESS && (
                                        <Button
                                            size="sm" variant="outline" className="h-7 text-green-600 hover:text-green-700"
                                            onClick={() => updateStatusMutation.mutate({ id: ticket.id, status: TicketStatus.RESOLVED })}
                                        >
                                            Resolve
                                        </Button>
                                    )}
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                    {tickets?.length === 0 && <div className="text-muted-foreground col-span-full text-center py-10">No tickets found.</div>}
                </div>
            )}
        </div>
    );
}
