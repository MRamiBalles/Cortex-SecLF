"use client"

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/src/components/ui/card"
import { Button } from "@/src/components/ui/button"
import { Badge } from "@/src/components/ui/badge"
import { Progress } from "@/src/components/ui/progress"
import { SearchCode, Zap, AlertTriangle, CheckCircle2, BarChart3, Binary } from 'lucide-react'

interface GapReport {
    total_docs: number
    red_blue_balance: { red: number, blue: number, neutral: number }
    topic_coverage: { [key: string]: number }
    missing_topics: { topic: string, count: number, status: string }[]
}

export default function GapDashboard() {
    const [report, setReport] = useState<GapReport | null>(null)
    const [loading, setLoading] = useState(true)
    const [patching, setPatching] = useState(false)

    const fetchGaps = async () => {
        setLoading(true)
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/gaps/analyze`)
            const data = await res.json()
            setReport(data)
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchGaps()
    }, [])

    const triggerAutoPatch = async () => {
        setPatching(true)
        try {
            await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/bridge/auto-patch`, {
                method: "POST"
            })
            alert("HIVE Bridge: Research mission dispatched. Check Scientist Lab.")
        } catch (e) {
            console.error(e)
        } finally {
            setPatching(false)
        }
    }

    if (!report && loading) return <div className="p-20 text-center text-cyan-500 animate-pulse">Scanning Archive Coverage...</div>

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6 max-w-7xl mx-auto">

            {/* 1. HEATMAP & TOPICS */}
            <div className="lg:col-span-2 space-y-6">
                <Card className="bg-neutral-900 border-neutral-800">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-orange-400">
                            <BarChart3 size={20} /> TOPIC COVERAGE HEATMAP
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        {report && Object.entries(report.topic_coverage).map(([topic, count]) => (
                            <div key={topic} className={`p-4 rounded border transition-all ${count > 0 ? 'bg-neutral-800/40 border-neutral-700' : 'bg-red-950/20 border-red-900/50'}`}>
                                <div className="text-[10px] uppercase text-neutral-500 mb-1 font-mono">{topic}</div>
                                <div className="flex items-end justify-between">
                                    <div className={`text-2xl font-black ${count > 0 ? 'text-neutral-200' : 'text-red-500'}`}>{count}</div>
                                    <div className="text-[10px] font-mono text-neutral-600">DOCS</div>
                                </div>
                                <Progress value={Math.min(count * 20, 100)} className="h-1 mt-2" />
                            </div>
                        ))}
                    </CardContent>
                </Card>

                <Card className="bg-neutral-900 border-neutral-800">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-cyan-400">
                            <Binary size={20} /> RED / BLUE ASYMMETRY
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="flex justify-between text-sm mb-2 font-mono">
                            <span className="text-red-500">OFFENSIVE (RED): {report?.red_blue_balance.red}</span>
                            <span className="text-blue-500">DEFENSIVE (BLUE): {report?.red_blue_balance.blue}</span>
                        </div>
                        <div className="flex h-8 w-full rounded-full overflow-hidden bg-neutral-800 border-2 border-neutral-800">
                            <div
                                className="bg-red-600 h-full transition-all duration-1000 shadow-[0_0_15px_rgba(220,38,38,0.5)]"
                                style={{ width: `${(report?.red_blue_balance.red || 0) / (report?.total_docs || 1) * 100}%` }}
                            ></div>
                            <div
                                className="bg-neutral-700 h-full"
                                style={{ width: `${(report?.red_blue_balance.neutral || 0) / (report?.total_docs || 1) * 100}%` }}
                            ></div>
                            <div
                                className="bg-blue-600 h-full transition-all duration-1000 shadow-[0_0_15px_rgba(37,99,235,0.5)]"
                                style={{ width: `${(report?.red_blue_balance.blue || 0) / (report?.total_docs || 1) * 100}%` }}
                            ></div>
                        </div>
                        <p className="text-xs text-neutral-500 italic text-center">
                            Goal: Symmetric balance across all operational pillars.
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* 2. CRITICAL GAPS & AUTO-PATCH */}
            <div className="space-y-6">
                <Card className="bg-black border-red-900 shadow-[0_0_30px_rgba(153,27,27,0.2)]">
                    <CardHeader className="bg-red-950/20 border-b border-red-900/50">
                        <CardTitle className="text-red-500 flex items-center gap-2 uppercase tracking-tighter">
                            <AlertTriangle size={18} /> Critical Incursions / Gaps
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="p-0 scrollbar-thin scrollbar-thumb-red-900 border-b border-red-900/30 max-h-[400px] overflow-y-auto">
                        {report?.missing_topics.length === 0 ? (
                            <div className="p-8 text-center">
                                <CheckCircle2 size={40} className="text-green-500 mx-auto mb-2" />
                                <p className="text-sm text-neutral-400">Knowledge Base Saturated</p>
                            </div>
                        ) : (
                            report?.missing_topics.map((gap, i) => (
                                <div key={i} className="p-4 border-b border-red-900/20 hover:bg-red-950/10 transition-colors group">
                                    <div className="flex justify-between items-start mb-1">
                                        <div className="text-sm font-bold text-red-200 group-hover:text-red-100">{gap.topic}</div>
                                        <Badge variant="destructive" className="text-[8px] bg-red-900/50">{gap.status}</Badge>
                                    </div>
                                    <div className="text-[10px] text-red-700 font-mono italic">
                                        CURRENT COUNT: {gap.count} // REQ: 3
                                    </div>
                                </div>
                            ))
                        )}
                    </CardContent>
                    <div className="p-4 bg-red-950/10">
                        <Button
                            className="w-full bg-red-600 hover:bg-red-700 text-white font-black h-12 gap-2 shadow-[0_0_20px_rgba(220,38,38,0.4)]"
                            onClick={triggerAutoPatch}
                            disabled={patching || report?.missing_topics.length === 0}
                        >
                            <Zap size={20} className={patching ? 'animate-bounce' : ''} />
                            {patching ? "PATCHING..." : "TRIGGER AUTO-PATCH"}
                        </Button>
                    </div>
                </Card>

                <Card className="bg-neutral-900 border-neutral-800">
                    <CardHeader>
                        <CardTitle className="text-sm text-neutral-400">SYSTEM STATS</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2 font-mono text-xs">
                        <div className="flex justify-between">
                            <span className="text-neutral-600">TOTAL DOCUMENTS:</span>
                            <span className="text-neutral-300">{report?.total_docs}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-neutral-600">HIVE BRIDGE:</span>
                            <span className="text-green-500">OPERATIONAL</span>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
