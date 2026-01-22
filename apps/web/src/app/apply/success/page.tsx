'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { CheckCircle, Copy, Eye, EyeOff } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface QuickApplyResponse {
    application_number: string
    portal_username?: string
    portal_password?: string
    message: string
}

export default function ApplySuccessPage() {
    const router = useRouter()
    const { toast } = useToast()
    const [response, setResponse] = useState<QuickApplyResponse | null>(null)
    const [showPassword, setShowPassword] = useState(false)

    useEffect(() => {
        // Retrieve response from session storage
        const storedResponse = sessionStorage.getItem('quickApplyResponse')
        if (storedResponse) {
            setResponse(JSON.parse(storedResponse))
            // Clear from session storage after reading
            sessionStorage.removeItem('quickApplyResponse')
        } else {
            // Redirect to apply page if no response found
            router.push('/apply')
        }
    }, [router])

    const copyToClipboard = (text: string, label: string) => {
        navigator.clipboard.writeText(text)
        toast({
            title: "Copied!",
            description: `${label} copied to clipboard`,
        })
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

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100 py-12 px-4 sm:px-6 lg:px-8">
            <Card className="max-w-2xl mx-auto shadow-xl">
                <CardHeader className="text-center bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-t-lg">
                    <div className="flex justify-center mb-4">
                        <CheckCircle className="h-16 w-16" />
                    </div>
                    <CardTitle className="text-3xl font-bold">Application Submitted Successfully!</CardTitle>
                    <CardDescription className="text-green-100 text-lg mt-2">
                        {response.message}
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

                    {/* Portal Credentials */}
                    {response.portal_username && response.portal_password && (
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

                    {/* Next Steps */}
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">📋 Next Steps</h3>
                        <ol className="list-decimal list-inside space-y-2 text-sm text-gray-700">
                            <li>Check your email and SMS for login credentials</li>
                            <li>Login to the student portal using the credentials above</li>
                            <li>Complete the remaining application form</li>
                            <li>Upload required documents</li>
                            <li>Complete payment (if applicable)</li>
                        </ol>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-col sm:flex-row gap-4">
                        <Button
                            className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-3"
                            onClick={() => router.push('/auth/login')}
                        >
                            Login to Student Portal
                        </Button>
                        <Button
                            variant="outline"
                            className="flex-1 py-3"
                            onClick={() => router.push('/')}
                        >
                            Back to Home
                        </Button>
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
