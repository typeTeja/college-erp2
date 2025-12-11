'use client';

import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { ODCApplication } from '@/types/odc';

interface ODCPayoutListProps {
    applications: ODCApplication[];
    selectedIds: number[];
    onSelectAll: (checked: boolean) => void;
    onSelectOne: (id: number, checked: boolean) => void;
    isLoading: boolean;
}

export function ODCPayoutList({
    applications,
    selectedIds,
    onSelectAll,
    onSelectOne,
    isLoading
}: ODCPayoutListProps) {
    if (isLoading) {
        return <div className="text-center py-10">Loading...</div>;
    }

    if (applications.length === 0) {
        return (
            <p className="text-gray-500 text-center py-8">No pending payouts</p>
        );
    }

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-IN');
    };

    return (
        <div className="overflow-x-auto">
            <table className="w-full">
                <thead className="bg-gray-50">
                    <tr>
                        <th className="px-4 py-3 text-left">
                            <Checkbox
                                checked={applications.length > 0 && selectedIds.length === applications.length}
                                onCheckedChange={onSelectAll}
                            />
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student ID</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Event</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Event Date</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Applied At</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                    {applications.map((application) => (
                        <tr key={application.id} className="hover:bg-gray-50">
                            <td className="px-4 py-3">
                                <Checkbox
                                    checked={selectedIds.includes(application.id)}
                                    onCheckedChange={(checked) =>
                                        onSelectOne(application.id, checked as boolean)
                                    }
                                />
                            </td>
                            <td className="px-4 py-3 text-sm font-medium text-gray-900">
                                #{application.student_id}
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-900">
                                {application.event_name || `Request #${application.request_id}`}
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-900">
                                {application.event_date ? formatDate(application.event_date) : '-'}
                            </td>
                            <td className="px-4 py-3 text-sm">
                                <Badge className="bg-green-500">
                                    {application.status}
                                </Badge>
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-900">
                                {formatDate(application.applied_at)}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
