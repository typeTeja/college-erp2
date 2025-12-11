'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { odcService } from '@/lib/services/odc-service';
import { ODCApplication, ApplicationStatus } from '@/types/odc';

export default function ApplicationHistoryPage() {
    const [applications, setApplications] = useState<ODCApplication[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const loadHistory = async () => {
            setIsLoading(true);
            try {
                const data = await odcService.getMyApplications();
                setApplications(data);
            } catch (error) {
                console.error('Failed to load history', error);
            } finally {
                setIsLoading(false);
            }
        };
        loadHistory();
    }, []);

    const getStatusVariant = (status: ApplicationStatus) => {
        switch (status) {
            case ApplicationStatus.SELECTED: return 'success';
            case ApplicationStatus.REJECTED: return 'danger';
            case ApplicationStatus.ATTENDED: return 'success';
            case ApplicationStatus.ABSENT: return 'danger';
            default: return 'warning'; // APPLIED
        }
    };

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">My Application History</h1>

            {isLoading ? (
                <div className="text-center py-10">Loading...</div>
            ) : (
                <div className="space-y-4">
                    {applications.map((app) => (
                        <Card key={app.id}>
                            <CardContent className="flex justify-between items-center bg-white p-4 rounded-lg">
                                <div>
                                    <h3 className="font-bold">ODC Request #{app.request_id}</h3>
                                    <p className="text-sm text-gray-500">Applied on {new Date(app.applied_at).toLocaleDateString()}</p>
                                </div>
                                <div className="flex items-center space-x-4">
                                    <Badge variant={getStatusVariant(app.status)}>
                                        {app.status}
                                    </Badge>
                                </div>
                            </CardContent>
                        </Card>
                    ))}

                    {applications.length === 0 && (
                        <div className="text-center text-gray-500 py-10 bg-white rounded-lg">
                            No application history found.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
