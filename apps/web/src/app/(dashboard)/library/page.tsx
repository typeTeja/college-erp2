'use client'

import { useState } from 'react'
import {
    BookOpen, Search, Filter, Plus,
    Book as BookIcon, User, Calendar,
    CheckCircle, XCircle, AlertCircle,
    Info
} from 'lucide-react'
import { useBooks, useIssueBook } from '@/hooks/use-library'
import { BookStatus, Book } from '@/types/library'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog'

export default function LibraryPage() {
    const [searchTerm, setSearchTerm] = useState('')
    const [isIssueOpen, setIsIssueOpen] = useState(false)
    const [selectedBook, setSelectedBook] = useState<Book | null>(null)
    const [issueData, setIssueData] = useState({
        studentId: '',
        dueDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // Default 14 days
    })

    const { data: books, isLoading, error } = useBooks({ search: searchTerm })
    const issueMutation = useIssueBook()

    const handleIssueSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!selectedBook) return

        try {
            await issueMutation.mutateAsync({
                book_id: selectedBook.id,
                member_id: parseInt(issueData.studentId),
                due_date: issueData.dueDate
            })
            setIsIssueOpen(false)
            setIssueData({ ...issueData, studentId: '' })
            setSelectedBook(null)
            // toast({ title: "Success", description: "Book issued successfully" })
        } catch (error) {
            // toast({ variant: "destructive", title: "Error", description: "Failed to issue book" })
        }
    }

    const stats = [
        { label: 'Total Books', value: books?.length || 0, icon: <BookOpen className="text-blue-600" /> },
        { label: 'Available', value: books?.filter((b: Book) => b.status === BookStatus.AVAILABLE).length || 0, icon: <CheckCircle className="text-green-600" /> },
        { label: 'Issued', value: books?.filter((b: Book) => b.status === BookStatus.ISSUED).length || 0, icon: <Info className="text-yellow-600" /> },
        { label: 'Waitlist', value: 0, icon: <AlertCircle className="text-purple-600" /> },
    ]

    const getStatusVariant = (status: BookStatus): "success" | "warning" | "danger" | "info" | "default" => {
        switch (status) {
            case BookStatus.AVAILABLE: return "success"
            case BookStatus.ISSUED: return "info"
            case BookStatus.DAMAGED: return "warning"
            case BookStatus.LOST: return "danger"
            default: return "default"
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 font-outfit">Library Management</h1>
                    <p className="text-slate-500 mt-1">Catalog and circulation tracking</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline">
                        <Plus className="w-4 h-4 mr-2" />
                        Add Book
                    </Button>
                    <Button>
                        <BookIcon className="w-4 h-4 mr-2" />
                        Issue Book
                    </Button>
                </div>
            </div>

            {/* Stats */}
            {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    {[...Array(4)].map((_, i) => (
                        <div key={i} className="bg-white p-6 rounded-xl border">
                            <Skeleton className="h-20 w-full" />
                        </div>
                    ))}
                </div>
            ) : error ? (
                <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                        Failed to load library data. Please try again later.
                    </AlertDescription>
                </Alert>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    {stats.map((stat, i) => (
                        <div key={i} className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
                            <div className="p-3 bg-slate-50 rounded-lg">
                                {stat.icon}
                            </div>
                            <div>
                                <p className="text-sm font-medium text-slate-500">{stat.label}</p>
                                <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Catalog */}
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                <div className="p-4 border-b border-slate-200 bg-slate-50 flex flex-col md:flex-row gap-4 justify-between">
                    <div className="relative flex-1 max-w-md">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
                        <input
                            type="text"
                            placeholder="Search by title, author, or ISBN..."
                            className="w-full pl-10 pr-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="flex gap-2">
                        <Button variant="outline" size="sm">
                            <Filter className="w-4 h-4 mr-2" />
                            Filter
                        </Button>
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="bg-slate-50 border-b border-slate-200">
                                <th className="px-6 py-4 text-xs font-semibold text-slate-600 uppercase tracking-wider">Book Details</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-600 uppercase tracking-wider">ISBN</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-600 uppercase tracking-wider">Category</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-600 uppercase tracking-wider">Copies</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-600 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-600 uppercase tracking-wider text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-200">
                            {isLoading ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-8 text-center text-slate-500 animate-pulse">Loading catalog...</td>
                                </tr>
                            ) : books?.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-8 text-center text-slate-500">No books found matching your search.</td>
                                </tr>
                            ) : books?.map((book: Book) => (
                                <tr key={book.id} className="hover:bg-slate-50 transition-colors">
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col">
                                            <span className="text-sm font-semibold text-slate-900">{book.title}</span>
                                            <span className="text-xs text-slate-500">{book.author}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-sm text-slate-600 font-mono">{book.isbn}</td>
                                    <td className="px-6 py-4">
                                        <span className="text-sm text-slate-600">{book.category || 'N/A'}</span>
                                    </td>
                                    <td className="px-6 py-4 text-sm text-slate-600">
                                        {book.available_copies} / {book.total_copies}
                                    </td>
                                    <td className="px-6 py-4">
                                        <Badge variant={getStatusVariant(book.status)}>
                                            {book.status}
                                        </Badge>
                                    </td>
                                    <td className="px-6 py-4 text-right space-x-2">
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => {
                                                setSelectedBook(book)
                                                setIsIssueOpen(true)
                                            }}
                                            disabled={book.status !== BookStatus.AVAILABLE}
                                        >
                                            Issue
                                        </Button>
                                        <Button variant="outline" size="sm">Edit</Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Issue Book Modal */}
            <Dialog open={isIssueOpen} onOpenChange={setIsIssueOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Issue Book</DialogTitle>
                        <DialogDescription>
                            Lending "{selectedBook?.title}" to a student.
                        </DialogDescription>
                    </DialogHeader>
                    <form onSubmit={handleIssueSubmit} className="space-y-4" method="POST">
                        <div className="space-y-2">
                            <Label htmlFor="studentId">Student ID</Label>
                            <Input
                                id="studentId"
                                placeholder="Enter Student ID..."
                                required
                                value={issueData.studentId}
                                onChange={(e) => setIssueData({ ...issueData, studentId: e.target.value })}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="dueDate">Due Date</Label>
                            <Input
                                id="dueDate"
                                type="date"
                                required
                                value={issueData.dueDate}
                                onChange={(e) => setIssueData({ ...issueData, dueDate: e.target.value })}
                            />
                        </div>
                        <DialogFooter>
                            <Button type="button" variant="outline" onClick={() => setIsIssueOpen(false)}>Cancel</Button>
                            <Button type="submit" disabled={issueMutation.isPending}>
                                {issueMutation.isPending ? 'Processing...' : 'Confirm Issue'}
                            </Button>
                        </DialogFooter>
                    </form>
                </DialogContent>
            </Dialog>
        </div>
    )
}
