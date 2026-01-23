'use client'

import { Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react'
import Link from 'next/link'

function PaymentStatusContent() {
    const searchParams = useSearchParams()
    const router = useRouter()
    
    const status = searchParams.get('status')
    const txnid = searchParams.get('txnid')
    const amount = searchParams.get('amount')
    const error = searchParams.get('error')

    const isSuccess = status === 'success'
    const isFailure = status === 'failure'

    return (
        <Card className="max-w-md w-full shadow-2xl border-0 overflow-hidden">
            <div className={`h-2 ${isSuccess ? 'bg-green-500' : 'bg-red-500'}`} />
            <CardHeader className="text-center pb-2">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-white shadow-lg">
                    {isSuccess ? (
                        <CheckCircle className="h-10 w-10 text-green-500" />
                    ) : (
                        <XCircle className="h-10 w-10 text-red-500" />
                    )}
                </div>
                <CardTitle className="text-2xl font-bold text-gray-900">
                    {isSuccess ? 'Payment Successful!' : 'Payment Failed'}
                </CardTitle>
                <CardDescription className="text-gray-600">
                    {isSuccess 
                        ? 'Your application fee has been paid successfully.' 
                        : 'We could not process your payment.'}
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6 pt-6">
                <div className="bg-gray-50 rounded-lg p-4 space-y-3 border border-gray-100">
                    <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-500 font-medium">Transaction ID</span>
                        <span className="text-gray-900 font-mono">{txnid || 'N/A'}</span>
                    </div>
                    {isSuccess && (
                    <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-500 font-medium">Amount Paid</span>
                        <span className="text-green-600 font-bold">₹{amount}</span>
                    </div>
                    )}
                    {isFailure && error && (
                    <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-500 font-medium">Reason</span>
                        <span className="text-red-600 max-w-[200px] truncate text-right" title={error}>{error}</span>
                    </div>
                    )}
                </div>

                <div className="space-y-3">
                    {isSuccess ? (
                        <Button 
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white shadow-md transition-all"
                            onClick={() => router.push('/login')}
                        >
                            Go to Student Portal
                        </Button>
                    ) : (
                        <Button 
                            className="w-full bg-red-600 hover:bg-red-700 text-white shadow-md transition-all"
                            onClick={() => router.push('/apply')}
                        >
                            Try Again
                        </Button>
                    )}
                    <Link href="/" className="block text-center">
                        <Button variant="ghost" className="text-gray-500 hover:text-gray-700 w-full">
                            Return to Home
                        </Button>
                    </Link>
                </div>
            </CardContent>
        </Card>
    )
}

export default function PaymentCompletePage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8 flex items-center justify-center">
            <Suspense fallback={<div className="text-center">Loading payment details...</div>}>
                <PaymentStatusContent />
            </Suspense>
        </div>
    )
}
