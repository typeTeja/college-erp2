import { useQuery } from "@tanstack/react-query";
import { timetableService } from "@/utils/timetable-service";
import { DayOfWeek, ClassSchedule, SlotType } from "@/types/timetable";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2 } from "lucide-react";

const DAYS = Object.values(DayOfWeek);

export function FacultySchedule({ facultyId }: { facultyId: number }) {
    const { data: schedule, isLoading } = useQuery({
        queryKey: ["faculty-schedule", facultyId],
        queryFn: () => timetableService.getFacultySchedule(facultyId),
    });

    const { data: slots } = useQuery({
        queryKey: ["time-slots"],
        queryFn: timetableService.getSlots,
    });

    if (isLoading) {
        return <div className="flex justify-center p-8"><Loader2 className="h-8 w-8 animate-spin" /></div>;
    }

    const getEntry = (day: DayOfWeek, periodId: number) => {
        return schedule?.find(s => s.day_of_week === day && s.period_id === periodId);
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>My Weekly Schedule</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="border rounded-md overflow-x-auto">
                    <table className="w-full text-sm text-left">
                        <thead className="text-xs uppercase bg-gray-50 border-b">
                            <tr>
                                <th className="px-6 py-3">Period</th>
                                {DAYS.map(day => (
                                    <th key={day} className="px-6 py-3 text-center">{day}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {slots?.map((slot) => (
                                <tr key={slot.id} className="border-b">
                                    <td className="px-6 py-4 font-medium bg-gray-50 whitespace-nowrap">
                                        {slot.name}
                                        <div className="text-xs text-muted-foreground">
                                            {slot.start_time.slice(0, 5)} - {slot.end_time.slice(0, 5)}
                                        </div>
                                    </td>
                                    {DAYS.map(day => {
                                        const entry = getEntry(day, slot.id);
                                        return (
                                            <td key={`${day}-${slot.id}`} className="px-2 py-2 border-l min-w-[120px]">
                                                {entry ? (
                                                    <div className={`p-2 rounded text-xs border ${entry.period?.type === SlotType.PRACTICAL
                                                        ? 'bg-purple-50 border-purple-200 text-purple-700'
                                                        : 'bg-blue-50 border-blue-200 text-blue-700'
                                                        }`}>
                                                        <div className="font-bold">{entry.subject_name || `Subject ${entry.subject_id}`}</div>
                                                        <div>Room: {entry.room_number || entry.room_id}</div>
                                                        <div className="mt-1">
                                                            <Badge variant="default" className="text-[10px] h-5">
                                                                Sem {entry.semester_id}
                                                            </Badge>
                                                        </div>
                                                    </div>
                                                ) : (
                                                    <div className="text-center text-gray-300">-</div>
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
    );
}
