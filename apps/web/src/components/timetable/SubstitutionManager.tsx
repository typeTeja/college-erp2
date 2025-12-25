import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { timetableService } from "@/utils/timetable-service";
import { AdjustmentStatus } from "@/types/timetable";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";
import { Loader2, Check, X } from "lucide-react";
import { useState } from "react";

export function SubstitutionManager() {
    const { toast } = useToast();
    const queryClient = useQueryClient();
    const [substituteId, setSubstituteId] = useState<Record<number, string>>({});

    const { data: adjustments, isLoading } = useQuery({
        queryKey: ["pending-adjustments"],
        queryFn: timetableService.getPendingAdjustments,
    });

    const updateMutation = useMutation({
        mutationFn: ({ id, status, subId }: { id: number, status: AdjustmentStatus, subId?: number }) =>
            timetableService.updateAdjustment(id, status, subId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["pending-adjustments"] });
            toast({ title: "Success", description: "Request updated" });
        },
        onError: () => {
            toast({ title: "Error", description: "Failed to update request", variant: "destructive" });
        }
    });

    const handleAction = (id: number, status: AdjustmentStatus) => {
        const subIdVal = substituteId[id];
        if (status === AdjustmentStatus.APPROVED && !subIdVal) {
            toast({ title: "Required", description: "Please enter a Substitute Faculty ID", variant: "destructive" });
            return;
        }

        updateMutation.mutate({
            id,
            status,
            subId: subIdVal ? parseInt(subIdVal) : undefined
        });
    };

    if (isLoading) return <Loader2 className="animate-spin" />;

    return (
        <Card>
            <CardHeader>
                <CardTitle>Pending Substitution Requests</CardTitle>
            </CardHeader>
            <CardContent>
                {adjustments?.length === 0 ? (
                    <p className="text-center text-muted-foreground py-8">No pending requests.</p>
                ) : (
                    <div className="space-y-4">
                        {adjustments?.map((adj) => (
                            <div key={adj.id} className="flex flex-col md:flex-row items-start md:items-center justify-between p-4 border rounded-lg gap-4">
                                <div className="space-y-1">
                                    <div className="font-semibold flex items-center gap-2">
                                        <span>Original Faculty ID: {adj.original_faculty_id}</span>
                                        <Badge variant="outline">{adj.reason || "No reason provided"}</Badge>
                                    </div>
                                    <div className="text-sm text-muted-foreground">
                                        Date: {adj.date} | Class ID: {adj.timetable_entry_id}
                                    </div>
                                </div>

                                <div className="flex items-center gap-2 w-full md:w-auto">
                                    <Input
                                        placeholder="Sub. Faculty ID"
                                        className="w-32"
                                        value={substituteId[adj.id] || ""}
                                        onChange={(e) => setSubstituteId(prev => ({ ...prev, [adj.id]: e.target.value }))}
                                    />

                                    <Button
                                        size="sm"
                                        className="bg-green-600 hover:bg-green-700"
                                        onClick={() => handleAction(adj.id, AdjustmentStatus.APPROVED)}
                                        disabled={updateMutation.isPending}
                                    >
                                        <Check className="w-4 h-4 mr-1" /> Approve
                                    </Button>

                                    <Button
                                        size="sm"
                                        variant="destructive"
                                        onClick={() => handleAction(adj.id, AdjustmentStatus.REJECTED)}
                                        disabled={updateMutation.isPending}
                                    >
                                        <X className="w-4 h-4 mr-1" /> Reject
                                    </Button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
