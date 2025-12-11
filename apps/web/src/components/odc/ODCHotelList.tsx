'use client';

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ODCHotel } from '@/types/odc';

interface ODCHotelListProps {
    hotels: ODCHotel[];
    isLoading: boolean;
}

export function ODCHotelList({ hotels, isLoading }: ODCHotelListProps) {
    if (isLoading) {
        return <div className="text-center py-10">Loading...</div>;
    }

    if (hotels.length === 0) {
        return (
            <div className="col-span-full text-center text-gray-500 py-10 bg-white rounded-lg">
                No hotels found. Add one to get started.
            </div>
        );
    }

    return (
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
        </div>
    );
}
