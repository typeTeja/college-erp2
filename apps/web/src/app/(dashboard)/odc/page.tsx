'use client';

import Link from 'next/link';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { KPICard } from '@/components/dashboard/KPICard';
import { Building2, ClipboardList, Wallet, Users } from 'lucide-react';
import { odcService } from '@/utils/odc-service';
import { useState, useEffect } from 'react';
import { ODCStatus, BillingStatus } from '@/types/odc';

export default function ODCDashboard() {
    const { user } = useAuthStore();
    const [stats, setStats] = useState({
        totalHotels: 0,
        activeRequests: 0,
        pendingPayouts: 0,
        totalCollected: 0
    });

    useEffect(() => {
        const loadStats = async () => {
            try {
                const [hotels, requests, pendingPayouts, billings] = await Promise.all([
                    odcService.getHotels(),
                    odcService.getRequests(),
                    odcService.getPendingPayouts(),
                    odcService.getBilling()
                ]);

                setStats({
                    totalHotels: hotels.length,
                    activeRequests: requests.filter(r => r.status === ODCStatus.OPEN).length,
                    pendingPayouts: pendingPayouts.length,
                    totalCollected: billings
                        .filter(b => b.status === BillingStatus.PAID)
                        .reduce((sum, b) => sum + (b.total_amount || 0), 0)
                });
            } catch (error) {
                console.error('Failed to load ODC stats', error);
            }
        };

        if (user) loadStats();
    }, [user]);

    const isStudent = user?.roles?.includes('STUDENT');
    const isAdmin = user?.roles?.some(role =>
        ['SUPER_ADMIN', 'ADMIN', 'FACULTY', 'ODC_COORDINATOR', 'STAFF'].includes(role)
    );

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-semibold text-slate-900">Outdoor Catering (ODC) - Hotel Training</h1>
            </div>

            {isAdmin && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <KPICard
                        title="Active Requests"
                        value={stats.activeRequests}
                        icon={<ClipboardList size={24} />}
                        color="blue"
                    />
                    <KPICard
                        title="Hotel Partners"
                        value={stats.totalHotels}
                        icon={<Building2 size={24} />}
                        color="indigo"
                    />
                    <KPICard
                        title="Pending Payouts"
                        value={stats.pendingPayouts}
                        icon={<Users size={24} />}
                        color="orange"
                    />
                    <KPICard
                        title="Total Collected"
                        value={`₹${stats.totalCollected.toLocaleString('en-IN')}`}
                        icon={<Wallet size={24} />}
                        color="green"
                    />
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Student Actions */}
                {isStudent && (
                    <>
                        <Card>
                            <CardHeader>
                                <h3 className="text-lg font-medium">New Opportunities</h3>
                            </CardHeader>
                            <CardContent>
                                <p className="text-slate-500 mb-4">Browse and apply for upcoming ODC events.</p>
                                <Link href="/odc/student">
                                    <Button className="w-full">View Opportunities</Button>
                                </Link>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <h3 className="text-lg font-medium">My Applications</h3>
                            </CardHeader>
                            <CardContent>
                                <p className="text-slate-500 mb-4">Check status of your applications and history.</p>
                                <Link href="/odc/history">
                                    <Button variant="secondary" className="w-full">View History</Button>
                                </Link>
                            </CardContent>
                        </Card>
                    </>
                )}

                {/* Admin Actions */}
                {isAdmin && (
                    <>
                        <Card>
                            <CardHeader>
                                <h3 className="text-lg font-medium">Manage Requests</h3>
                            </CardHeader>
                            <CardContent>
                                <p className="text-slate-500 mb-4">Create and manage ODC event requests.</p>
                                <Link href="/odc/requests">
                                    <Button className="w-full">Manage Requests</Button>
                                </Link>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <h3 className="text-lg font-medium">Manage Hotels</h3>
                            </CardHeader>
                            <CardContent>
                                <p className="text-slate-500 mb-4">Add or update hotel partners.</p>
                                <Link href="/odc/hotels">
                                    <Button variant="secondary" className="w-full">Manage Hotels</Button>
                                </Link>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <h3 className="text-lg font-medium">Billing Management</h3>
                            </CardHeader>
                            <CardContent>
                                <p className="text-slate-500 mb-4">Generate and track invoices for ODC events.</p>
                                <Link href="/odc/billing">
                                    <Button variant="secondary" className="w-full">View Billings</Button>
                                </Link>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <h3 className="text-lg font-medium">Payout Management</h3>
                            </CardHeader>
                            <CardContent>
                                <p className="text-slate-500 mb-4">Process student payouts for attended events.</p>
                                <Link href="/odc/payouts">
                                    <Button variant="secondary" className="w-full">Manage Payouts</Button>
                                </Link>
                            </CardContent>
                        </Card>
                    </>
                )}
            </div>
        </div>
    );
}
