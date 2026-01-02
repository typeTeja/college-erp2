import React, { useState, useEffect } from 'react';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { getInstituteInfo, updateInstituteInfo } from '@/utils/institute-service';
import { InstituteInfo } from '@/types/institute';

export function InstituteTab({ isAdmin }: { isAdmin: boolean }) {
    const [info, setInfo] = useState<InstituteInfo | null>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        if (!isAdmin) return;
        const fetch = async () => {
            try {
                const data = await getInstituteInfo();
                setInfo(data);
            } catch (e) {
                toast.error('Failed to load institute info');
            } finally {
                setLoading(false);
            }
        };
        fetch();
    }, [isAdmin]);

    if (!isAdmin) {
        return <p className="text-sm text-slate-500">You do not have permission to view institute settings.</p>;
    }

    if (loading) {
        return <p className="text-sm text-slate-500">Loading...</p>;
    }

    const handleChange = (field: keyof InstituteInfo) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        if (info) setInfo({ ...info, [field]: e.target.value });
    };

    const handleSave = async () => {
        if (!info) return;
        setSaving(true);
        try {
            await updateInstituteInfo(info);
            toast.success('Institute information updated');
        } catch (e) {
            toast.error('Failed to update institute information');
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium mb-1">Institute Name</label>
                    <Input value={info?.name || ''} onChange={handleChange('name')} />
                </div>
                <div>
                    <label className="block text-sm font-medium mb-1">Short Code</label>
                    <Input value={info?.short_code || ''} onChange={handleChange('short_code')} />
                </div>
            </div>
            <div>
                <label className="block text-sm font-medium mb-1">Address</label>
                <Textarea value={info?.address || ''} onChange={handleChange('address')} rows={3} />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium mb-1">Contact Email</label>
                    <Input type="email" value={info?.contact_email || ''} onChange={handleChange('contact_email')} />
                </div>
                <div>
                    <label className="block text-sm font-medium mb-1">Contact Phone</label>
                    <Input value={info?.contact_phone || ''} onChange={handleChange('contact_phone')} />
                </div>
            </div>
            <div>
                <label className="block text-sm font-medium mb-1">Logo URL</label>
                <Input value={info?.logo_url || ''} onChange={handleChange('logo_url')} placeholder="https://example.com/logo.png" />
            </div>
            <div className="flex justify-end pt-2">
                <Button onClick={handleSave} disabled={saving} className="bg-blue-600 hover:bg-blue-700">
                    {saving ? 'Saving...' : 'Save Institute Info'}
                </Button>
            </div>
        </div>
    );
}
