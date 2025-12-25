import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CalendarDays, Users, ArrowRight, Settings } from "lucide-react";

export default function TimetableDashboard() {
    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold tracking-tight mb-6">Timetable & Faculty</h1>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Timetable Management</CardTitle>
                        <Settings className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">Schedule Builder</div>
                        <p className="text-xs text-muted-foreground mb-4">
                            Create and modify class schedules.
                        </p>
                        <Link href="/timetable/manage">
                            <Button className="w-full">
                                Go to Builder <ArrowRight className="ml-2 h-4 w-4" />
                            </Button>
                        </Link>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Faculty</CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">My Schedule</div>
                        <p className="text-xs text-muted-foreground mb-4">
                            View your weekly teaching schedule.
                        </p>
                        <Link href="/timetable/faculty">
                            <Button variant="outline" className="w-full">
                                View Schedule <ArrowRight className="ml-2 h-4 w-4" />
                            </Button>
                        </Link>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Adjustments</CardTitle>
                        <CalendarDays className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">Substitutions</div>
                        <p className="text-xs text-muted-foreground mb-4">
                            Request leaves and class adjustments.
                        </p>
                        <div className="flex flex-col gap-2">
                            <Link href="/timetable/adjustments/request">
                                <Button className="w-full" variant="outline">
                                    Request Substitution
                                </Button>
                            </Link>
                            <Link href="/timetable/adjustments/manage">
                                <Button className="w-full" variant="secondary">
                                    Manage Requests
                                </Button>
                            </Link>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
