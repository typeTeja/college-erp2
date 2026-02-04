'use client'

import { useRouter, useSearchParams } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { XCircle, RefreshCw } from 'lucide-react'
import { Suspense } from 'react'

function FailureContent() {
    const router = useRouter()
    const searchParams = useSearchParams()

    return (
        <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 flex items-center justify-center p-4">
            <Card className="max-w-md w-full shadow-xl border-red-100">
                <CardHeader className="text-center">
                    <div className="flex justify-center mb-4">
                        <XCircle className="h-16 w-16 text-red-500" />
                    </div>
                    <CardTitle className="text-2xl font-bold text-red-700">Payment Failed</CardTitle>
                    <CardDescription className="text-red-600 font-medium mt-2">
                        We could not process your transaction.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-sm text-red-800">
                        <p><strong>Reason:</strong> {searchParams.get('error') || 'Transaction was declined or cancelled.'}</p>
                        <p className="mt-2">If money was deducted from your account, it will be refunded automatically within 5-7 working days.</p>
                    </div>

                    <div className="flex flex-col gap-3">
                        <Button
                            className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3"
                            onClick={() => router.push('/apply/success')} // Redirects back to "Success" page where payment can be retried
                        >
                            <RefreshCw className="mr-2 h-4 w-4" />
                            Retry Payment
                        </Button>
                        <Button
                            variant="outline"
                            className="w-full"
                            onClick={() => router.push('/')}
                        >
                            Back to Home
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

export default function ApplyFailurePage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <FailureContent />
        </Suspense>
    )
}
