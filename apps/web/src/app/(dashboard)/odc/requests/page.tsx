'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { RequestForm } from '@/components/odc/request-form';
import { ODCRequestList } from '@/components/odc/ODCRequestList';
import { odcService } from '@/utils/odc-service';
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

            <ODCRequestList requests={requests} isLoading={isLoading} />
        </div>
    );
}
