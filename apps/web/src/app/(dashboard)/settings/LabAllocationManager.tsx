import { useState, useEffect } from 'react';
import {
    Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import {
    Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from '@/components/ui/select';
import { useToast } from '@/hooks/use-toast';
import {
    getLabAllocations,
    assignStudentsToLab,
    removeStudentFromLab,
    LabAllocation,
} from '@/utils/master-data-service';
import { BatchSubject } from '@/types/academic-batch';
import { studentService } from '@/utils/student-service';
import { Student } from '@/types/student';
import { Loader2, UserPlus, Trash2, Users } from 'lucide-react';

interface LabAllocationManagerProps {
    open: boolean;
    onClose: () => void;
    labBatch: {
        id: number;
        name: string;
        batch_semester_id: number;
        max_strength: number;
        batch_id: number; // Academic Batch ID
    };
    subjects: BatchSubject[]; // Available subjects for this semester
}

export default function LabAllocationManager({
    open, onClose, labBatch, subjects
}: LabAllocationManagerProps) {
    const { toast } = useToast();
    const [loading, setLoading] = useState(false);
    const [selectedSubject, setSelectedSubject] = useState<string>("");

    const [allStudents, setAllStudents] = useState<Student[]>([]);
    const [allocatedStudents, setAllocatedStudents] = useState<LabAllocation[]>([]);

    const [selectedStudentIds, setSelectedStudentIds] = useState<number[]>([]);

    // Filter out only PRACTICAL subjects
    const practicalSubjects = subjects.filter(s => s.subject_type === 'PRACTICAL');

    useEffect(() => {
        if (open && labBatch) {
            fetchStudents();
            // Reset state
            setSelectedSubject("");
            setAllocatedStudents([]);
            setSelectedStudentIds([]);
        }
    }, [open, labBatch]);

    useEffect(() => {
        if (selectedSubject && labBatch) {
            fetchAllocations();
        } else {
            setAllocatedStudents([]);
        }
    }, [selectedSubject, labBatch]);

    const fetchStudents = async () => {
        try {
            // Fetch students for this semester/batch
            const data = await studentService.getAll({
                batch_semester_id: labBatch.batch_semester_id
            });
            setAllStudents(data);
        } catch (error) {
            console.error("Failed to fetch students", error);
            toast({
                title: "Error",
                description: "Failed to load students",
                variant: "destructive"
            });
        }
    };

    const fetchAllocations = async () => {
        if (!selectedSubject) return;
        setLoading(true);
        try {
            const data = await getLabAllocations(labBatch.id, parseInt(selectedSubject));
            setAllocatedStudents(data);
        } catch (error) {
            console.error("Failed to fetch allocations", error);
        } finally {
            setLoading(false);
        }
    };

    const handleAllocate = async () => {
        if (!selectedSubject || selectedStudentIds.length === 0) return;

        setLoading(true);
        try {
            await assignStudentsToLab({
                student_ids: selectedStudentIds,
                practical_batch_id: labBatch.id,
                subject_id: parseInt(selectedSubject),
                batch_semester_id: labBatch.batch_semester_id
            });

            toast({
                title: "Success",
                description: `Allocated ${selectedStudentIds.length} students to ${labBatch.name}`
            });

            // Refresh
            fetchAllocations();
            setSelectedStudentIds([]);

        } catch (error: any) {
            console.error("Allocation failed", error);
            toast({
                title: "Allocation Failed",
                description: error.response?.data?.detail || "Could not assign students",
                variant: "destructive"
            });
        } finally {
            setLoading(false);
        }
    };

    const handleRemove = async (studentId: number) => {
        if (!confirm("Are you sure you want to remove this student from the lab?")) return;

        try {
            await removeStudentFromLab(studentId, parseInt(selectedSubject));
            toast({ title: "Removed student" });
            fetchAllocations();
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to remove student",
                variant: "destructive"
            });
        }
    };

    // Derived state: Students NOT allocated to THIS batch (can be allocated elsewhere, handled by backend move logic basically)
    // Actually visual helper: Filter out students who are ALREADY in this batch view
    const availableStudents = allStudents.filter(s =>
        !allocatedStudents.some(a => a.student_id === s.id)
    );

    return (
        <Dialog open={open} onOpenChange={onClose}>
            <DialogContent className="max-w-4xl max-h-[90vh] flex flex-col">
                <DialogHeader>
                    <DialogTitle>Manage Lab Allocation: {labBatch.name}</DialogTitle>
                    <DialogDescription>
                        Assign students to this practical batch for specific subjects.
                    </DialogDescription>
                </DialogHeader>

                <div className="flex gap-4 items-center py-4 border-b">
                    <span className="text-sm font-medium">Select Subject:</span>
                    <Select value={selectedSubject} onValueChange={setSelectedSubject}>
                        <SelectTrigger className="w-[300px]">
                            <SelectValue placeholder="Select Practical Subject" />
                        </SelectTrigger>
                        <SelectContent>
                            {practicalSubjects.map(sub => (
                                <SelectItem key={sub.subject_id} value={sub.subject_id.toString()}>
                                    {sub.subject_name} ({sub.subject_code})
                                </SelectItem>
                            ))}
                            {practicalSubjects.length === 0 && (
                                <div className="p-2 text-sm text-gray-500">No practical subjects found</div>
                            )}
                        </SelectContent>
                    </Select>
                </div>

                {!selectedSubject ? (
                    <div className="flex-1 flex items-center justify-center min-h-[300px] text-gray-500">
                        Please select a subject to start allocation
                    </div>
                ) : (
                    <div className="flex-1 grid grid-cols-2 gap-4 min-h-0 overflow-hidden pt-4">
                        {/* LEFT: Available Students */}
                        <Card className="flex flex-col min-h-0">
                            <CardHeader className="py-3 px-4 border-b bg-gray-50/50">
                                <CardTitle className="text-sm font-medium flex justify-between items-center">
                                    <span>Available Students ({availableStudents.length})</span>
                                    {selectedStudentIds.length > 0 && (
                                        <Button size="sm" onClick={handleAllocate} disabled={loading}>
                                            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <UserPlus className="h-4 w-4 mr-2" />}
                                            Add {selectedStudentIds.length}
                                        </Button>
                                    )}
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="flex-1 overflow-auto p-0">
                                <div className="divide-y">
                                    {availableStudents.map(student => (
                                        <div key={student.id} className="flex items-center p-3 hover:bg-gray-50">
                                            <Checkbox
                                                checked={selectedStudentIds.includes(student.id)}
                                                onCheckedChange={(checked) => {
                                                    if (checked) setSelectedStudentIds([...selectedStudentIds, student.id]);
                                                    else setSelectedStudentIds(selectedStudentIds.filter(id => id !== student.id));
                                                }}
                                            />
                                            <div className="ml-3">
                                                <p className="text-sm font-medium">{student.name}</p>
                                                <p className="text-xs text-gray-500">{student.admission_number}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>

                        {/* RIGHT: Allocated Students */}
                        <Card className="flex flex-col min-h-0">
                            <CardHeader className="py-3 px-4 border-b bg-gray-50/50">
                                <CardTitle className="text-sm font-medium flex justify-between items-center">
                                    <span>Allocated ({allocatedStudents.length} / {labBatch.max_strength})</span>
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="flex-1 overflow-auto p-0">
                                {allocatedStudents.length === 0 ? (
                                    <div className="p-8 text-center text-gray-500 text-sm">
                                        No students allocated yet.
                                    </div>
                                ) : (
                                    <div className="divide-y">
                                        {allocatedStudents.map(alloc => (
                                            <div key={alloc.id} className="flex items-center justify-between p-3 hover:bg-gray-50 group">
                                                <div>
                                                    <p className="text-sm font-medium">{alloc.student_name}</p>
                                                    <p className="text-xs text-gray-500">{alloc.admission_number}</p>
                                                </div>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-8 w-8 text-red-500 opacity-0 group-hover:opacity-100"
                                                    onClick={() => handleRemove(alloc.student_id)}
                                                >
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </div>
                )}
            </DialogContent>
        </Dialog>
    );
}
