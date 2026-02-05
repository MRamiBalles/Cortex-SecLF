"use client"

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/src/components/ui/card"
import { Badge } from "@/src/components/ui/badge"
import { Alert, AlertTitle, AlertDescription } from "@/src/components/ui/alert"
import { AlertTriangle, Shield, Sword, Activity } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie, LineChart, Line } from 'recharts';

interface GapStats {
    total_docs: number
    red_blue_balance: { red: number, blue: number, neutral: number }
    topic_coverage: Record<str, number>
    temporal_distribution: Record<str, number>
    missing_topics: Array<{ topic: string, count: number, status: string }>
}

export default function GapDashboard() {
    const [stats, setStats] = useState<GapStats | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8008'}/gaps/analyze`)
                const data = await res.json()
                setStats(data)
            } catch (e) {
                console.error("Failed to fetch gap stats", e)
            } finally {
                setLoading(false)
            }
        }
        fetchStats()
    }, [])

    if (loading) return <div className="p-10 text-center text-neutral-500 font-mono">Scanning Neural Archive Constraints...</div>
    if (!stats) return <div className="p-10 text-center text-red-500">Failed to load Intelligence Data.</div>

    // Prepare Data for Charts
    const redBlueData = [
        { name: 'Red (Offensive)', value: stats.red_blue_balance.red, color: '#ef4444' }, // Red-500
        { name: 'Blue (Defensive)', value: stats.red_blue_balance.blue, color: '#3b82f6' }, // Blue-500
        { name: 'Neutral', value: stats.red_blue_balance.neutral, color: '#737373' }, // Neutral-500
    ]

    const topicData = Object.entries(stats.topic_coverage).map(([key, value]) => ({
        name: key,
        docs: value
    }))

    const yearData = Object.entries(stats.temporal_distribution)
        .sort((a, b) => Number(a[0]) - Number(b[0]))
        .map(([year, count]) => ({ year, count }))

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 max-w-7xl mx-auto">

            {/* 1. ASYMMETRY VISUALIZER */}
            <Card className="bg-neutral-900 border-neutral-800 col-span-1">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-primary">
                        <Activity size={20} /> Red vs Blue Asymmetry
                    </CardTitle>
                    <CardDescription>Knowledge balance between Attack and Defense.</CardDescription>
                </CardHeader>
                <CardContent className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={redBlueData} layout="vertical" margin={{ left: 20 }}>
                            <XAxis type="number" hide />
                            <YAxis dataKey="name" type="category" width={100} tick={{ fill: '#a3a3a3', fontSize: 12 }} />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#171717', border: '1px solid #404040', color: '#fff' }}
                            />
                            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                                {redBlueData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </CardContent>
            </Card>

            {/* 2. CRITICAL GAPS ALERT */}
            <Card className="bg-neutral-900 border-neutral-800 col-span-1 border-l-4 border-l-red-600">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-red-500">
                        <AlertTriangle size={20} /> Knowledge Gaps (Missing Doctrine)
                    </CardTitle>
                    <CardDescription>Topics with insufficient Ground Truth coverage.</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-3">
                        {stats.missing_topics.length === 0 ? (
                            <div className="text-green-500 flex items-center gap-2">
                                <Shield size={16} /> Full Spectrum Coverage Achieved.
                            </div>
                        ) : (
                            stats.missing_topics.map((gap, i) => (
                                <div key={i} className="flex justify-between items-center p-2 bg-red-950/20 rounded border border-red-900/30">
                                    <span className="font-mono text-sm text-red-200">{gap.topic}</span>
                                    <Badge variant="destructive">{gap.status}</Badge>
                                </div>
                            ))
                        )}
                        {stats.missing_topics.length > 0 && (
                            <p className="text-xs text-neutral-500 mt-4 italic">
                                * Recommendation: Ingest papers on these topics immediately to prevent blind spots.
                            </p>
                        )}
                    </div>
                </CardContent>
            </Card>

            {/* 3. MITRE COVERAGE */}
            <Card className="bg-neutral-900 border-neutral-800 col-span-1 md:col-span-2">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-emerald-500">
                        <Shield size={20} /> MITRE / Topic Coverage
                    </CardTitle>
                    <CardDescription>Document density per security domain.</CardDescription>
                </CardHeader>
                <CardContent className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={topicData}>
                            <XAxis dataKey="name" tick={{ fill: '#a3a3a3', fontSize: 12 }} />
                            <YAxis tick={{ fill: '#a3a3a3' }} />
                            <Tooltip
                                cursor={{ fill: '#262626' }}
                                contentStyle={{ backgroundColor: '#171717', border: '1px solid #404040', color: '#fff' }}
                            />
                            <Bar dataKey="docs" fill="#10b981" radius={[4, 4, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </CardContent>
            </Card>

            {/* 4. OBSOLESCENCE RADAR */}
            <Card className="bg-neutral-900 border-neutral-800 col-span-1 md:col-span-2">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-amber-500">
                        <Activity size={20} /> Temporal Relevance (Obsolescence Check)
                    </CardTitle>
                    <CardDescription>Distribution of knowledge by year. Gaps in 2024-2026 indicate risk.</CardDescription>
                </CardHeader>
                <CardContent className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={yearData}>
                            <XAxis dataKey="year" tick={{ fill: '#a3a3a3' }} />
                            <YAxis tick={{ fill: '#a3a3a3' }} />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#171717', border: '1px solid #404040', color: '#fff' }}
                            />
                            <Line type="monotone" dataKey="count" stroke="#f59e0b" strokeWidth={2} dot={{ fill: '#f59e0b' }} />
                        </LineChart>
                    </ResponsiveContainer>
                </CardContent>
            </Card>

        </div>
    )
}
