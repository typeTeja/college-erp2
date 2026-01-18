'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Checkbox } from '@/components/ui/checkbox'
import { BookOpen, CheckCircle2, Circle, Plus, FileText, Search, Filter, Trash2, Download, Clock } from 'lucide-react'
import { useLessonPlans, useQuestionBank, useMarkTopicCompleted, useAddQuestion } from '@/hooks/use-academics'
import { useMyProfile } from '@/hooks/use-faculty'
import { TopicStatus, DifficultyLevel, QuestionType } from '@/types/lesson-plan'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function AcademicsPage() {
    const [selectedSubjectId, setSelectedSubjectId] = useState<number | null>(null)
    const [activeTab, setActiveTab] = useState<'syllabus' | 'questions'>('syllabus')

    const { data: facultyProfile } = useMyProfile()
    const { data: lessonPlans } = useLessonPlans(selectedSubjectId || 0)
    const { data: questionBank } = useQuestionBank(selectedSubjectId || 0)

    const markCompletedMutation = useMarkTopicCompleted()
    // const addQuestionMutation = useAddQuestion() // Uncomment when needed

    // Derived data
    const activePlan = lessonPlans?.[0]
    const completedTopics = activePlan?.topics.filter((t: any) => t.status === TopicStatus.COMPLETED).length || 0
    const totalTopics = activePlan?.topics.length || 0
    const progress = totalTopics > 0 ? (completedTopics / totalTopics) * 100 : 0

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6">
            {/* Header */}
            <div className="flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">Academic Management</h1>
                    <p className="text-slate-500 mt-1">Syllabus tracking and question bank repository</p>
                </div>
                <div className="flex gap-3">
                    <select
                        className="h-10 px-4 rounded-xl border border-slate-200 bg-white text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all shadow-sm min-w-[240px]"
                        onChange={(e) => setSelectedSubjectId(Number(e.target.value))}
                        value={selectedSubjectId || ''}
                    >
                        <option value="" disabled>Select Subject</option>
                        {facultyProfile?.subjects?.map((s: any) => (
                            <option key={s.id} value={s.id}>{s.code} - {s.name}</option>
                        ))}
                        {!facultyProfile?.subjects?.length && <option disabled>No subjects assigned</option>}
                    </select>
                </div>
            </div>

            {!selectedSubjectId ? (
                <Card className="border-dashed border-2 bg-slate-50/50">
                    <CardContent className="h-[400px] flex flex-col items-center justify-center text-center">
                        <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mb-4">
                            <BookOpen className="text-blue-500" size={32} />
                        </div>
                        <h3 className="text-lg font-bold text-slate-800">No Subject Selected</h3>
                        <p className="text-slate-500 max-w-xs mx-auto mt-1">Please select a subject from the list to view its syllabus and question bank.</p>
                    </CardContent>
                </Card>
            ) : (
                <>
                    {/* Stats Overview */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <Card className="bg-gradient-to-br from-blue-600 to-blue-700 text-white border-none shadow-lg shadow-blue-200">
                            <CardContent className="pt-6">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <p className="text-blue-100 text-sm font-medium uppercase tracking-wider">Syllabus Completion</p>
                                        <h3 className="text-4xl font-bold mt-2">{Math.round(progress)}%</h3>
                                    </div>
                                    <div className="p-2 bg-white/20 rounded-lg">
                                        <CheckCircle2 size={24} />
                                    </div>
                                </div>
                                <div className="mt-4 w-full bg-white/20 rounded-full h-2 overflow-hidden">
                                    <div className="bg-white h-full transition-all duration-500" style={{ width: `${progress}%` }} />
                                </div>
                                <p className="text-xs text-blue-100 mt-3">{completedTopics} of {totalTopics} topics covered</p>
                            </CardContent>
                        </Card>

                        <Card className="shadow-sm border-slate-200">
                            <CardContent className="pt-6">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Question Bank</p>
                                        <h3 className="text-4xl font-bold mt-2 text-slate-800">{questionBank?.questions?.length || 0}</h3>
                                    </div>
                                    <div className="p-2 bg-slate-100 rounded-lg text-slate-600">
                                        <FileText size={24} />
                                    </div>
                                </div>
                                <p className="text-xs text-slate-400 mt-3">Ready for automated generation</p>
                            </CardContent>
                        </Card>

                        <Card className="shadow-sm border-slate-200">
                            <CardContent className="pt-6">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Estimated Hours</p>
                                        <h3 className="text-4xl font-bold mt-2 text-slate-800">{activePlan?.total_hours_planned || 0}</h3>
                                    </div>
                                    <div className="p-2 bg-slate-100 rounded-lg text-slate-600">
                                        <Clock size={24} />
                                    </div>
                                </div>
                                <p className="text-xs text-slate-400 mt-3">Planned for current semester</p>
                            </CardContent>
                        </Card>
                    </div>

                    {/* Tabs */}
                    <div className="flex border-b border-slate-200">
                        <button
                            onClick={() => setActiveTab('syllabus')}
                            className={`px-6 py-3 text-sm font-bold transition-all border-b-2 ${activeTab === 'syllabus' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
                        >
                            Syllabus Tracker
                        </button>
                        <button
                            onClick={() => setActiveTab('questions')}
                            className={`px-6 py-3 text-sm font-bold transition-all border-b-2 ${activeTab === 'questions' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
                        >
                            Question Bank
                        </button>
                    </div>

                    {/* Content */}
                    {activeTab === 'syllabus' ? (
                        <div className="space-y-4">
                            {!activePlan ? (
                                <Card className="border-dashed border-2 text-center py-12">
                                    <p className="text-slate-400">No lesson plan found for this subject.</p>
                                    <Button className="mt-4" variant="outline">Create Lesson Plan</Button>
                                </Card>
                            ) : (
                                <div className="grid gap-4">
                                    {activePlan.topics.sort((a: any, b: any) => a.unit_number - b.unit_number).map((topic: any) => (
                                        <Card key={topic.id} className={`transition-all ${topic.status === TopicStatus.COMPLETED ? 'bg-slate-50 opacity-75' : 'hover:shadow-md'}`}>
                                            <CardContent className="p-4 flex items-center gap-4">
                                                <div className={`p-2 rounded-full ${topic.status === TopicStatus.COMPLETED ? 'bg-green-100 text-green-600' : 'bg-slate-100 text-slate-400'}`}>
                                                    {topic.status === TopicStatus.COMPLETED ? <CheckCircle2 size={18} /> : <Circle size={18} />}
                                                </div>
                                                <div className="flex-1">
                                                    <div className="flex items-center gap-2">
                                                        <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded uppercase">Unit {topic.unit_number}</span>
                                                        <h4 className="font-bold text-slate-800">{topic.title}</h4>
                                                    </div>
                                                    <p className="text-sm text-slate-500 mt-1">{topic.description}</p>
                                                </div>
                                                <div className="flex items-center gap-4 text-right">
                                                    <div>
                                                        <p className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Planned Date</p>
                                                        <p className="text-sm text-slate-600 font-medium">{topic.planned_date || '--'}</p>
                                                    </div>
                                                    {topic.status !== TopicStatus.COMPLETED ? (
                                                        <Button
                                                            variant="outline"
                                                            size="sm"
                                                            onClick={() => markCompletedMutation.mutate(topic.id)}
                                                            disabled={markCompletedMutation.isPending}
                                                        >
                                                            Mark Done
                                                        </Button>
                                                    ) : (
                                                        <div className="text-green-600 text-xs font-bold flex items-center gap-1">
                                                            <CheckCircle2 size={12} />
                                                            Done {topic.completion_date}
                                                        </div>
                                                    )}
                                                </div>
                                            </CardContent>
                                        </Card>
                                    ))}
                                </div>
                            )}
                        </div>
                    ) : (
                        <Card className="overflow-hidden border-slate-200">
                            <CardHeader className="bg-slate-50/50 border-b border-slate-200 flex flex-row items-center justify-between">
                                <div>
                                    <CardTitle className="text-sm font-bold uppercase text-slate-600">Repository</CardTitle>
                                    <CardDescription>Manage questions for automatic paper generation</CardDescription>
                                </div>
                                <div className="flex gap-2">
                                    <Button variant="outline" size="sm">
                                        <Download size={14} className="mr-2" /> Export PDF
                                    </Button>
                                    <Button size="sm">
                                        <Plus size={14} className="mr-2" /> Add Question
                                    </Button>
                                </div>
                            </CardHeader>
                            <CardContent className="p-0">
                                <div className="divide-y divide-slate-100">
                                    {(questionBank?.questions || []).length === 0 ? (
                                        <div className="p-12 text-center text-slate-400">
                                            <FileText size={32} className="mx-auto mb-2 opacity-20" />
                                            <p className="text-sm">No questions added yet.</p>
                                        </div>
                                    ) : (
                                        questionBank?.questions.map((q: any) => (
                                            <div key={q.id} className="p-4 hover:bg-slate-50 transition-colors flex gap-4">
                                                <div className="flex flex-col items-center gap-1 shrink-0 pt-1">
                                                    <Badge variant="outline" className="text-[10px] uppercase font-bold text-slate-500">{q.type}</Badge>
                                                    <span className="text-xs font-bold text-slate-700">{q.marks}M</span>
                                                </div>
                                                <div className="flex-1">
                                                    <p className="text-slate-800 text-sm leading-relaxed">{q.text}</p>
                                                    <div className="flex gap-4 mt-2">
                                                        <div className="flex items-center gap-1">
                                                            <div className={`w-2 h-2 rounded-full ${q.difficulty === DifficultyLevel.EASY ? 'bg-green-500' : q.difficulty === DifficultyLevel.MEDIUM ? 'bg-yellow-500' : 'bg-red-500'}`} />
                                                            <span className="text-[10px] text-slate-500 font-bold uppercase">{q.difficulty}</span>
                                                        </div>
                                                        {q.answer_key && (
                                                            <span className="text-[10px] text-blue-600 font-bold uppercase">Answered</span>
                                                        )}
                                                    </div>
                                                </div>
                                                <div className="flex items-start gap-1">
                                                    <Button variant="outline" size="sm" className="h-8 w-8 p-0 text-slate-400 hover:text-red-600">
                                                        <Trash2 size={14} />
                                                    </Button>
                                                </div>
                                            </div>
                                        ))
                                    )}
                                </div>
                            </CardContent>
                        </Card>
                    )}
                </>
            )}
        </div>
    )
}


