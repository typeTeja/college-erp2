import React, { useState, useEffect } from 'react';
import { Dialog } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';
import { odcService } from '@/lib/services/odc-service';
import { ODCRequestCreate, ODCHotel, GenderPreference } from '@/types/odc';

interface RequestFormProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

export const RequestForm = ({ isOpen, onClose, onSuccess }: RequestFormProps) => {
    const [isLoading, setIsLoading] = useState(false);
    const [hotels, setHotels] = useState<ODCHotel[]>([]);
    const [formData, setFormData] = useState<ODCRequestCreate>({
        hotel_id: 0,
        event_name: '',
        event_date: '',
        report_time: '',
        duration_hours: 4,
        vacancies: 1,
        gender_preference: GenderPreference.ANY,
        pay_amount: 0,
        transport_provided: false
    });

    useEffect(() => {
        if (isOpen) {
            odcService.getHotels().then(setHotels).catch(console.error);
        }
    }, [isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            await odcService.createRequest(formData);
            onSuccess();
            onClose();
        } catch (error) {
            console.error('Failed to create request', error);
            alert('Failed to create request');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Dialog isOpen={isOpen} onClose={onClose} title="Create ODC Request">
            <form onSubmit={handleSubmit} className="space-y-4">
                <Select
                    label="Hotel"
                    required
                    value={formData.hotel_id}
                    onChange={(e) => setFormData({ ...formData, hotel_id: parseInt(e.target.value) })}
                    options={[
                        { label: 'Select Hotel', value: 0 },
                        ...hotels.map(h => ({ label: h.name, value: h.id }))
                    ]}
                />

                <Input
                    label="Event Name"
                    required
                    value={formData.event_name}
                    onChange={(e) => setFormData({ ...formData, event_name: e.target.value })}
                />

                <div className="grid grid-cols-2 gap-4">
                    <Input
                        label="Event Date"
                        type="date"
                        required
                        value={formData.event_date}
                        onChange={(e) => setFormData({ ...formData, event_date: e.target.value })}
                    />
                    <Input
                        label="Report Time"
                        type="datetime-local"
                        required
                        value={formData.report_time}
                        onChange={(e) => setFormData({ ...formData, report_time: e.target.value })}
                    />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <Input
                        label="Duration (Hours)"
                        type="number"
                        required
                        value={formData.duration_hours}
                        onChange={(e) => setFormData({ ...formData, duration_hours: parseFloat(e.target.value) })}
                    />
                    <Input
                        label="Vacancies"
                        type="number"
                        required
                        value={formData.vacancies}
                        onChange={(e) => setFormData({ ...formData, vacancies: parseInt(e.target.value) })}
                    />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <Select
                        label="Gender Preference"
                        value={formData.gender_preference}
                        onChange={(e) => setFormData({ ...formData, gender_preference: e.target.value as GenderPreference })}
                        options={[
                            { label: 'Any', value: GenderPreference.ANY },
                            { label: 'Male Only', value: GenderPreference.MALE },
                            { label: 'Female Only', value: GenderPreference.FEMALE }
                        ]}
                    />
                    <Input
                        label="Pay Amount"
                        type="number"
                        required
                        value={formData.pay_amount}
                        onChange={(e) => setFormData({ ...formData, pay_amount: parseFloat(e.target.value) })}
                    />
                </div>

                <div className="flex items-center">
                    <input
                        id="transport"
                        type="checkbox"
                        checked={formData.transport_provided}
                        onChange={(e) => setFormData({ ...formData, transport_provided: e.target.checked })}
                        className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    />
                    <label htmlFor="transport" className="ml-2 block text-sm text-gray-900">
                        Transport Provided
                    </label>
                </div>

                <div className="flex justify-end space-x-2 pt-4">
                    <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
                    <Button type="submit" disabled={isLoading}>{isLoading ? 'Creating...' : 'Create Request'}</Button>
                </div>
            </form>
        </Dialog>
    );
};
