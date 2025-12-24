'use client';

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ODCApplication, ApplicationStatus } from '@/types/odc';

interface ApplicantListProps {
    applications: ODCApplication[];
    onSelect: (appId: number) => void;
    onReject: (appId: number) => void;
    isLoading: boolean;
}

export function ApplicantList({ applications, onSelect, onReject, isLoading }: ApplicantListProps) {
    if (isLoading) {
        return <div className="text-center py-10">Loading applicants...</div>;
    }

    if (applications.length === 0) {
        return (
            <div className="text-center text-gray-500 py-10 bg-white rounded-lg">
                No applicants yet for this request.
            </div>
        );
    }

    const getStatusVariant = (status: ApplicationStatus) => {
        switch (status) {
            case ApplicationStatus.SELECTED: return 'success';
            case ApplicationStatus.REJECTED: return 'danger';
            case ApplicationStatus.ATTENDED: return 'success';
            default: return 'warning';
        }
    };

    return (
        <div className="space-y-4">
            {applications.map((app) => (
                <Card key={app.id}>
                    <CardContent className="flex justify-between items-center p-4">
                        <div>
                            <p className="font-bold">Student #{app.student_id}</p>
                            <p className="text-sm text-gray-500">Applied: {new Date(app.applied_at).toLocaleString()}</p>
                            <Badge variant={getStatusVariant(app.status)} className="mt-1">
                                {app.status}
                            </Badge>
                        </div>
                        {app.status === ApplicationStatus.APPLIED && (
                            <div className="flex gap-2">
                                <Button
                                    size="sm"
                                    variant="outline"
                                    className="text-red-600 border-red-200 hover:bg-red-50"
                                    onClick={() => onReject(app.id)}
                                >
                                    Reject
                                </Button>
                                <Button
                                    size="sm"
                                    onClick={() => onSelect(app.id)}
                                >
                                    Select
                                </Button>
                            </div>
                        )}
                    </CardContent>
                </Card>
            ))}
        </div>
    );
}
