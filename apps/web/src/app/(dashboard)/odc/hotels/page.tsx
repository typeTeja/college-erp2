'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { HotelForm } from '@/components/odc/hotel-form';
import { odcService } from '@/lib/services/odc-service';
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

            {isLoading ? (
                <div className="text-center py-10">Loading...</div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {hotels.map((hotel) => (
                        <Card key={hotel.id}>
                            <CardContent className="space-y-2">
                                <div className="flex justify-between items-start">
                                    <h3 className="text-lg font-bold">{hotel.name}</h3>
                                    {hotel.is_active ? <Badge variant="success">Active</Badge> : <Badge variant="danger">Inactive</Badge>}
                                </div>
                                <p className="text-sm text-gray-600">{hotel.address}</p>
                                <div className="text-sm pt-2">
                                    <p><strong>Contact:</strong> {hotel.contact_person}</p>
                                    <p><strong>Phone:</strong> {hotel.phone}</p>
                                    {hotel.default_pay_rate && <p><strong>Rate:</strong> ₹{hotel.default_pay_rate}</p>}
                                </div>
                            </CardContent>
                        </Card>
                    ))}

                    {hotels.length === 0 && (
                        <div className="col-span-full text-center text-gray-500 py-10 bg-white rounded-lg">
                            No hotels found. Add one to get started.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
