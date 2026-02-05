"use client"

import React, { useState, useRef, useEffect } from "react"
import { Send, Download, AlertTriangle, Shield, Terminal, BookOpen, ChevronDown, ChevronUp } from "lucide-react"
import { Button } from "@/src/components/ui/button"
import { Input } from "@/src/components/ui/input"
import { Card, CardContent, CardTitle, CardHeader } from "@/src/components/ui/card"
import { ScrollArea } from "@/src/components/ui/scroll-area"
import { Badge } from "@/src/components/ui/badge"
import { Alert, AlertDescription, AlertTitle } from "@/src/components/ui/alert"

interface SearchResult {
    content: str
    source: str
    distance: number
    year?: number
    authority?: string
    language?: string
}

interface Message {
    id: string
    role: "user" | "assistant"
    content: string
    citations?: SearchResult[]
    hallucination_risk?: boolean
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [minYear, setMinYear] = useState<number | "">("")

    const messagesEndRef = useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSend = async () => {
        if (!input.trim()) return

        const userMsg: Message = { id: Date.now().toString(), role: "user", content: input }
        setMessages(prev => [...prev, userMsg])
        setInput("")
        setIsLoading(true)

        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8008'}/archive/search`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    query: userMsg.content,
                    collection: "trench",
                    n_results: 3,
                    min_year: minYear ? Number(minYear) : undefined
                })
            })

            const data = await res.json()

            const aiMsg: Message = {
                id: (Date.now() + 1).toString(),
                role: "assistant",
                content: data.context ? "Based on the Canonical Archive:" : "No relevant data found.",
                citations: data.results,
                hallucination_risk: data.hallucination_risk
            }
            setMessages(prev => [...prev, aiMsg])

        } catch (error) {
            console.error(error)
            setMessages(prev => [...prev, { id: Date.now().toString(), role: "assistant", content: "Error connecting to Archive." }])
        } finally {
            setIsLoading(false)
        }
    }

    const downloadReport = (msg: Message) => {
        if (!msg.citations) return

        const timestamp = new Date().toISOString()
        let report = `# Cortex-Sec Archive Report\n**Date:** ${timestamp}\n**Query context:** User Interaction\n\n`
        report += `## Summary\n${msg.content}\n\n`
        report += `## Evidence & Ground Truth\n`

        msg.citations.forEach((cit, i) => {
            report += `### Source ${i + 1}: ${cit.source}\n`
            report += `- **Authority:** ${cit.authority || 'N/A'}\n`
            report += `- **Year:** ${cit.year || 'N/A'}\n`
            report += `- **Language:** ${cit.language || 'Text'}\n`
            report += `> ${cit.content.replace(/\n/g, '\n> ')}\n\n`
        })

        const blob = new Blob([report], { type: 'text/markdown' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `cortex_report_${Date.now()}.md`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
    }

    return (
        <div className="flex flex-col h-[calc(100vh-100px)] w-full max-w-5xl mx-auto p-4 gap-4">
            <Card className="flex-1 overflow-hidden flex flex-col border-neutral-800 bg-neutral-900/50 backdrop-blur">
                <CardHeader className="border-b border-neutral-800 pb-4">
                    <CardTitle className="flex items-center gap-2 text-primary">
                        <BookOpen size={20} /> Canal: TRINCHERA (Technical)
                    </CardTitle>
                    <div className="flex gap-2 items-center text-sm text-neutral-400">
                        Filter: Min Year
                        <Input
                            type="number"
                            placeholder="2022"
                            className="w-24 h-8 bg-neutral-950 border-neutral-800"
                            value={minYear}
                            onChange={(e) => setMinYear(Number(e.target.value))}
                        />
                    </div>
                </CardHeader>

                <CardContent className="flex-1 overflow-hidden p-0 relative">
                    <ScrollArea className="h-full p-4">
                        <div className="flex flex-col gap-6">
                            {messages.map((msg) => (
                                <div key={msg.id} className={`flex flex-col gap-2 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>

                                    <div className={`p-4 rounded-lg max-w-[85%] ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-neutral-800 text-neutral-200 border border-neutral-700'}`}>
                                        <p className="whitespace-pre-wrap">{msg.content}</p>

                                        {msg.hallucination_risk && (
                                            <Alert variant="destructive" className="mt-4 bg-red-950/50 border-red-900">
                                                <AlertTriangle size={16} />
                                                <AlertTitle>Hallucination Risk</AlertTitle>
                                                <AlertDescription>No strict ground truth found (Distance {'>'} 0.4). Verify manually.</AlertDescription>
                                            </Alert>
                                        )}

                                        {msg.citations && msg.citations.length > 0 && (
                                            <div className="mt-6 flex flex-col gap-4">
                                                <div className="flex justify-between items-center border-b border-neutral-700 pb-2">
                                                    <span className="text-xs font-mono text-neutral-400">EVIDENCE CHAIN</span>
                                                    <Button variant="ghost" size="sm" onClick={() => downloadReport(msg)} className="h-6 text-xs gap-1">
                                                        <Download size={12} /> Export Report
                                                    </Button>
                                                </div>

                                                {msg.citations.map((cit, idx) => (
                                                    <div key={idx} className="bg-neutral-950/50 rounded p-3 border border-neutral-800 text-sm">
                                                        <div className="flex flex-wrap gap-2 items-center mb-2">
                                                            <span className="font-bold text-blue-400">#{idx + 1} {cit.source}</span>

                                                            {/* AUTHORITY BADGE */}
                                                            {cit.authority?.includes("High") ?
                                                                <Badge variant="high" className="gap-1"><Shield size={10} /> High Auth</Badge> :
                                                                <Badge variant="medium" className="gap-1"><Terminal size={10} /> Trench</Badge>
                                                            }

                                                            {/* OBSOLESCENCE ALERT */}
                                                            {(cit.year !== undefined && cit.year < 2023) ?
                                                                <Badge variant="destructive" className="gap-1"><AlertTriangle size={10} /> Old ({cit.year})</Badge> :
                                                                <Badge variant="secondary">{cit.year}</Badge>
                                                            }

                                                            {cit.language && <Badge variant="outline" className="font-mono text-[10px]">{cit.language}</Badge>}
                                                        </div>

                                                        {/* GROUND TRUTH CHECK (Expandable) */}
                                                        <details className="group">
                                                            <summary className="cursor-pointer text-xs text-neutral-500 hover:text-neutral-300 flex items-center gap-1 select-none">
                                                                <ChevronDown size={12} className="group-open:hidden" />
                                                                <ChevronUp size={12} className="hidden group-open:block" />
                                                                Verify Ground Truth (Context)
                                                            </summary>
                                                            <div className="mt-2 p-2 bg-black rounded font-mono text-xs overflow-x-auto border border-neutral-800 text-green-500/80">
                                                                {cit.content}
                                                            </div>
                                                        </details>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>

                                </div>
                            ))}
                            <div ref={messagesEndRef} />
                        </div>
                    </ScrollArea>
                </CardContent>

                <div className="p-4 border-t border-neutral-800 bg-neutral-900">
                    <div className="flex gap-2">
                        <Input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Query the Archive (e.g., 'How to detect XXE in 2024?')..."
                            className="bg-neutral-950 border-neutral-800 active:border-primary"
                            disabled={isLoading}
                        />
                        <Button onClick={handleSend} disabled={isLoading} className="w-12 px-0">
                            <Send size={18} />
                        </Button>
                    </div>
                </div>
            </Card>
        </div>
    )
}
