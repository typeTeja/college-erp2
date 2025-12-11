'use client'

import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'

export default function AdmissionsPage() {
    const [formData, setFormData] = useState({
        applicantName: '',
        email: '',
        mobile: '',
        courseApplied: ''
    })

    // Mock API call
    const mutation = useMutation({
        mutationFn: async (data: typeof formData) => {
            const res = await fetch('http://localhost:3001/admissions/apply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            if (!res.ok) throw new Error('Failed')
            return res.json()
        }
    })

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        mutation.mutate(formData)
    }

    return (
        <div className="max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold mb-6">New Admission Application</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium mb-1">Applicant Name</label>
                    <input
                        type="text"
                        className="w-full p-2 border rounded"
                        value={formData.applicantName}
                        onChange={e => setFormData({ ...formData, applicantName: e.target.value })}
                        required
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">Email</label>
                    <input
                        type="email"
                        className="w-full p-2 border rounded"
                        value={formData.email}
                        onChange={e => setFormData({ ...formData, email: e.target.value })}
                        required
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">Mobile</label>
                    <input
                        type="tel"
                        className="w-full p-2 border rounded"
                        value={formData.mobile}
                        onChange={e => setFormData({ ...formData, mobile: e.target.value })}
                        required
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">Course Applied</label>
                    <select
                        className="w-full p-2 border rounded"
                        value={formData.courseApplied}
                        onChange={e => setFormData({ ...formData, courseApplied: e.target.value })}
                        required
                    >
                        <option value="">Select Course</option>
                        <option value="CSE">CSE</option>
                        <option value="ECE">ECE</option>
                        <option value="MECH">MECH</option>
                    </select>
                </div>

                <button
                    type="submit"
                    className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 disabled:opacity-50"
                    disabled={mutation.isPending}
                >
                    {mutation.isPending ? 'Submitting...' : 'Submit Application'}
                </button>

                {mutation.isSuccess && <p className="text-green-600">Application Submitted!</p>}
                {mutation.isError && <p className="text-red-600">Error submitting application.</p>}
            </form>
        </div>
    )
}
