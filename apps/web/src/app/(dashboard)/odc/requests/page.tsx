'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { RequestForm } from '@/components/odc/request-form';
import { odcService } from '@/lib/services/odc-service';
import { ODCRequest, ODCStatus } from '@/types/odc';

export default function RequestsPage() {
    const [requests, setRequests] = useState<ODCRequest[]>([]);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    const loadRequests = async () => {
        setIsLoading(true);
        try {
            const data = await odcService.getRequests();
            setRequests(data);
        } catch (error) {
            console.error('Failed to load requests', error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadRequests();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">Manage Requests</h1>
                <Button onClick={() => setIsFormOpen(true)}>+ New Request</Button>
            </div>

            <RequestForm
                isOpen={isFormOpen}
                onClose={() => setIsFormOpen(false)}
                onSuccess={loadRequests}
            />

            {isLoading ? (
                <div className="text-center py-10">Loading...</div>
            ) : (
                <div className="grid grid-cols-1 gap-4">
                    {requests.map((request) => (
                        <Card key={request.id}>
                            <CardContent className="flex flex-col md:flex-row justify-between items-start md:items-center p-4">
                                <div className="space-y-1">
                                    <h3 className="text-lg font-bold">{request.event_name}</h3>
                                    <p className="text-sm text-gray-600">at <strong>{request.hotel_name || `Hotel #${request.hotel_id}`}</strong> on {new Date(request.event_date).toLocaleDateString()}</p>
                                    <div className="text-xs text-gray-500 flex space-x-4">
                                        <span>Vacancies: {request.vacancies}</span>
                                        <span>Pay: ₹{request.pay_amount}</span>
                                        <span>Duration: {request.duration_hours}h</span>
                                    </div>
                                </div>
                                <div className="flex flex-col items-end space-y-2 mt-2 md:mt-0">
                                    <Badge variant={request.status === ODCStatus.OPEN ? 'success' : 'default'}>
                                        {request.status}
                                    </Badge>
                                    {request.status === ODCStatus.OPEN && (
                                        <div className="text-xs text-gray-500">
                                            {/* Future: Add button to view applicants */}
                                            Applicants: View details
                                        </div>
                                    )}
                                </div>
                            </CardContent>
                        </Card>
                    ))}

                    {requests.length === 0 && (
                        <div className="text-center text-gray-500 py-10 bg-white rounded-lg">
                            No active requests found. Create one above.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
