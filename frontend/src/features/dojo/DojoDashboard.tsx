"use client"

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/src/components/ui/card"
import { Button } from "@/src/components/ui/button"
import { Badge } from "@/src/components/ui/badge"
import { Activity, Play, Square, ExternalLink, RefreshCw, Server, ShieldCheck } from 'lucide-react'

interface Lab {
    id: string
    name: string
    image: string
    description: string
    status?: string
    access_url?: string
}

export default function DojoDashboard() {
    const [labs, setLabs] = useState<Lab[]>([])
    const [loading, setLoading] = useState<Record<string, boolean>>({})
    const [globalLoading, setGlobalLoading] = useState(true)

    const fetchLabs = async () => {
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/dojo/labs`)
            const data = await res.json()
            setLabs(data)
        } catch (e) {
            console.error(e)
        } finally {
            setGlobalLoading(false)
        }
    }

    useEffect(() => {
        fetchLabs()
    }, [])

    const startLab = async (id: string) => {
        setLoading(prev => ({ ...prev, [id]: true }))
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/dojo/start/${id}`, { method: 'POST' })
            const data = await res.json()
            // Update local state
            setLabs(prev => prev.map(l => l.id === id ? { ...l, status: 'running', access_url: data.access_url } : l))
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(prev => ({ ...prev, [id]: false }))
        }
    }

    const stopLab = async (id: string) => {
        setLoading(prev => ({ ...prev, [id]: true }))
        try {
            await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/dojo/stop/${id}`, { method: 'POST' })
            setLabs(prev => prev.map(l => l.id === id ? { ...l, status: 'down', access_url: undefined } : l))
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(prev => ({ ...prev, [id]: false }))
        }
    }

    return (
        <div className="flex flex-col gap-8 p-8 max-w-7xl mx-auto min-h-screen bg-[#0a0a0a] text-white">
            <header className="flex flex-col gap-2">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-emerald-500/10 rounded-lg">
                        <Activity className="text-emerald-500" size={24} />
                    </div>
                    <h1 className="text-4xl font-bold tracking-tight">TRAINING <span className="text-emerald-500">DOJO</span></h1>
                </div>
                <p className="text-neutral-500 font-mono text-sm uppercase tracking-widest">Vulnerable Environment Orchestrator & Defense Sandbox</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {globalLoading ? (
                    [1, 2, 3].map(i => <div key={i} className="h-64 bg-neutral-900/50 rounded-2xl animate-pulse"></div>)
                ) : (
                    labs.map(lab => (
                        <Card key={lab.id} className="bg-neutral-900 border-neutral-800 overflow-hidden transition-all hover:border-emerald-500/30 group">
                            <CardHeader className="bg-neutral-950/50 pb-4">
                                <div className="flex justify-between items-start mb-2">
                                    <Badge variant="outline" className="text-[10px] font-mono border-neutral-700 text-neutral-500">
                                        CONTAINER: {lab.id}
                                    </Badge>
                                    <StatusBadge status={lab.status} />
                                </div>
                                <CardTitle className="text-xl group-hover:text-emerald-400 transition-colors uppercase font-black italic">{lab.name}</CardTitle>
                                <CardDescription className="text-neutral-500 text-xs font-mono">{lab.image}</CardDescription>
                            </CardHeader>
                            <CardContent className="pt-6 flex flex-col gap-6">
                                <p className="text-sm text-neutral-400 h-10 overflow-hidden line-clamp-2">
                                    {lab.description}
                                </p>

                                <div className="space-y-3">
                                    {lab.status === 'running' ? (
                                        <>
                                            <Button
                                                className="w-full bg-emerald-600 hover:bg-emerald-700 text-white gap-2 font-bold"
                                                onClick={() => window.open(lab.access_url, '_blank')}
                                            >
                                                <ExternalLink size={16} /> ACCESS LAB INTERFACE
                                            </Button>
                                            <Button
                                                variant="outline"
                                                className="w-full border-red-900/50 text-red-500 hover:bg-red-950/30 gap-2"
                                                onClick={() => stopLab(lab.id)}
                                                disabled={loading[lab.id]}
                                            >
                                                <Square size={16} fill="currentColor" /> TERMINATE SESSION
                                            </Button>
                                        </>
                                    ) : (
                                        <Button
                                            className="w-full bg-neutral-800 hover:bg-emerald-600 text-white gap-2 transition-all font-bold"
                                            onClick={() => startLab(lab.id)}
                                            disabled={loading[lab.id]}
                                        >
                                            {loading[lab.id] ? <RefreshCw className="animate-spin" size={16} /> : <Play size={16} fill="currentColor" />}
                                            INITIALIZE ENVIRONMENT
                                        </Button>
                                    )}
                                </div>
                            </CardContent>
                            <div className="px-6 pb-4 flex justify-between items-center text-[10px] font-mono text-neutral-600">
                                <div className="flex items-center gap-1">
                                    <Server size={10} />
                                    <span>LOCAL_DOCKER_ENGINE</span>
                                </div>
                                <div className="flex items-center gap-1">
                                    <ShieldCheck size={10} className="text-emerald-900" />
                                    <span>WAZUH_MONITORED</span>
                                </div>
                            </div>
                        </Card>
                    ))
                )}
            </div>

            <footer className="mt-auto pt-12 text-center">
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-neutral-900/50 rounded-full border border-neutral-800 text-[10px] font-mono text-neutral-500 uppercase tracking-widest">
                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span>
                    Operational Guard Enforced: All labs are isolated in the 'cslf-net' bridge.
                </div>
            </footer>
        </div>
    )
}

function StatusBadge({ status }: { status?: string }) {
    if (status === 'running') {
        return (
            <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 text-[10px] font-bold font-mono">
                <span className="w-1 h-1 bg-emerald-500 rounded-full animate-ping"></span>
                ONLINE
            </div>
        )
    }
    return (
        <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-neutral-800 border border-neutral-700 text-neutral-500 text-[10px] font-bold font-mono">
            DORMANT
        </div>
    )
}
