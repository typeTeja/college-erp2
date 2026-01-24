'use client'

import { useEffect, useState, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { CheckCircle, Copy, Eye, EyeOff, CreditCard, Banknote, DollarSign, Download, Lock } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'
import admissionApi from '@/services/admission-api'

interface QuickApplyResponse {
    application_number: string
    portal_username?: string
    portal_password?: string
    message: string
    payment_mode?: string
    fee_amount?: number
    fee_enabled?: boolean
    id: number
}

function ApplySuccessContent() {
    const router = useRouter()
    const searchParams = useSearchParams()
    const { toast } = useToast()
    const [response, setResponse] = useState<QuickApplyResponse | null>(null)
    const [showPassword, setShowPassword] = useState(false)
    const [isPaid, setIsPaid] = useState(false)
    const [downloadingReceipt, setDownloadingReceipt] = useState(false)

    useEffect(() => {
        // Retrieve response from session storage
        const storedResponse = sessionStorage.getItem('quickApplyResponse')
        const status = searchParams.get('status')
        const txnid = searchParams.get('txnid')

        if (storedResponse) {
            const parsedData = JSON.parse(storedResponse)
            setResponse(parsedData)
            
            // Check if payment was just completed or previously marked as not required
            if (status === 'success' || !parsedData.fee_enabled) {
                setIsPaid(true)
                if (status === 'success') {
                    toast({
                        title: "Payment Successful",
                        description: `Transaction ID: ${txnid}`,
                    })
                }
            }
        } else {
            // If no session data but we have success params, we might want to recover.
            // But for now, let's just stick to session storage dependency as per original design.
             console.log('Success Page: No response found in session storage')
        }
    }, [router, searchParams, toast])

    const copyToClipboard = (text: string, label: string) => {
        navigator.clipboard.writeText(text)
        toast({
            title: "Copied!",
            description: `${label} copied to clipboard`,
        })
    }

    const handleDownloadReceipt = async () => {
        if (!response?.application_number) return
        
        setDownloadingReceipt(true)
        try {
            const data = await admissionApi.downloadReceiptPublic(response.application_number)
            if (data.url) {
                window.open(data.url, '_blank')
            } else {
                throw new Error("Receipt URL not found")
            }
        } catch (error) {
            console.error("Receipt download error:", error)
            toast({
                title: "Error",
                description: "Failed to download receipt. Please try logging into the portal.",
                variant: "destructive"
            })
        } finally {
            setDownloadingReceipt(false)
        }
    }

    if (!response) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading...</p>
                </div>
            </div>
        )
    }

    const hasCredentials = response.portal_username && response.portal_password
    // Logic: Requires payment if fee enabled AND not paid yet
    const requiresPayment = response.fee_enabled && !isPaid && !hasCredentials
    // Logic: Show credentials if available OR if paid (they should have received them)
    // Actually, credential display here relies on `response` object. 
    // If backend creates credentials async, they might NOT be in `response` (which came from session storage BEFORE payment).
    // But the message says "You will receive credentials via email". 
    // So we can't show them here if they weren't generated before.
    // We can only show "Check your email".

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100 py-12 px-4 sm:px-6 lg:px-8">
            <Card className="max-w-2xl mx-auto shadow-xl">
                <CardHeader className="text-center bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-t-lg">
                    <div className="flex justify-center mb-4">
                        <CheckCircle className="h-16 w-16" />
                    </div>
                    <CardTitle className="text-3xl font-bold">
                        {isPaid ? "Payment Successful!" : "Application Submitted Successfully!"}
                    </CardTitle>
                    <CardDescription className="text-green-100 text-lg mt-2">
                        {isPaid 
                            ? "Your application fee has been received. Please check your email for login credentials."
                            : response.message}
                    </CardDescription>
                </CardHeader>
                <CardContent className="mt-6 space-y-6">
                    {/* Application Number */}
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-blue-900">Application Number</p>
                                <p className="text-2xl font-bold text-blue-600 mt-1">{response.application_number}</p>
                            </div>
                            <Button
                                variant="outline"
                                size="sm"
                                onClick={() => copyToClipboard(response.application_number, 'Application number')}
                            >
                                <Copy className="h-4 w-4" />
                            </Button>
                        </div>
                    </div>
                    
                    {/* Download Receipt Section */}
                    {isPaid && (
                        <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center justify-between">
                            <div>
                                <h3 className="font-semibold text-green-900">Payment Receipt</h3>
                                <p className="text-sm text-green-700">Download your transaction receipt</p>
                            </div>
                            <Button 
                                onClick={handleDownloadReceipt}
                                disabled={downloadingReceipt}
                                className="bg-green-600 hover:bg-green-700"
                            >
                                <Download className="h-4 w-4 mr-2" />
                                {downloadingReceipt ? "Downloading..." : "Download PDF"}
                            </Button>
                        </div>
                    )}

                    {/* Payment Instructions (if payment required) */}
                    {requiresPayment && (
                        <div className="bg-gradient-to-r from-orange-50 to-yellow-50 border border-orange-200 rounded-lg p-6">
                            <div className="flex items-center gap-2 mb-4">
                                <DollarSign className="h-6 w-6 text-orange-600" />
                                <h3 className="text-lg font-semibold text-orange-900">
                                    Payment Required
                                </h3>
                            </div>

                            <div className="bg-white rounded-lg p-4 mb-4 border border-orange-200">
                                <p className="text-sm text-gray-600 mb-2">Application Fee</p>
                                <p className="text-3xl font-bold text-orange-600">₹{response.fee_amount}</p>
                            </div>

                            {response.payment_mode === 'ONLINE' ? (
                                <div className="space-y-4">
                                    <div className="flex items-center gap-2 text-green-700">
                                        <CreditCard className="h-5 w-5" />
                                        <span className="font-semibold">Online Payment Selected</span>
                                    </div>
                                    <Button
                                        className="w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-bold py-3"
                                        onClick={async () => {
                                            try {
                                                if (!response.id || !response.fee_amount) {
                                                    toast({
                                                        title: "Error",
                                                        description: "Missing application details for payment.",
                                                        variant: "destructive"
                                                    });
                                                    return;
                                                }

                                                toast({
                                                    title: "Initiating Payment",
                                                    description: "Please wait while we redirect you to the payment gateway...",
                                                });

                                                const paymentResponse = await admissionApi.initiatePayment(response.id, response.fee_amount);
                                                
                                                if (paymentResponse.payment_url) {
                                                    window.location.href = paymentResponse.payment_url;
                                                } else {
                                                    throw new Error("No payment URL received");
                                                }
                                            } catch (error) {
                                                console.error("Payment initiation error:", error);
                                                toast({
                                                    title: "Error",
                                                    description: "Failed to initiate payment. Please try again.",
                                                    variant: "destructive"
                                                });
                                            }
                                        }}
                                    >
                                        Proceed to Payment Gateway
                                    </Button>
                                </div>
                            ) : (
                                <div className="space-y-3">
                                    <div className="flex items-center gap-2 text-blue-700">
                                        <Banknote className="h-5 w-5" />
                                        <span className="font-semibold">Offline Payment Selected</span>
                                    </div>
                                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                        <p className="text-sm text-blue-800">
                                            <strong>Payment Instructions:</strong><br />
                                            1. Visit the college admissions office<br />
                                            2. Pay ₹{response.fee_amount} at the counter<br />
                                            3. Collect payment receipt<br />
                                            4. Upload receipt proof in student portal
                                        </p>
                                    </div>
                                </div>
                            )}

                            <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                                <p className="text-xs text-yellow-800">
                                    <strong>📧 After Payment:</strong> You will receive your student portal login credentials via email and SMS once payment is confirmed.
                                </p>
                            </div>
                        </div>
                    )}

                    {/* Portal Credentials (if available from session) */}
                    {hasCredentials && (
                        <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6">
                            <h3 className="text-lg font-semibold text-purple-900 mb-4">
                                🎓 Your Student Portal Credentials
                            </h3>
                            <p className="text-sm text-purple-700 mb-4">
                                Use these credentials to login to the student portal and complete your application.
                            </p>

                            {/* Username */}
                            <div className="mb-4">
                                <div className="flex items-center justify-between bg-white rounded-lg p-3 border border-purple-200">
                                    <div className="flex-1">
                                        <p className="text-xs font-medium text-gray-600">Username</p>
                                        <p className="text-lg font-mono font-semibold text-gray-900">{response.portal_username}</p>
                                    </div>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => copyToClipboard(response.portal_username!, 'Username')}
                                    >
                                        <Copy className="h-4 w-4" />
                                    </Button>
                                </div>
                            </div>

                            {/* Password */}
                            <div>
                                <div className="flex items-center justify-between bg-white rounded-lg p-3 border border-purple-200">
                                    <div className="flex-1">
                                        <p className="text-xs font-medium text-gray-600">Password</p>
                                        <p className="text-lg font-mono font-semibold text-gray-900">
                                            {showPassword ? response.portal_password : '••••••••••••'}
                                        </p>
                                    </div>
                                    <div className="flex gap-2">
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            onClick={() => setShowPassword(!showPassword)}
                                        >
                                            {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                        </Button>
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            onClick={() => copyToClipboard(response.portal_password!, 'Password')}
                                        >
                                            <Copy className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>
                            </div>

                            <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                                <p className="text-xs text-yellow-800">
                                    <strong>⚠️ Important:</strong> Save these credentials securely. They have also been sent to your email and phone number.
                                </p>
                            </div>
                        </div>
                    )}
                    
                    {/* If paid but no credentials in session (e.g. came back from payment gateway) */}
                    {isPaid && !hasCredentials && (
                         <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                            <div className="flex items-start gap-3">
                                <Lock className="h-6 w-6 text-yellow-600 mt-1" />
                                <div>
                                    <h3 className="font-semibold text-yellow-900">Portal Access</h3>
                                    <p className="text-sm text-yellow-800 mt-1">
                                        Your login credentials have been generated and sent to your registered email address and mobile number.
                                        Please check your inbox (and spam folder) to access your student portal.
                                    </p>
                                </div>
                            </div>
                         </div>
                    )}

                    {/* Next Steps */}
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">📋 Next Steps</h3>
                        <ol className="list-decimal list-inside space-y-2 text-sm text-gray-700">
                            {requiresPayment ? (
                                <>
                                    <li>Complete the application fee payment</li>
                                    <li>Wait for payment confirmation email/SMS</li>
                                    <li>Receive your student portal login credentials</li>
                                    <li>Login to the student portal</li>
                                    <li>Complete the remaining application form</li>
                                    <li>Upload required documents</li>
                                </>
                            ) : (
                                <>
                                    <li>Check your email and SMS for login credentials</li>
                                    <li>Login to the student portal using the credentials</li>
                                    <li>Complete the remaining application form</li>
                                    <li>Upload required documents</li>
                                </>
                            )}
                        </ol>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-col sm:flex-row gap-4">
                        {hasCredentials || isPaid ? (
                            <Button
                                className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-3"
                                onClick={() => router.push('/login')}
                            >
                                Login to Student Portal
                            </Button>
                        ) : (
                            <Button
                                variant="outline"
                                className="flex-1 py-3"
                                onClick={() => router.push('/')}
                            >
                                Back to Home
                            </Button>
                        )}
                    </div>

                    {/* Contact Information */}
                    <div className="text-center text-sm text-gray-600 pt-4 border-t">
                        <p>Need help? Contact us at <a href="mailto:admissions@college.edu" className="text-blue-600 hover:underline">admissions@college.edu</a></p>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

export default function ApplySuccessPage() {
    return (
        <Suspense fallback={
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
                <div className="text-center">Loading...</div>
            </div>
        }>
            <ApplySuccessContent />
        </Suspense>
    )
}
