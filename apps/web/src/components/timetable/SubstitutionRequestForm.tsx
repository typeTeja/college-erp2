import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { timetableService } from "@/utils/timetable-service";
import { CreateAdjustmentDTO } from "@/types/timetable";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea"; // Assuming this exists, or use Input
import { useToast } from "@/hooks/use-toast";
import { Loader2 } from "lucide-react";

export function SubstitutionRequestForm({ facultyId }: { facultyId: number }) {
    const { toast } = useToast();
    const queryClient = useQueryClient();

    const [selectedEntryId, setSelectedEntryId] = useState<string>("");
    const [date, setDate] = useState<string>("");
    const [reason, setReason] = useState<string>("");

    // Get Faculty's Schedule to populate dropdown
    const { data: schedule, isLoading } = useQuery({
        queryKey: ["faculty-schedule", facultyId],
        queryFn: () => timetableService.getFacultySchedule(facultyId),
    });

    const requestMutation = useMutation({
        mutationFn: timetableService.requestAdjustment,
        onSuccess: () => {
            toast({ title: "Success", description: "Substitution request submitted" });
            resetForm();
        },
        onError: (error: any) => {
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to submit request",
                variant: "destructive"
            });
        }
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedEntryId || !date) {
            toast({ title: "Validation Error", description: "Please select a class and date" });
            return;
        }

        const payload: CreateAdjustmentDTO = {
            timetable_entry_id: parseInt(selectedEntryId),
            date,
            original_faculty_id: facultyId,
            reason,
        };

        requestMutation.mutate(payload);
    };

    const resetForm = () => {
        setSelectedEntryId("");
        setDate("");
        setReason("");
    };

    if (isLoading) return <Loader2 className="animate-spin" />;

    return (
        <Card className="max-w-xl mx-auto">
            <CardHeader>
                <CardTitle>Request Value/Substitution</CardTitle>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="space-y-2">
                        <Label>Select Class to Miss</Label>
                        <Select value={selectedEntryId} onValueChange={setSelectedEntryId}>
                            <SelectTrigger>
                                <SelectValue placeholder="Select a scheduled class" />
                            </SelectTrigger>
                            <SelectContent>
                                {schedule?.map((entry) => (
                                    <SelectItem key={entry.id} value={entry.id.toString()}>
                                        {entry.day_of_week} - {entry.period?.start_time.slice(0, 5)} ({entry.subject_name || `Subject ${entry.subject_id}`})
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="space-y-2">
                        <Label>Date of Absence</Label>
                        <Input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
                    </div>

                    <div className="space-y-2">
                        <Label>Reason (Optional)</Label>
                        {/* Fallback to Input if Textarea is missing, but best practice is Textarea */}
                        <Textarea value={reason} onChange={(e) => setReason(e.target.value)} placeholder="Reason for leave..." />
                    </div>

                    <Button type="submit" className="w-full" disabled={requestMutation.isPending}>
                        {requestMutation.isPending ? "Submitting..." : "Submit Request"}
                    </Button>
                </form>
            </CardContent>
        </Card>
    );
}
