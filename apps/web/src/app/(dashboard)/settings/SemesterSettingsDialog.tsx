import React, { useState, useEffect } from 'react';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogDescription
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { updateBatchSemester } from '@/utils/master-data-service';
import { toast } from 'sonner';

interface SemesterSettingsDialogProps {
    open: boolean;
    onClose: () => void;
    batchId: number;
    semesterId: number;
    semesterName: string;
    currentStartDate?: string;
    currentEndDate?: string;
    currentIsActive?: boolean;
    onUpdate: () => void; // Callback to reload structure
}

export function SemesterSettingsDialog({
    open,
    onClose,
    batchId,
    semesterId,
    semesterName,
    currentStartDate,
    currentEndDate,
    currentIsActive,
    onUpdate
}: SemesterSettingsDialogProps) {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [isActive, setIsActive] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (open) {
            setStartDate(currentStartDate || '');
            setEndDate(currentEndDate || '');
            setIsActive(currentIsActive || false);
        }
    }, [open, currentStartDate, currentEndDate, currentIsActive]);

    const handleSave = async () => {
        setLoading(true);
        try {
            await updateBatchSemester(batchId, semesterId, {
                start_date: startDate || undefined, // Send undefined if empty to nullify or keep as is? Backend expects date or None
                end_date: endDate || undefined,
                is_active: isActive
            });
            toast.success("Semester settings updated");
            onUpdate();
            onClose();
        } catch (error: any) {
            console.error(error);
            toast.error(error.response?.data?.detail || "Failed to update semester");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Edit {semesterName}</DialogTitle>
                    <DialogDescription>
                        Set the academic calendar dates for this semester.
                    </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <div className="flex items-center space-x-2">
                        <Switch id="is-active" checked={isActive} onCheckedChange={setIsActive} />
                        <Label htmlFor="is-active">Active Semester</Label>
                    </div>
                    <p className="text-xs text-muted-foreground">
                        Marking as active indicates this is the current semester for this batch.
                    </p>

                    <div className="grid gap-2">
                        <Label htmlFor="start-date">Opening Date</Label>
                        <Input
                            id="start-date"
                            type="date"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="end-date">Closing Date</Label>
                        <Input
                            id="end-date"
                            type="date"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                        />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" onClick={onClose} disabled={loading}>
                        Cancel
                    </Button>
                    <Button onClick={handleSave} disabled={loading}>
                        {loading ? 'Saving...' : 'Save Changes'}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
