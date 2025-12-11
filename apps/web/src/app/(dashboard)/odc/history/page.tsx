'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { odcService } from '@/utils/odc-service';
import { ODCApplication, ApplicationStatus } from '@/types/odc';
import FeedbackForm from '@/components/odc/FeedbackForm';

export default function ApplicationHistoryPage() {
    const [applications, setApplications] = useState<ODCApplication[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [showFeedbackFor, setShowFeedbackFor] = useState<number | null>(null);

    useEffect(() => {
        loadHistory();
    }, []);

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

    const getStatusVariant = (status: ApplicationStatus) => {
        switch (status) {
            case ApplicationStatus.SELECTED: return 'success';
            case ApplicationStatus.REJECTED: return 'danger';
            case ApplicationStatus.ATTENDED: return 'success';
            case ApplicationStatus.ABSENT: return 'danger';
            default: return 'warning'; // APPLIED
        }
    };

    const handleFeedbackSuccess = () => {
        setShowFeedbackFor(null);
        loadHistory();
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
                            <CardContent className="p-4 space-y-4">
                                <div className="flex justify-between items-start">
                                    <div className="flex-1">
                                        <h3 className="font-bold text-lg">
                                            {app.event_name || `ODC Request #${app.request_id}`}
                                        </h3>
                                        <p className="text-sm text-gray-500">
                                            Applied on {new Date(app.applied_at).toLocaleDateString()}
                                        </p>
                                        {app.event_date && (
                                            <p className="text-sm text-gray-600 mt-1">
                                                Event Date: {new Date(app.event_date).toLocaleDateString()}
                                            </p>
                                        )}
                                    </div>
                                    <div className="flex flex-col items-end gap-2">
                                        <Badge variant={getStatusVariant(app.status)}>
                                            {app.status}
                                        </Badge>
                                        {app.status === ApplicationStatus.ATTENDED && (
                                            <Badge className="bg-purple-500">
                                                Payout: Pending
                                            </Badge>
                                        )}
                                    </div>
                                </div>

                                {app.status === ApplicationStatus.ATTENDED && (
                                    <div className="border-t pt-4">
                                        {showFeedbackFor === app.id ? (
                                            <div className="space-y-2">
                                                <FeedbackForm
                                                    applicationId={app.id}
                                                    onSuccess={handleFeedbackSuccess}
                                                />
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    onClick={() => setShowFeedbackFor(null)}
                                                >
                                                    Cancel
                                                </Button>
                                            </div>
                                        ) : (
                                            <Button
                                                onClick={() => setShowFeedbackFor(app.id)}
                                                size="sm"
                                            >
                                                Submit Feedback
                                            </Button>
                                        )}
                                    </div>
                                )}
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
