'use client';

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ODCRequest, ODCStatus } from '@/types/odc';

interface ODCRequestListProps {
    requests: ODCRequest[];
    isLoading: boolean;
}

export function ODCRequestList({ requests, isLoading }: ODCRequestListProps) {
    if (isLoading) {
        return <div className="text-center py-10">Loading...</div>;
    }

    if (requests.length === 0) {
        return (
            <div className="text-center text-gray-500 py-10 bg-white rounded-lg">
                No active requests found. Create one above.
            </div>
        );
    }

    return (
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
                                    Applicants: View details
                                </div>
                            )}
                        </div>
                    </CardContent>
                </Card>
            ))}
        </div>
    );
}
