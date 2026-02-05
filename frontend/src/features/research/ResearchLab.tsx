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
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8008'}/scientist/research`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ topic })
            })
            const data = await res.json()
            setPaper(data.paper)
            setReview(data.review)
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
                <Card className="bg-neutral-900 border-neutral-800">
                    <CardHeader>
                        <CardTitle className="text-sm font-mono text-neutral-400 flex items-center gap-2">
                            <Microscope size={16} /> HYPOTHESIS GENERATOR
                        </CardTitle>
                        <CardDescription>Initiate autonomous research loop.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <Input
                            placeholder="e.g. Log Obfuscation, PQC Migration..."
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            className="bg-black border-neutral-700 font-mono text-sm"
                        />
                        <Button
                            className="w-full bg-cyan-600 hover:bg-cyan-700 text-white font-bold"
                            onClick={conductResearch}
                            disabled={loading}
                        >
                            {loading ? "CONDUCTING RESEARCH..." : "START EXPERIMENT"}
                        </Button>
                    </CardContent>
                </Card>

                {/* PEER REVIEW SCORECARD */}
                {review && (
                    <Card className={`border-neutral-800 ${review.decision === 'ACCEPT' ? 'bg-green-950/20 border-green-900' : 'bg-red-950/20 border-red-900'}`}>
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
                                <span className="text-2xl font-bold font-mono text-neutral-200">{review.score}</span>
                            </div>
                            <div className="space-y-2">
                                <p className="text-xs text-neutral-500 uppercase">Reviewer Comments:</p>
                                {review.comments.map((c, i) => (
                                    <div key={i} className="text-xs text-neutral-300 bg-black/30 p-2 rounded border border-white/10">
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
                <Card className="bg-neutral-900 border-neutral-800 h-full flex flex-col overflow-hidden">
                    <CardHeader className="bg-neutral-950 border-b border-neutral-800 py-3">
                        <div className="flex justify-between items-center">
                            <CardTitle className="text-sm font-mono text-cyan-400 flex items-center gap-2">
                                <FlaskConical size={16} /> GENERATED RESEARCH ARTIFACT
                            </CardTitle>
                            {/* RAML METADATA BADGE */}
                            <Badge variant="outline" className="text-[10px] text-neutral-500 border-neutral-700 font-mono">
                                <Cpu size={10} className="mr-1" /> GENERATED BY: CORTEX-SCIENTIST-v2.0
                            </Badge>
                        </div>
                    </CardHeader>

                    <CardContent className="flex-1 p-0 overflow-hidden relative">
                        {loading && (
                            <div className="absolute inset-0 flex items-center justify-center bg-black/50 z-10 backdrop-blur-sm">
                                <div className="text-cyan-500 font-mono animate-pulse">GENERATING DOCTRINE...</div>
                            </div>
                        )}

                        {!paper && !loading && (
                            <div className="flex items-center justify-center h-full text-neutral-600 font-mono text-sm">
                                AWAITING HYPOTHESIS...
                            </div>
                        )}

                        {paper && (
                            <ScrollArea className="h-full p-6">
                                <article className="prose prose-invert prose-sm max-w-none">
                                    <h1 className="text-2xl font-bold text-neutral-100 mb-2">{paper.hypothesis.title}</h1>
                                    <div className="text-xs text-neutral-500 font-mono mb-6">TOPIC: {paper.hypothesis.topic}</div>

                                    <h3 className="text-cyan-400 border-b border-neutral-800 pb-2">1. Abstract & Hypothesis</h3>
                                    <p className="italic text-neutral-300 border-l-2 border-cyan-900 pl-4 py-2 bg-cyan-950/10 rounded-r">
                                        {paper.hypothesis.statement}
                                    </p>

                                    <h3 className="text-cyan-400 border-b border-neutral-800 pb-2 mt-6">2. Experimental Design (PoC)</h3>
                                    <pre className="bg-black border border-neutral-800 rounded p-4 text-xs font-mono overflow-x-auto text-green-400">
                                        {paper.design.code}
                                    </pre>

                                    <h3 className="text-cyan-400 border-b border-neutral-800 pb-2 mt-6">3. Results & Metrics</h3>
                                    <div className="bg-neutral-950 p-4 rounded border border-neutral-800">
                                        <div className="flex gap-2 items-center mb-2">
                                            {paper.result.success ? <CheckCircle2 className="text-green-500" size={16} /> : <XCircle className="text-red-500" size={16} />}
                                            <span className="font-bold text-neutral-200">Execution Status: {paper.result.success ? 'SUCCESS' : 'FAILURE'}</span>
                                        </div>
                                        <p className="text-neutral-400 mb-2">{paper.result.output}</p>
                                        <div className="grid grid-cols-2 gap-2 mt-2">
                                            {Object.entries(paper.result.metrics).map(([k, v]) => (
                                                <div key={k} className="bg-neutral-900 p-2 rounded flex justify-between">
                                                    <span className="text-neutral-500 text-xs uppercase">{k}</span>
                                                    <span className="text-cyan-400 font-mono font-bold">{v as string}</span>
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
