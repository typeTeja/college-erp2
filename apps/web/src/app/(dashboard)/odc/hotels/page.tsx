'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { HotelForm } from '@/components/odc/hotel-form';
import { ODCHotelList } from '@/components/odc/ODCHotelList';
import { odcService } from '@/utils/odc-service';
import { ODCHotel } from '@/types/odc';

export default function HotelsPage() {
    const [hotels, setHotels] = useState<ODCHotel[]>([]);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    const loadHotels = async () => {
        setIsLoading(true);
        try {
            const data = await odcService.getHotels();
            setHotels(data);
        } catch (error) {
            console.error('Failed to load hotels', error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadHotels();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">Manage Hotels</h1>
                <Button onClick={() => setIsFormOpen(true)}>+ Add Hotel</Button>
            </div>

            <HotelForm
                isOpen={isFormOpen}
                onClose={() => setIsFormOpen(false)}
                onSuccess={loadHotels}
            />

            <ODCHotelList hotels={hotels} isLoading={isLoading} />
        </div>
    );
}
