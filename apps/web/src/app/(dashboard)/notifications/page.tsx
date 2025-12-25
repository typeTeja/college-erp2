'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
    Bell, CheckCircle2, AlertCircle, Info,
    XCircle, ArrowLeft, MoreVertical, Trash2,
    Check
} from 'lucide-react'
import Link from 'next/link'
import { communicationService } from '@/utils/communication-service'
import { NotificationType } from '@/types/communication'

export default function NotificationsPage() {
    const { data: notifications, isLoading } = communicationService.useNotifications()
    const markAsRead = communicationService.useMarkAsRead()
    const markAllRead = communicationService.useMarkAllAsRead()

    const getIcon = (type: NotificationType) => {
        switch (type) {
            case NotificationType.SUCCESS: return <CheckCircle2 className="text-green-500" size={20} />
            case NotificationType.WARNING: return <AlertCircle className="text-amber-500" size={20} />
            case NotificationType.ERROR: return <XCircle className="text-red-500" size={20} />
            default: return <Info className="text-blue-500" size={20} />
        }
    }

    return (
        <div className="p-6 max-w-4xl mx-auto space-y-6">
            <div className="flex items-center gap-4">
                <Link href="/">
                    <Button variant="outline" size="sm" className="h-9 w-9 p-0">
                        <ArrowLeft size={18} />
                    </Button>
                </Link>
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">Notifications</h1>
                    <p className="text-slate-500 mt-1">Stay updated with important system alerts</p>
                </div>
                <div className="ml-auto flex gap-3">
                    <Button
                        variant="outline"
                        className="gap-2"
                        onClick={() => markAllRead.mutate()}
                        disabled={markAllRead.isPending}
                    >
                        <Check size={18} /> Mark All as Read
                    </Button>
                </div>
            </div>

            <div className="space-y-3">
                {isLoading ? (
                    <div className="py-12 text-center text-slate-400">Loading notifications...</div>
                ) : notifications?.length === 0 ? (
                    <Card className="border-dashed border-slate-200">
                        <CardContent className="py-12 text-center">
                            <Bell className="mx-auto text-slate-300 mb-4" size={48} />
                            <p className="text-slate-500">You're all caught up! No recent notifications.</p>
                        </CardContent>
                    </Card>
                ) : (
                    notifications?.map((notification) => (
                        <Card
                            key={notification.id}
                            className={`border-slate-200 transition-colors ${!notification.is_read ? 'bg-blue-50/30 border-blue-100' : 'bg-white'}`}
                        >
                            <CardContent className="p-4 flex gap-4">
                                <div className="mt-1">
                                    {getIcon(notification.type)}
                                </div>
                                <div className="flex-1 space-y-1">
                                    <div className="flex justify-between items-start">
                                        <h3 className={`font-semibold ${!notification.is_read ? 'text-slate-900' : 'text-slate-700'}`}>
                                            {notification.title}
                                        </h3>
                                        <span className="text-xs text-slate-400">
                                            {new Date(notification.created_at).toLocaleDateString()}
                                        </span>
                                    </div>
                                    <p className="text-sm text-slate-600">{notification.message}</p>

                                    {!notification.is_read && (
                                        <button
                                            className="text-xs text-blue-600 font-medium mt-2 hover:underline"
                                            onClick={() => markAsRead.mutate(notification.id)}
                                        >
                                            Mark as read
                                        </button>
                                    )}
                                </div>
                                <Button variant="ghost" size="sm" className="h-8 w-8 p-0 text-slate-400">
                                    <MoreVertical size={16} />
                                </Button>
                            </CardContent>
                        </Card>
                    ))
                )}
            </div>
        </div>
    )
}
