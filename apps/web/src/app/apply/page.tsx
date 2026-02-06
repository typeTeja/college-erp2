'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { admissionApi } from '@/services/admission-api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'
import { useQuery } from '@tanstack/react-query'
import {
    GraduationCap,
    User,
    Mail,
    Phone,
    MapPin,
    CreditCard,
    ChevronRight,
    ArrowRight,
    CheckCircle2,
    Calendar,
    BookOpen,
    Globe,
    Building2,
    Briefcase
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface Program {
    id: number
    name: string
}

export default function QuickApplyPage() {
    const router = useRouter()
    const { toast } = useToast()

    // Fetch programs - MODIFIED: Using public endpoint
    const { data: programs, isLoading: programsLoading } = useQuery<Program[]>({
        queryKey: ['public-programs'],
        queryFn: () => admissionApi.getPublicPrograms()
    })

    // Fetch payment configuration
    const { data: paymentConfig } = useQuery({
        queryKey: ['payment-config'],
        queryFn: () => admissionApi.getPaymentConfig(),
    })

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        gender: '',
        program_id: '',
        state: '',
        board: '',
        group_of_study: '',
        payment_mode: 'ONLINE', // Default to online
    })

    const [isSubmitting, setIsSubmitting] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setIsSubmitting(true)

        try {
            // Call Quick Apply API
            const response = await admissionApi.quickApplyV2({
                name: formData.name,
                email: formData.email,
                phone: formData.phone,
                gender: formData.gender,
                program_id: parseInt(formData.program_id),
                state: formData.state,
                board: formData.board,
                group_of_study: formData.group_of_study
            })

            // Store credentials and payment info in session storage for success page
            const storageData = {
                ...response,
                payment_mode: formData.payment_mode,
                fee_amount: paymentConfig?.fee_amount || 0,
                fee_enabled: paymentConfig?.fee_enabled || false
            }
            console.log('Form Submit: Saving to session storage:', storageData)
            sessionStorage.setItem('quickApplyResponse', JSON.stringify(storageData))

            // Payment Logic
            if (paymentConfig?.fee_enabled && formData.payment_mode === 'ONLINE') {
                console.log('Initiating Payment...');
                try {
                    const paymentResp = await admissionApi.initiatePayment(response.id);
                    if (paymentResp.status === 'success' && paymentResp.payment_url) {
                        console.log('Redirecting to Payment Gateway:', paymentResp.payment_url);
                        window.location.href = paymentResp.payment_url;
                        return;
                    } else {
                        throw new Error(paymentResp.error || "Payment initiation failed");
                    }
                } catch (payErr: any) {
                    console.error("Payment Error:", payErr);
                    toast({
                        title: "Payment Error",
                        description: payErr.message || "Could not initiate payment. Please try again from dashboard.",
                        variant: "destructive"
                    });
                    router.push('/apply/success?status=payment_failed');
                    return;
                }
            }

            toast({
                title: "Application Submitted!",
                description: response.message,
            })

            console.log('Form Submit: Redirecting to success page')
            router.push('/apply/success')
        } catch (error: any) {
            console.error('Quick Apply error:', error)
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to submit application. Please try again.",
                variant: "destructive"
            })
        } finally {
            setIsSubmitting(false)
        }
    }

    return (
        <div className="min-h-screen bg-[#F8FAFC] flex flex-col items-center justify-center p-4 md:p-8">
            <div className="w-full max-w-4xl grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">

                {/* Left Side: Info & Marketing */}
                <div className="lg:col-span-4 space-y-6 pt-8">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-sm font-medium">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Admissions Open 2026-27</span>
                    </div>

                    <h1 className="text-4xl font-extrabold tracking-tight text-slate-900">
                        Start Your <span className="text-blue-600">Journey</span> With Us.
                    </h1>

                    <p className="text-slate-600 text-lg">
                        Complete your application in under 5 minutes. Get instant access to the student portal upon submission.
                    </p>

                    <div className="space-y-4 pt-4">
                        <div className="flex items-start gap-4">
                            <div className="w-10 h-10 rounded-lg bg-white shadow-sm border flex items-center justify-center text-blue-600">
                                <CheckCircle2 className="w-5 h-5" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-slate-900">Fast Process</h3>
                                <p className="text-sm text-slate-500">Simplified 3-step application journey.</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-4">
                            <div className="w-10 h-10 rounded-lg bg-white shadow-sm border flex items-center justify-center text-blue-600">
                                <Globe className="w-5 h-5" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-slate-900">Digital First</h3>
                                <p className="text-sm text-slate-500">Everything from fee to docs is online.</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-4">
                            <div className="w-10 h-10 rounded-lg bg-white shadow-sm border flex items-center justify-center text-blue-600">
                                <CreditCard className="w-5 h-5" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-slate-900">Secure Payment</h3>
                                <p className="text-sm text-slate-500">Integrated global payment gateways.</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Side: Form */}
                <Card className="lg:col-span-8 border-none shadow-2xl overflow-hidden">
                    <CardHeader className="bg-slate-900 text-white p-8">
                        <div className="flex items-center gap-3 mb-2">
                            <div className="p-2 rounded-lg bg-blue-600/20 text-blue-400">
                                <GraduationCap className="w-6 h-6" />
                            </div>
                            <CardTitle className="text-2xl font-bold text-white">Admission Application</CardTitle>
                        </div>
                        <CardDescription className="text-slate-400">
                            Fill in your basic details to get started. Asterisk (*) denotes required fields.
                        </CardDescription>
                    </CardHeader>

                    <CardContent className="p-8">
                        <form onSubmit={handleSubmit} className="space-y-8">

                            {/* Personal Details Section */}
                            <section className="space-y-4">
                                <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
                                    <User className="w-4 h-4 text-blue-600" />
                                    <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500">Personal Information</h3>
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <Label htmlFor="name">Full Name *</Label>
                                        <div className="relative">
                                            <User className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
                                            <Input
                                                id="name"
                                                className="pl-10"
                                                placeholder="Enter your full name"
                                                required
                                                value={formData.name}
                                                onChange={e => setFormData({ ...formData, name: e.target.value })}
                                            />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="email">Email Address *</Label>
                                        <div className="relative">
                                            <Mail className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
                                            <Input
                                                id="email"
                                                type="email"
                                                className="pl-10"
                                                placeholder="your@email.com"
                                                required
                                                value={formData.email}
                                                onChange={e => setFormData({ ...formData, email: e.target.value })}
                                            />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="phone">Mobile Number *</Label>
                                        <div className="relative">
                                            <Phone className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
                                            <Input
                                                id="phone"
                                                className="pl-10"
                                                placeholder="10-digit mobile number"
                                                required
                                                value={formData.phone}
                                                onChange={e => setFormData({ ...formData, phone: e.target.value })}
                                            />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <Label>Gender *</Label>
                                        <Select onValueChange={v => setFormData({ ...formData, gender: v })} required>
                                            <SelectTrigger className="bg-white">
                                                <SelectValue placeholder="Select Gender" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="MALE">Male</SelectItem>
                                                <SelectItem value="FEMALE">Female</SelectItem>
                                                <SelectItem value="OTHER">Other</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                </div>
                            </section>

                            {/* Academic Section */}
                            <section className="space-y-4">
                                <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
                                    <BookOpen className="w-4 h-4 text-blue-600" />
                                    <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500">Academic & Course Selection</h3>
                                </div>
                                <div className="space-y-6">
                                    <div className="space-y-2">
                                        <Label>Course Applying For *</Label>
                                        <Select onValueChange={v => setFormData({ ...formData, program_id: v })} required>
                                            <SelectTrigger className="bg-white h-12 text-blue-700 font-semibold border-blue-100 hover:border-blue-300 transition-colors">
                                                <div className="flex items-center gap-2">
                                                    <GraduationCap className="w-4 h-4" />
                                                    <SelectValue placeholder="Browse available programs" />
                                                </div>
                                            </SelectTrigger>
                                            <SelectContent>
                                                {programsLoading && (
                                                    <div className="p-4 text-center text-sm text-slate-500">
                                                        Loading programs...
                                                    </div>
                                                )}
                                                {programs?.map(p => (
                                                    <SelectItem key={p.id} value={p.id.toString()}>
                                                        {p.name}
                                                    </SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div className="space-y-2">
                                            <Label htmlFor="state">Current State *</Label>
                                            <div className="relative">
                                                <MapPin className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
                                                <Input
                                                    id="state"
                                                    className="pl-10"
                                                    placeholder="State of residence"
                                                    required
                                                    value={formData.state}
                                                    onChange={e => setFormData({ ...formData, state: e.target.value })}
                                                />
                                            </div>
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="board">Board (10+2) *</Label>
                                            <div className="relative">
                                                <Building2 className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
                                                <Input
                                                    id="board"
                                                    className="pl-10"
                                                    placeholder="CBSE / State / IB"
                                                    required
                                                    value={formData.board}
                                                    onChange={e => setFormData({ ...formData, board: e.target.value })}
                                                />
                                            </div>
                                        </div>
                                        <div className="space-y-2 md:col-span-2">
                                            <Label htmlFor="group">Group of Study *</Label>
                                            <div className="relative">
                                                <Briefcase className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
                                                <Input
                                                    id="group"
                                                    className="pl-10"
                                                    placeholder="e.g. MPC, BiPC, Commerce, Arts"
                                                    required
                                                    value={formData.group_of_study}
                                                    onChange={e => setFormData({ ...formData, group_of_study: e.target.value })}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </section>

                            {/* Payment Section */}
                            {paymentConfig?.fee_enabled && (
                                <section className="space-y-4 p-6 rounded-xl bg-blue-50/50 border border-blue-100">
                                    <div className="flex items-center justify-between gap-4 flex-wrap">
                                        <div className="flex items-center gap-3">
                                            <div className="p-2 rounded-lg bg-blue-600 text-white shadow-lg shadow-blue-200">
                                                <CreditCard className="w-5 h-5" />
                                            </div>
                                            <div>
                                                <p className="text-xs font-bold text-blue-600 uppercase tracking-widest">Application Fee</p>
                                                <p className="text-2xl font-black text-slate-900">₹{paymentConfig.fee_amount}</p>
                                            </div>
                                        </div>

                                        <div className="flex-1 min-w-[200px]">
                                            <Label className="text-xs font-bold text-slate-500 mb-1.5 block">Payment Mode</Label>
                                            <Select
                                                value={formData.payment_mode}
                                                onValueChange={(v) => setFormData({ ...formData, payment_mode: v })}
                                            >
                                                <SelectTrigger className="bg-white border-blue-200">
                                                    <SelectValue />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    {paymentConfig.online_enabled && (
                                                        <SelectItem value="ONLINE">
                                                            <div className="flex items-center gap-2">
                                                                <ArrowRight className="h-4 w-4 text-blue-600" />
                                                                <span>Online Payment</span>
                                                            </div>
                                                        </SelectItem>
                                                    )}
                                                    {paymentConfig.offline_enabled && (
                                                        <SelectItem value="OFFLINE">
                                                            <div className="flex items-center gap-2">
                                                                <MapPin className="h-4 w-4 text-slate-600" />
                                                                <span>Pay at College Office</span>
                                                            </div>
                                                        </SelectItem>
                                                    )}
                                                </SelectContent>
                                            </Select>
                                        </div>
                                    </div>
                                    <p className="text-xs text-blue-700/70 italic">
                                        {formData.payment_mode === 'ONLINE'
                                            ? "You'll be safely redirected to our secure payment gateway."
                                            : "Please visit the college office within 3 days to confirm your application."}
                                    </p>
                                </section>
                            )}

                            {/* Submit Button */}
                            <div className="pt-4">
                                <Button
                                    type="submit"
                                    className={cn(
                                        "w-full h-14 text-lg font-bold transition-all duration-300 shadow-xl shadow-blue-100",
                                        "bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800",
                                        "active:scale-[0.98]"
                                    )}
                                    disabled={isSubmitting}
                                >
                                    {isSubmitting ? (
                                        <div className="flex items-center gap-2">
                                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                            <span>Processing...</span>
                                        </div>
                                    ) : (
                                        <div className="flex items-center gap-2">
                                            <span>{paymentConfig?.fee_enabled && formData.payment_mode === 'ONLINE' ? "Proceed to Payment" : "Submit Application"}</span>
                                            <ChevronRight className="w-5 h-5" />
                                        </div>
                                    )}
                                </Button>

                                <p className="text-center text-xs text-slate-400 mt-6">
                                    By submitting, you agree to our <a href="#" className="underline">Terms</a> & <a href="#" className="underline">Admission Policy</a>.
                                </p>
                            </div>
                        </form>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
