'use client'

import { admissionsService } from '@/utils/admissions-service'
import { ActivityType } from '@/types/admissions'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Clock, CheckCircle, XCircle, Upload, FileCheck, DollarSign, FormInput } from 'lucide-react'

interface ActivityTimelineProps {
    applicationId: number
}

const ACTIVITY_ICONS: Record<ActivityType, React.ReactNode> = {
    [ActivityType.APPLICATION_CREATED]: <FormInput className="h-4 w-4" />,
    [ActivityType.PAYMENT_INITIATED]: <DollarSign className="h-4 w-4" />,
    [ActivityType.PAYMENT_SUCCESS]: <CheckCircle className="h-4 w-4 text-green-600" />,
    [ActivityType.PAYMENT_FAILED]: <XCircle className="h-4 w-4 text-red-600" />,
    [ActivityType.OFFLINE_PAYMENT_VERIFIED]: <CheckCircle className="h-4 w-4 text-green-600" />,
    [ActivityType.FORM_COMPLETED]: <FormInput className="h-4 w-4 text-blue-600" />,
    [ActivityType.DOCUMENT_UPLOADED]: <Upload className="h-4 w-4" />,
    [ActivityType.DOCUMENT_VERIFIED]: <FileCheck className="h-4 w-4 text-green-600" />,
    [ActivityType.DOCUMENT_REJECTED]: <XCircle className="h-4 w-4 text-red-600" />,
    [ActivityType.STATUS_CHANGED]: <Clock className="h-4 w-4" />,
    [ActivityType.ADMISSION_CONFIRMED]: <CheckCircle className="h-4 w-4 text-green-600" />,
    [ActivityType.ADMISSION_REJECTED]: <XCircle className="h-4 w-4 text-red-600" />
}

export default function ActivityTimeline({ applicationId }: ActivityTimelineProps) {
    const { data: timeline, isLoading } = admissionsService.useTimeline(applicationId)

    const formatDate = (dateString: string) => {
        const date = new Date(dateString)
        return date.toLocaleString('en-IN', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <Clock className="h-5 w-5" />
                    Activity Timeline
                </CardTitle>
            </CardHeader>
            <CardContent>
                {isLoading ? (
                    <p className="text-center text-muted-foreground">Loading timeline...</p>
                ) : timeline && timeline.length > 0 ? (
                    <div className="relative space-y-4">
                        {/* Timeline line */}
                        <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-border" />

                        {timeline.map((activity, index) => (
                            <div key={activity.id} className="relative flex gap-4 pl-10">
                                {/* Timeline dot */}
                                <div className="absolute left-0 top-1 flex h-8 w-8 items-center justify-center rounded-full border-2 border-background bg-card">
                                    {ACTIVITY_ICONS[activity.activity_type] || <Clock className="h-4 w-4" />}
                                </div>

                                {/* Content */}
                                <div className="flex-1 pb-4">
                                    <div className="flex items-start justify-between gap-2">
                                        <div className="flex-1">
                                            <p className="font-medium">{activity.description}</p>
                                            <p className="text-sm text-muted-foreground mt-1">
                                                {formatDate(activity.created_at)}
                                            </p>
                                            {activity.ip_address && (
                                                <p className="text-xs text-muted-foreground mt-1">
                                                    IP: {activity.ip_address}
                                                </p>
                                            )}
                                            {activity.extra_data && (
                                                <details className="mt-2">
                                                    <summary className="text-xs text-muted-foreground cursor-pointer hover:text-foreground">
                                                        View details
                                                    </summary>
                                                    <pre className="text-xs mt-1 p-2 bg-muted rounded overflow-x-auto">
                                                        {JSON.stringify(activity.extra_data, null, 2)}
                                                    </pre>
                                                </details>
                                            )}
                                        </div>
                                        <Badge variant="outline" className="text-xs">
                                            {activity.activity_type.replace(/_/g, ' ')}
                                        </Badge>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="text-center text-muted-foreground py-8">
                        No activity recorded yet
                    </p>
                )}
            </CardContent>
        </Card>
    )
}
