'use client';

import Link from 'next/link';
import { useAuthStore } from '@/store/use-auth-store';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function ODCDashboard() {
    const { user } = useAuthStore();
    const isStudent = user?.roles?.includes('STUDENT');
    const isAdmin = user?.roles?.includes('SUPER_ADMIN') || user?.roles?.includes('ADMIN') || user?.roles?.includes('FACULTY');

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">Outdoor Catering (ODC) Dashboard</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Student Actions */}
                {isStudent && (
                    <>
                        <Card>
                            <CardHeader>
                                <h3 className="text-lg font-medium">New Opportunities</h3>
                            </CardHeader>
                            <CardContent>
                                <p className="text-gray-500 mb-4">Browse and apply for upcoming ODC events.</p>
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
                                <p className="text-gray-500 mb-4">Check status of your applications and history.</p>
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
                                <p className="text-gray-500 mb-4">Create and manage ODC event requests.</p>
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
                                <p className="text-gray-500 mb-4">Add or update hotel partners.</p>
                                <Link href="/odc/hotels">
                                    <Button variant="secondary" className="w-full">Manage Hotels</Button>
                                </Link>
                            </CardContent>
                        </Card>
                    </>
                )}
            </div>
        </div>
    );
}
