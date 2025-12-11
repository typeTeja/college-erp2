import React, { useState } from 'react';
import { Dialog } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { odcService } from '@/utils/odc-service';
import { ODCHotelCreate } from '@/types/odc';

interface HotelFormProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

export const HotelForm = ({ isOpen, onClose, onSuccess }: HotelFormProps) => {
    const [isLoading, setIsLoading] = useState(false);
    const [formData, setFormData] = useState<ODCHotelCreate>({
        name: '',
        address: '',
        contact_person: '',
        phone: '',
        email: '',
        default_pay_rate: undefined
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            await odcService.createHotel(formData);
            onSuccess();
            onClose();
            // Reset form
            setFormData({ name: '', address: '', contact_person: '', phone: '', email: '', default_pay_rate: undefined });
        } catch (error) {
            console.error('Failed to create hotel', error);
            alert('Failed to create hotel');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Dialog isOpen={isOpen} onClose={onClose} title="Add New Hotel">
            <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                    label="Hotel Name"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                />
                <Input
                    label="Address"
                    required
                    value={formData.address}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                />
                <Input
                    label="Contact Person"
                    required
                    value={formData.contact_person}
                    onChange={(e) => setFormData({ ...formData, contact_person: e.target.value })}
                />
                <Input
                    label="Phone"
                    required
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                />
                <Input
                    label="Email"
                    type="email"
                    value={formData.email || ''}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                />
                <Input
                    label="Default Pay Rate (Optional)"
                    type="number"
                    value={formData.default_pay_rate || ''}
                    onChange={(e) => setFormData({ ...formData, default_pay_rate: e.target.value ? parseFloat(e.target.value) : undefined })}
                />
                <div className="flex justify-end space-x-2 pt-4">
                    <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
                    <Button type="submit" disabled={isLoading}>{isLoading ? 'Saving...' : 'Save Hotel'}</Button>
                </div>
            </form>
        </Dialog>
    );
};
