"use client"

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/src/components/ui/card"
import { Button } from "@/src/components/ui/button"
import { Input } from "@/src/components/ui/input"
import { Badge } from "@/src/components/ui/badge"
import { ScrollArea } from "@/src/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/src/components/ui/tabs"
import { FlaskConical, CheckCircle2, XCircle, FileText, Cpu, Microscope } from 'lucide-react'

// Types based on Backend API
interface ResearchArtifact {
    hypothesis: { title: string, statement: string, topic: string }
    design: { code: string, language: string, expected_output: string }
    result: { success: boolean, output: string, metrics: any }
    grounding?: string[]
}

interface ReviewArtifact {
    decision: "ACCEPT" | "REJECT" | "REVISE"
    score: string
    comments: string[]
    publication_ready: boolean
}

export default function ResearchLab() {
    const [topic, setTopic] = useState("")
    const [loading, setLoading] = useState(false)
    const [paper, setPaper] = useState<ResearchArtifact | null>(null)
    const [review, setReview] = useState<ReviewArtifact | null>(null)

    const conductResearch = async () => {
        if (!topic) return
        setLoading(true)
        setPaper(null)
        setReview(null)

        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/scientist/research`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ topic })
            })
            const data = await res.json()

            // Map DSG result from backend to simple UI structure
            if (data.nodes) {
                const ideation = data.nodes.ideation
                const realization = data.nodes.realization
                const audit = data.nodes.audit

                setPaper({
                    hypothesis: ideation.content,
                    grounding: ideation.grounding,
                    design: {
                        code: realization.content || "N/A",
                        language: "python",
                        expected_output: "Success"
                    },
                    result: {
                        success: realization.status === "COMPILED",
                        output: realization.trials?.[0]?.logs || "No logs available",
                        metrics: { status: realization.status }
                    }
                })

                setReview({
                    decision: audit.verdict,
                    score: audit.score.toString(),
                    comments: [audit.critique],
                    publication_ready: audit.verdict === "ACCEPT"
                })
            }
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6 max-w-7xl mx-auto h-[calc(100vh-100px)]">

            {/* 1. CONTROLS (Left Col) */}
            <div className="lg:col-span-1 flex flex-col gap-6">
                <Card className="bg-neutral-900 border-neutral-800 shadow-2xl">
                    <CardHeader>
                        <CardTitle className="text-sm font-mono text-neutral-400 flex items-center gap-2">
                            <Microscope size={16} /> HYPOTHESIS GENERATOR
                        </CardTitle>
                        <CardDescription>Initiate autonomous research loop via HIVE.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <Input
                            placeholder="e.g. Log Obfuscation, PQC Migration..."
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            className="bg-black border-neutral-700 font-mono text-sm focus:border-cyan-500 transition-colors"
                        />
                        <Button
                            className="w-full bg-cyan-600 hover:bg-cyan-700 text-white font-bold transition-all hover:tracking-widest"
                            onClick={conductResearch}
                            disabled={loading}
                        >
                            {loading ? "CONDUCTING RESEARCH..." : "START EXPERIMENT"}
                        </Button>
                    </CardContent>
                </Card>

                {/* PEER REVIEW SCORECARD */}
                {review && (
                    <Card className={`border-neutral-800 shadow-xl overflow-hidden transition-all duration-500 ${review.decision === 'ACCEPT' ? 'bg-green-950/10 border-green-900/50' : 'bg-red-950/10 border-red-900/50'}`}>
                        <CardHeader>
                            <CardTitle className="text-sm font-mono flex items-center gap-2">
                                <FileText size={16} /> PEER REVIEW VERDICT
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex items-center justify-between">
                                <span className="text-neutral-400 text-sm">DECISION</span>
                                <Badge className={review.decision === 'ACCEPT' ? 'bg-green-500' : 'bg-red-500'}>
                                    {review.decision}
                                </Badge>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-neutral-400 text-sm">SCORE</span>
                                <span className="text-2xl font-bold font-mono text-neutral-200">{review.score}/10</span>
                            </div>
                            <div className="space-y-2">
                                <p className="text-xs text-neutral-500 uppercase tracking-widest font-bold">Reviewer Critique:</p>
                                {review.comments.map((c, i) => (
                                    <div key={i} className="text-xs text-neutral-300 bg-black/40 p-3 rounded-xl border border-white/5 leading-relaxed italic">
                                        "{c}"
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                )}
            </div>

            {/* 2. PAPER RENDERER (Right Col) */}
            <div className="lg:col-span-2 h-full min-h-0">
                <Card className="bg-neutral-900 border-neutral-800 h-full flex flex-col overflow-hidden shadow-2xl">
                    <CardHeader className="bg-neutral-950 border-b border-neutral-800 py-3">
                        <div className="flex justify-between items-center">
                            <CardTitle className="text-sm font-mono text-cyan-400 flex items-center gap-2">
                                <FlaskConical size={16} /> GENERATED RESEARCH ARTIFACT
                            </CardTitle>
                            <Badge variant="outline" className="text-[10px] text-neutral-500 border-neutral-700 font-mono">
                                <Cpu size={10} className="mr-1" /> HIVE-ORCHESTRATOR v1.2
                            </Badge>
                        </div>
                    </CardHeader>

                    <CardContent className="flex-1 p-0 overflow-hidden relative">
                        {loading && (
                            <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/80 z-10 backdrop-blur-md">
                                <div className="text-cyan-500 font-mono animate-pulse mb-2 text-xl tracking-tighter font-black underline decoration-cyan-500/50 underline-offset-8">CONDUCTING RESEARCH</div>
                                <div className="text-[10px] text-neutral-500 font-mono uppercase tracking-[0.3em]">Querying Canonical Archive...</div>
                            </div>
                        )}

                        {!paper && !loading && (
                            <div className="flex flex-col items-center justify-center h-full text-neutral-700 font-mono text-xs uppercase tracking-widest">
                                <div className="w-12 h-12 border-2 border-neutral-900 rounded-full mb-4 flex items-center justify-center">?</div>
                                Awaiting Hypothesis Objective
                            </div>
                        )}

                        {paper && (
                            <ScrollArea className="h-full p-8 lg:p-12">
                                <article className="prose prose-invert prose-sm max-w-none">
                                    <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight italic">{paper.hypothesis.title}</h1>
                                    <div className="text-xs text-neutral-500 font-mono mb-8 flex gap-4 uppercase tracking-widest border-b border-neutral-850 pb-4">
                                        <span>Topic: <span className="text-cyan-500">{paper.hypothesis.topic}</span></span>
                                        <span>Grounding: <span className="text-white">ENFORCED</span></span>
                                    </div>

                                    {/* GROUNDING SOURCES */}
                                    {paper.grounding && paper.grounding.length > 0 && (
                                        <div className="mb-8 p-4 bg-cyan-950/10 border border-cyan-900/30 rounded-2xl">
                                            <h4 className="text-[10px] font-bold text-cyan-500 uppercase tracking-widest mb-3">Grounding Sources (Archive)</h4>
                                            <div className="flex flex-wrap gap-2">
                                                {paper.grounding.map((s, i) => (
                                                    <Badge key={i} variant="outline" className="bg-black/50 text-[10px] border-neutral-700 text-neutral-400">
                                                        {s}
                                                    </Badge>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    <h3 className="text-cyan-400 font-mono text-xs uppercase tracking-widest mb-4 flex items-center gap-2">
                                        <div className="w-1 h-3 bg-cyan-500"></div> 1. Abstract & Hypothesis
                                    </h3>
                                    <p className="italic text-neutral-200 text-lg leading-relaxed mb-10 pl-6 border-l border-neutral-800">
                                        {paper.hypothesis.statement}
                                    </p>

                                    <h3 className="text-cyan-400 font-mono text-xs uppercase tracking-widest mb-4 flex items-center gap-2">
                                        <div className="w-1 h-3 bg-cyan-500"></div> 2. Implementation Logic
                                    </h3>
                                    <pre className="bg-black border border-neutral-800 rounded-2xl p-6 text-xs font-mono overflow-x-auto text-green-400 shadow-inner mb-10 selection:bg-green-500/20">
                                        {paper.design.code}
                                    </pre>

                                    <h3 className="text-cyan-400 font-mono text-xs uppercase tracking-widest mb-4 flex items-center gap-2">
                                        <div className="w-1 h-3 bg-cyan-500"></div> 3. Verification Metrics
                                    </h3>
                                    <div className="bg-neutral-950/50 p-6 rounded-2xl border border-neutral-800 mb-20 animate-in fade-in slide-in-from-bottom-5 duration-700">
                                        <div className="flex gap-2 items-center mb-4">
                                            {paper.result.success ? <CheckCircle2 className="text-emerald-500" size={18} /> : <XCircle className="text-red-500" size={18} />}
                                            <span className="font-bold text-neutral-200">Execution: {paper.result.success ? 'SUCCESS' : 'FAILURE'}</span>
                                        </div>
                                        <p className="text-neutral-400 mb-6 font-mono text-xs leading-relaxed bg-black/30 p-4 rounded-xl border border-white/5">
                                            {paper.result.output}
                                        </p>
                                        <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
                                            {Object.entries(paper.result.metrics).map(([k, v]) => (
                                                <div key={k} className="bg-neutral-900/50 p-3 rounded-xl border border-neutral-800/50 flex flex-col justify-center">
                                                    <span className="text-neutral-600 text-[9px] uppercase font-bold tracking-widest mb-1">{k}</span>
                                                    <span className="text-cyan-400 font-mono font-bold text-sm tracking-tight">{v as string}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </article>
                            </ScrollArea>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
    )
}
