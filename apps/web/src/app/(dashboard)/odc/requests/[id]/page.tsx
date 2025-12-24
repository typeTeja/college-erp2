'use client';

import React, { useEffect, useState, use } from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { odcService } from '@/utils/odc-service';
import { ODCRequest, ODCApplication, ApplicationStatus } from '@/types/odc';
import { ApplicantList } from '@/components/odc/ApplicantList';
import { useRouter } from 'next/navigation';

export default function RequestDetailsPage({ params }: { params: Promise<{ id: string }> }) {
    const { id: requestIdStr } = use(params);
    const requestId = parseInt(requestIdStr);
    const router = useRouter();

    const [request, setRequest] = useState<ODCRequest | null>(null);
    const [applications, setApplications] = useState<ODCApplication[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    const loadData = async () => {
        setIsLoading(true);
        try {
            // In a real app we'd have a getRequestById, but here we'll filter from list
            const allRequests = await odcService.getRequests();
            const req = allRequests.find(r => r.id === requestId);
            if (!req) {
                alert('Request not found');
                router.push('/odc/requests');
                return;
            }
            setRequest(req);

            const apps = await odcService.getRequestApplications(requestId);
            setApplications(apps);
        } catch (error) {
            console.error('Failed to load request data', error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, [requestId]);

    const handleUpdateStatus = async (appId: number, status: ApplicationStatus) => {
        try {
            await odcService.selectStudents({
                application_ids: [appId],
                status: status
            });
            loadData();
        } catch (error) {
            console.error('Failed to update status', error);
            alert('Failed to update status');
        }
    };

    if (isLoading && !request) {
        return <div className="text-center py-10">Loading...</div>;
    }

    if (!request) return null;

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-4">
                <Button variant="outline" size="sm" onClick={() => router.back()}>
                    &larr; Back
                </Button>
                <h1 className="text-2xl font-bold text-gray-900">{request.event_name}</h1>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <Card className="lg:col-span-1">
                    <CardHeader>
                        <h3 className="text-lg font-bold">Event Details</h3>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="text-sm space-y-2">
                            <p><strong>Hotel:</strong> {request.hotel_name || `Hotel #${request.hotel_id}`}</p>
                            <p><strong>Date:</strong> {new Date(request.event_date).toLocaleDateString()}</p>
                            <p><strong>Time:</strong> {new Date(request.report_time).toLocaleTimeString()}</p>
                            <p><strong>Pay:</strong> ₹{request.pay_amount}</p>
                            <p><strong>Vacancies:</strong> {request.vacancies}</p>
                            <p><strong>Status:</strong> <Badge>{request.status}</Badge></p>
                        </div>
                    </CardContent>
                </Card>

                <Card className="lg:col-span-2">
                    <CardHeader>
                        <h3 className="text-lg font-bold">Applicants ({applications.length})</h3>
                    </CardHeader>
                    <CardContent>
                        <ApplicantList
                            applications={applications}
                            isLoading={isLoading}
                            onSelect={(id) => handleUpdateStatus(id, ApplicationStatus.SELECTED)}
                            onReject={(id) => handleUpdateStatus(id, ApplicationStatus.REJECTED)}
                        />
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
