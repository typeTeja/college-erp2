import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { timetableService } from "@/utils/timetable-service";
import { DayOfWeek, ClassSchedule, CreateScheduleDTO } from "@/types/timetable";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";

const DAYS = Object.values(DayOfWeek);

export function TimetableBuilder() {
    const { toast } = useToast();
    const queryClient = useQueryClient();

    // Selection State
    const [academicYearId, setAcademicYearId] = useState<number>(1); // Default to current
    const [semesterId, setSemesterId] = useState<number>(1);
    const [sectionId, setSectionId] = useState<number | undefined>(undefined);

    // Modal State
    const [selectedDay, setSelectedDay] = useState<DayOfWeek | null>(null);
    const [selectedPeriod, setSelectedPeriod] = useState<number | null>(null);
    const [isOpen, setIsOpen] = useState(false);

    // Form State
    const [subjectId, setSubjectId] = useState("");
    const [facultyId, setFacultyId] = useState("");
    const [roomId, setRoomId] = useState("");

    // Queries
    const { data: slots } = useQuery({
        queryKey: ["time-slots"],
        queryFn: timetableService.getSlots,
    });

    const { data: schedule } = useQuery({
        queryKey: ["timetable", academicYearId, semesterId, sectionId],
        queryFn: () => timetableService.getSchedule(academicYearId, semesterId, sectionId),
        enabled: !!slots,
    });

    // Mutations
    const createEntryMutation = useMutation({
        mutationFn: timetableService.createScheduleEntry,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["timetable"] });
            toast({ title: "Success", description: "Class scheduled successfully" });
            setIsOpen(false);
            resetForm();
        },
        onError: (error: any) => {
            toast({
                title: "Conflict Detected",
                description: error.response?.data?.detail || "Failed to schedule class",
                variant: "destructive"
            });
        }
    });

    const handleCellClick = (day: DayOfWeek, periodId: number) => {
        setSelectedDay(day);
        setSelectedPeriod(periodId);
        setIsOpen(true);
    };

    const handleSave = () => {
        if (!selectedDay || !selectedPeriod) return;

        const payload: CreateScheduleDTO = {
            academic_year_id: academicYearId,
            semester_id: semesterId,
            section_id: sectionId,
            day_of_week: selectedDay,
            period_id: selectedPeriod,
            subject_id: parseInt(subjectId),
            faculty_id: parseInt(facultyId),
            room_id: roomId ? parseInt(roomId) : undefined,
        };

        createEntryMutation.mutate(payload);
    };

    const resetForm = () => {
        setSubjectId("");
        setFacultyId("");
        setRoomId("");
    };

    // Helper to find existing entry
    const getEntry = (day: DayOfWeek, periodId: number) => {
        return schedule?.find(s => s.day_of_week === day && s.period_id === periodId);
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle>Timetable Builder</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex gap-4 mb-6">
                        <Select value={String(semesterId)} onValueChange={(v) => setSemesterId(Number(v))}>
                            <SelectTrigger className="w-[180px]">
                                <SelectValue placeholder="Select Semester" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="1">Semester 1</SelectItem>
                                <SelectItem value="2">Semester 2</SelectItem>
                            </SelectContent>
                        </Select>
                        {/* Add Section Select here if needed */}
                    </div>

                    <div className="border rounded-md overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="text-xs uppercase bg-gray-50 border-b">
                                <tr>
                                    <th className="px-6 py-3">Period / Day</th>
                                    {DAYS.map(day => (
                                        <th key={day} className="px-6 py-3 text-center">{day}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {slots?.map((slot) => (
                                    <tr key={slot.id} className="border-b">
                                        <td className="px-6 py-4 font-medium bg-gray-50">
                                            {slot.name}
                                            <div className="text-xs text-muted-foreground">
                                                {slot.start_time.slice(0, 5)} - {slot.end_time.slice(0, 5)}
                                            </div>
                                        </td>
                                        {DAYS.map(day => {
                                            const entry = getEntry(day, slot.id);
                                            return (
                                                <td
                                                    key={`${day}-${slot.id}`}
                                                    className="px-2 py-2 border-l cursor-pointer hover:bg-gray-50 transition-colors"
                                                    onClick={() => handleCellClick(day, slot.id)}
                                                >
                                                    {entry ? (
                                                        <div className="p-2 bg-blue-100 text-blue-800 rounded text-xs min-h-[60px]">
                                                            <div className="font-bold truncate">{entry.subject_id}</div> {/* Need Subject Name join */}
                                                            <div>Fac: {entry.faculty_id}</div>
                                                            <div>Room: {entry.room_id}</div>
                                                        </div>
                                                    ) : (
                                                        <div className="h-[60px] flex items-center justify-center text-gray-300 text-xs">
                                                            + Add
                                                        </div>
                                                    )}
                                                </td>
                                            );
                                        })}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>

            <Dialog open={isOpen} onOpenChange={setIsOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Schedule Class ({selectedDay} - Period {selectedPeriod})</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                        <div className="space-y-2">
                            <Label>Subject ID</Label>
                            <Input value={subjectId} onChange={e => setSubjectId(e.target.value)} type="number" placeholder="Enter Subject ID" />
                        </div>
                        <div className="space-y-2">
                            <Label>Faculty ID</Label>
                            <Input value={facultyId} onChange={e => setFacultyId(e.target.value)} type="number" placeholder="Enter Faculty ID" />
                        </div>
                        <div className="space-y-2">
                            <Label>Room ID</Label>
                            <Input value={roomId} onChange={e => setRoomId(e.target.value)} type="number" placeholder="Enter Room ID" />
                        </div>
                        <Button onClick={handleSave} className="w-full" disabled={createEntryMutation.isPending}>
                            {createEntryMutation.isPending ? "Saving..." : "Save Schedule"}
                        </Button>
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    );
}
