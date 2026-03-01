"use client"

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/src/components/ui/card"
import { Button } from "@/src/components/ui/button"
import { Badge } from "@/src/components/ui/badge"
import { Progress } from "@/src/components/ui/progress"
import { SearchCode, Zap, AlertTriangle, CheckCircle2, BarChart3, Binary } from 'lucide-react'

// Define strict interfaces
interface RedBlueBalance {
    red: number
    blue: number
    neutral: number
}

interface MissingTopic {
    topic: string
    count: number
    status: string
}

interface GapReport {
    total_docs: number
    red_blue_balance: RedBlueBalance
    topic_coverage: { [key: string]: number }
    missing_topics: MissingTopic[]
}

export default function GapDashboard() {
    const [report, setReport] = useState<GapReport | null>(null)
    const [loading, setLoading] = useState(true)
    const [patching, setPatching] = useState(false)

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    const fetchGaps = async () => {
        setLoading(true)
        try {
            const res = await fetch(`${API_URL}/gaps/analyze`)
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
    }, [API_URL])

    const triggerAutoPatch = async () => {
        setPatching(true)
        try {
            await fetch(`${API_URL}/bridge/auto-patch`, {
                method: "POST"
            })
            alert("HIVE Bridge: Research mission dispatched. Check Scientist Lab.")
        } catch (e) {
            console.error(e)
        } finally {
            setPatching(false)
        }
    }

    if (loading && !report) return <div className="p-20 text-center text-cyan-500 animate-pulse font-mono uppercase tracking-widest">Scanning Archive Coverage Heatmap...</div>

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6 max-w-7xl mx-auto">

            {/* 1. HEATMAP & TOPICS */}
            <div className="lg:col-span-2 space-y-6">
                <Card className="bg-neutral-900 border-neutral-800">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-orange-400">
                            <BarChart3 size={20} /> TOPIC COVERAGE HEATMAP
                        </CardTitle>
                        <CardDescription>Knowledge frequency across operational domains</CardDescription>
                    </CardHeader>
                    <CardContent className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        {report && Object.entries(report.topic_coverage).map(([topic, count]) => (
                            <div key={topic} className={`p-4 rounded border transition-all duration-500 ${count > 0 ? 'bg-neutral-800/40 border-neutral-700' : 'bg-red-950/20 border-red-900/50'}`}>
                                <div className="text-[10px] uppercase text-neutral-500 mb-1 font-mono tracking-tighter">{topic}</div>
                                <div className="flex items-end justify-between">
                                    <div className={`text-2xl font-black ${count > 0 ? 'text-neutral-200' : 'text-red-500'}`}>{count}</div>
                                    <div className="text-[10px] font-mono text-neutral-600">UNITS</div>
                                </div>
                                <Progress value={Math.min(count * 20, 100)} className="h-1 mt-2 bg-neutral-800" />
                            </div>
                        ))}
                    </CardContent>
                </Card>

                <Card className="bg-neutral-900 border-neutral-800">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-cyan-400">
                            <Binary size={20} /> DOCTRINE ASYMMETRY (RED / BLUE)
                        </CardTitle>
                        <CardDescription>Offensive vs Defensive knowledge balance</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="flex justify-between text-[10px] mb-2 font-mono uppercase tracking-widest">
                            <span className="text-red-500">OFFENSIVE (TRENCH): {report?.red_blue_balance.red}</span>
                            <span className="text-blue-500">DEFENSIVE (DOCTRINE): {report?.red_blue_balance.blue}</span>
                        </div>
                        <div className="flex h-10 w-full rounded-full overflow-hidden bg-neutral-800 border-4 border-neutral-900 shadow-inner">
                            <div
                                className="bg-red-600 h-full transition-all duration-1000 shadow-[0_0_20px_rgba(220,38,38,0.5)]"
                                style={{ width: `${((report?.red_blue_balance.red || 0) / (report?.total_docs || 1)) * 100}%` }}
                            ></div>
                            <div
                                className="bg-neutral-700 h-full"
                                style={{ width: `${((report?.red_blue_balance.neutral || 0) / (report?.total_docs || 1)) * 100}%` }}
                            ></div>
                            <div
                                className="bg-blue-600 h-full transition-all duration-1000 shadow-[0_0_20px_rgba(37,99,235,0.5)]"
                                style={{ width: `${((report?.red_blue_balance.blue || 0) / (report?.total_docs || 1)) * 100}%` }}
                            ></div>
                        </div>
                        <p className="text-[10px] text-neutral-500 italic text-center uppercase tracking-tighter">
                            Mandate: Maintain zero-asymmetry for robust local defense.
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* 2. CRITICAL GAPS & AUTO-PATCH */}
            <div className="space-y-6">
                <Card className="bg-black border-red-900 shadow-[0_0_30px_rgba(153,27,27,0.2)]">
                    <CardHeader className="bg-red-950/20 border-b border-red-900/50">
                        <CardTitle className="text-red-500 flex items-center gap-2 uppercase tracking-tighter font-black">
                            <AlertTriangle size={18} /> ASYMMETRY INCURSIONS
                        </CardTitle>
                        <CardDescription className="text-red-900 text-[10px]">Identified knowledge deficits in the local archive</CardDescription>
                    </CardHeader>
                    <CardContent className="p-0 scrollbar-thin scrollbar-thumb-red-900 border-b border-red-900/30 max-h-[400px] overflow-y-auto">
                        {report?.missing_topics.length === 0 ? (
                            <div className="p-12 text-center">
                                <CheckCircle2 size={48} className="text-green-500 mx-auto mb-4 opacity-50" />
                                <p className="text-xs text-neutral-500 font-mono">ARCHIVE SATURATION: 100%</p>
                            </div>
                        ) : (
                            report?.missing_topics.map((gap, i) => (
                                <div key={i} className="p-4 border-b border-red-900/20 hover:bg-red-950/10 transition-colors group">
                                    <div className="flex justify-between items-start mb-1">
                                        <div className="text-sm font-bold text-red-200 group-hover:text-red-100 uppercase font-mono tracking-tighter">{gap.topic}</div>
                                        <Badge variant="destructive" className="text-[8px] bg-red-900/80 font-mono">{gap.status}</Badge>
                                    </div>
                                    <div className="text-[9px] text-red-700 font-mono italic">
                                        CURRENT_QUANTITY: {gap.count} // REQ_THRESHOLD: 3
                                    </div>
                                </div>
                            ))
                        )}
                    </CardContent>
                    <div className="p-4 bg-red-950/10">
                        <Button
                            className="w-full bg-red-600 hover:bg-red-700 text-white font-black h-12 gap-2 shadow-[0_0_20px_rgba(220,38,38,0.4)] transition-all active:scale-95"
                            onClick={triggerAutoPatch}
                            disabled={patching || report?.missing_topics.length === 0}
                        >
                            <Zap size={20} className={patching ? 'animate-bounce' : ''} />
                            {patching ? "PATCHING LATTICE..." : "TRIGGER AUTONOMOUS PATCH"}
                        </Button>
                    </div>
                </Card>

                <Card className="bg-neutral-900 border-neutral-800">
                    <CardHeader className="py-3">
                        <CardTitle className="text-[10px] text-neutral-500 font-mono uppercase tracking-[0.2em]">Telemetry Base</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2 font-mono text-[10px]">
                        <div className="flex justify-between">
                            <span className="text-neutral-600">ARCHIVE_SIZE:</span>
                            <span className="text-neutral-300">{report?.total_docs} DOCUMENTS</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-neutral-600">HIVE_BRIDGE:</span>
                            <span className="text-green-500">READY</span>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
