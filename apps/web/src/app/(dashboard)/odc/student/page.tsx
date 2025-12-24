'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { odcService } from '@/utils/odc-service';
import { ODCRequest, ODCStatus } from '@/types/odc';

export default function StudentOpportunitiesPage() {
    const [requests, setRequests] = useState<ODCRequest[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [applyingId, setApplyingId] = useState<number | null>(null);

    const loadRequests = async () => {
        setIsLoading(true);
        try {
            const allRequests = await odcService.getRequests();
            const data = allRequests.filter(r => r.status === ODCStatus.OPEN);
            setRequests(data);
        } catch (error) {
            console.error('Failed to load opportunities', error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadRequests();
    }, []);

    const handleApply = async (requestId: number) => {
        if (!confirm('Are you sure you want to apply for this ODC?')) return;
        setApplyingId(requestId);
        try {
            await odcService.applyForODC(requestId);
            alert('Applied successfully!');
            // Ideally remove from list or mark as applied
            loadRequests();
        } catch (error) {
            console.error('Failed to apply', error);
            alert('Failed to apply. You might have already applied.');
        } finally {
            setApplyingId(null);
        }
    };

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">Outdoor Catering (ODC) - Hotel Training Opportunities</h1>

            {isLoading ? (
                <div className="text-center py-10">Loading...</div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {requests.map((request) => (
                        <Card key={request.id}>
                            <CardContent className="space-y-4">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h3 className="text-lg font-bold">{request.event_name}</h3>
                                        <p className="text-sm text-gray-600">{request.hotel_name}</p>
                                    </div>
                                    <Badge variant="info">₹{request.pay_amount}</Badge>
                                </div>

                                <div className="text-sm space-y-1">
                                    <p>📅 <strong>Date:</strong> {new Date(request.event_date).toLocaleDateString()}</p>
                                    <p>⏰ <strong>Report Time:</strong> {new Date(request.report_time).toLocaleTimeString()}</p>
                                    <p>⏳ <strong>Duration:</strong> {request.duration_hours} hours</p>
                                    <p>🚌 <strong>Transport:</strong> {request.transport_provided ? 'Provided' : 'Not Provided'}</p>
                                    <p>👥 <strong>Vacancies:</strong> {request.vacancies}</p>
                                </div>

                                <Button
                                    className="w-full"
                                    onClick={() => handleApply(request.id)}
                                    disabled={applyingId === request.id}
                                >
                                    {applyingId === request.id ? 'Applying...' : 'Apply Now'}
                                </Button>
                            </CardContent>
                        </Card>
                    ))}

                    {requests.length === 0 && (
                        <div className="col-span-full text-center text-gray-500 py-10 bg-white rounded-lg">
                            No open opportunities available right now.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
