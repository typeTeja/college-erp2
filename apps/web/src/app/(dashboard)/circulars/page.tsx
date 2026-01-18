'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
    Megaphone, Search, Filter, Plus, FileText,
    Calendar, User, Download, ExternalLink,
    Clock, Tag, AlertCircle
} from 'lucide-react'
import { useCirculars } from '@/hooks/use-circulars'
import { CircularTarget } from '@/types/communication'

export default function CircularsPage() {
    const [searchQuery, setSearchQuery] = useState('')
    const { data: circulars, isLoading, error } = useCirculars()

    const filteredCirculars = circulars?.filter((c: any) =>
        c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.content.toLowerCase().includes(searchQuery.toLowerCase())
    )

    return (
        <div className="p-6 max-w-5xl mx-auto space-y-6">
            <div className="flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
                        <Megaphone className="text-blue-600" />
                        Circulars & Notices
                    </h1>
                    <p className="text-slate-500 mt-1">Institutional announcements and official communications</p>
                </div>
                <Button className="gap-2 bg-blue-600 hover:bg-blue-700">
                    <Plus size={18} /> Post Circular
                </Button>
            </div>

            <Card className="border-slate-200">
                <CardContent className="p-4 flex flex-col md:flex-row gap-4">
                    <div className="flex-1 relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                        <Input
                            placeholder="Search notices, keywords..."
                            className="pl-10"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                    <Button variant="outline" className="gap-2">
                        <Filter size={18} /> All Categories
                    </Button>
                </CardContent>
            </Card>

            <div className="space-y-4">
                {isLoading ? (
                    <div className="py-12 text-center text-slate-400">Loading circulars...</div>
                ) : filteredCirculars?.length === 0 ? (
                    <div className="py-12 text-center text-slate-400">No active circulars found.</div>
                ) : (
                    filteredCirculars?.map((circular: any) => (
                        <Card key={circular.id} className="border-slate-200 hover:shadow-md transition-shadow">
                            <CardHeader className="pb-3">
                                <div className="flex justify-between items-start">
                                    <div className="space-y-1">
                                        <Badge className="bg-blue-50 text-blue-700 hover:bg-blue-100 border-none px-2 py-0 text-[10px] uppercase tracking-wider">
                                            {circular.target_type.replace('_', ' ')}
                                        </Badge>
                                        <CardTitle className="text-xl text-slate-800">{circular.title}</CardTitle>
                                    </div>
                                    <div className="text-right text-xs text-slate-400">
                                        <div className="flex items-center gap-1 justify-end">
                                            <Calendar size={12} />
                                            {new Date(circular.published_at).toLocaleDateString()}
                                        </div>
                                        <div className="flex items-center gap-1 mt-1 justify-end">
                                            <Clock size={12} />
                                            {new Date(circular.published_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </div>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <p className="text-slate-600 whitespace-pre-wrap leading-relaxed">
                                    {circular.content}
                                </p>

                                <div className="flex items-center justify-between pt-4 border-t border-slate-50">
                                    <div className="flex items-center gap-4">
                                        {circular.attachment_url && (
                                            <Button variant="outline" size="sm" className="gap-2 text-blue-600 border-blue-100 bg-blue-50/50">
                                                <FileText size={16} /> Attachment.pdf
                                            </Button>
                                        )}
                                        <div className="flex items-center gap-2 text-xs text-slate-400">
                                            <User size={14} />
                                            Posted by Admin
                                        </div>
                                    </div>
                                    <Button variant="ghost" size="sm" className="text-slate-400 hover:text-blue-600">
                                        <ExternalLink size={16} />
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))
                )}
            </div>
        </div>
    )
}
