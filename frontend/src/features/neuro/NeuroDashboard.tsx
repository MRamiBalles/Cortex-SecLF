"use client"

import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/src/components/ui/card"
import { Button } from "@/src/components/ui/button"
import { Badge } from "@/src/components/ui/badge"
import { Switch } from "@/src/components/ui/switch"
import { Brain, Shield, ShieldAlert, Activity, Lock, Unlock, FileKey } from 'lucide-react'

// Mock types based on API
interface NeuroPacket {
    timestamp: number
    raw_eeg: { [key: string]: number }
    psychography: { inferred_state: string, privacy_risk: string }
    status: string
}

export default function NeuroDashboard() {
    const [consent, setConsent] = useState(false)
    const [streamData, setStreamData] = useState<number[]>([]) // Single channel for demo visual
    const [packet, setPacket] = useState<NeuroPacket | null>(null)
    const [ledger, setLedger] = useState<any[]>([])
    const [blockedCount, setBlockedCount] = useState(0)
    const [isPolling, setIsPolling] = useState(true)
    const [sovereignMode, setSovereignMode] = useState(true) // Default to v3.0
    const [zkpStatus, setZkpStatus] = useState<string | null>(null)

    // SVG Polyline config
    const maxPoints = 100
    const height = 100

    // Fetch Stream (Simulate Agent Polling)
    useEffect(() => {
        if (!isPolling) return

        const interval = setInterval(async () => {
            try {
                let res;
                if (sovereignMode) {
                    // v3.0: GENERATE ZKP PROOF (Mock)
                    const proof = {
                        id: `π_${Math.random().toString(36).substr(2, 9)}`,
                        metadata: "CORTEX_ZKP_v3",
                        timestamp: Date.now() / 1000
                    }
                    const public_signals = [75] // Threshold constant

                    res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8008'}/neuro/stream`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            client_id: "agent-nexus-prover",
                            proof,
                            public_signals
                        })
                    })
                } else {
                    // v2.0: LEGACY GET (Exposes Identity to check Consent)
                    res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8008'}/neuro/stream?client_id=agent-legacy`)
                }

                const data = await res.json()

                if (data.mode === "SOVEREIGN_ZKP") {
                    setZkpStatus(data.zkp_status)
                    // Synthesize a packet for the visualizer from redacted data
                    setPacket({
                        timestamp: Date.now(),
                        raw_eeg: { "AF7": 0 }, // Redacted
                        psychography: { inferred_state: data.inference, privacy_risk: "ZERO_KNOWLEDGE_VERIFIED" },
                        status: "SOVEREIGN_ZKP"
                    })
                } else {
                    setZkpStatus(null)
                    setPacket(data.data)
                }

                const p = data.mode === "SOVEREIGN_ZKP" ? { status: "SOVEREIGN_ZKP", raw_eeg: { "AF7": 50 } } : data.data as NeuroPacket

                // Update Visualizer Data (Simulate rolling window)
                // If encrypted, show noise
                let newValue = 50
                if (p.status === "EXPOSED") {
                    // Normalize 10-100 uV to 0-100 height
                    newValue = p.raw_eeg["AF7"] || 50
                } else {
                    // Noise for encrypted state
                    newValue = Math.random() * 100
                }

                setStreamData(prev => {
                    const next = [...prev, newValue]
                    if (next.length > maxPoints) next.shift()
                    return next
                })

                // Track Blocked Attempts
                if (data.audit_log && data.audit_log.decision === "DENIED") {
                    setBlockedCount(prev => prev + 1)
                }

            } catch (e) {
                console.error(e)
            }
        }, 200) // 5Hz Refresh for smoothness

        return () => clearInterval(interval)
    }, [isPolling])

    // Load Ledger
    const fetchLedger = async () => {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8008'}/neuro/ledger`)
        const data = await res.json()
        setLedger(data.reverse()) // Show newest first
    }

    // Initial Load
    useEffect(() => {
        fetchLedger()
    }, [])

    const toggleConsent = async () => {
        const action = consent ? "REVOKE" : "GRANT"
        await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8008'}/neuro/consent`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action })
        })
        setConsent(!consent)
        fetchLedger()
    }

    // SVG Path Generator
    const getPolylinePoints = () => {
        return streamData.map((val, i) => {
            const x = (i / maxPoints) * 100
            // Invert Y because SVG 0 is top
            const y = height - val
            return `${x},${y}`
        }).join(" ")
    }

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6 max-w-7xl mx-auto h-[calc(100vh-100px)]">

            {/* 1. VISUALIZER & CONTROLS (Main Col) */}
            <div className="lg:col-span-2 flex flex-col gap-6">

                {/* NEURO-MONITOR CARD */}
                <Card className="bg-neutral-900 border-neutral-800 flex flex-col overflow-hidden relative min-h-[400px]">
                    <CardHeader className="z-10 bg-neutral-900/80 backdrop-blur border-b border-neutral-800 flex flex-row justify-between items-center">
                        <CardTitle className="flex items-center gap-2 text-cyan-400">
                            <Brain size={24} /> BIOMETRIC PSYCHOGRAPHY MONITOR
                        </CardTitle>
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2 bg-neutral-800 p-1 rounded px-2">
                                <span className="text-[10px] font-mono text-neutral-500 uppercase">Sovereign Mode (ZKP):</span>
                                <Switch
                                    checked={sovereignMode}
                                    onCheckedChange={setSovereignMode}
                                />
                            </div>
                            <span className={`text-xs font-mono font-bold ${consent && !sovereignMode ? 'text-red-500 animate-pulse' : 'text-green-500'}`}>
                                {sovereignMode ? "✨ MATHEMATICAL SOVEREIGNTY" : (consent ? "⚠ DATA EXPOSED" : "🔒 PRIVACY SHIELD ACTIVE")}
                            </span>
                            <div className="flex items-center gap-2">
                                <span className="text-sm text-neutral-400">CONSENT:</span>
                                <Button
                                    variant={consent ? "destructive" : "default"}
                                    disabled={sovereignMode} // v3.0 doesn't need manual consent toggle for raw data as it's never sent
                                    className={`w-32 font-bold transition-all duration-300 ${!consent ? 'bg-emerald-600 hover:bg-emerald-700' : ''} ${sovereignMode ? 'opacity-50 grayscale' : ''}`}
                                    onClick={toggleConsent}
                                >
                                    {consent ? <Unlock size={16} className="mr-2" /> : <Lock size={16} className="mr-2" />}
                                    {consent ? "REVOKE" : "GRANT"}
                                </Button>
                            </div>
                        </div>
                    </CardHeader>

                    {/* SVG GRAPH AREA */}
                    <div className="flex-1 relative bg-black p-4 flex items-center justify-center overflow-hidden">

                        {/* INFERENCE OVERLAY */}
                        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-20 text-center pointer-events-none">
                            <h3 className="text-xs text-neutral-500 tracking-[0.2em] mb-2 uppercase">Inferred Mental State</h3>
                            {packet?.status === "EXPOSED" ? (
                                <div className="text-4xl md:text-6xl font-black text-cyan-500 tracking-tighter drop-shadow-[0_0_15px_rgba(6,182,212,0.5)]">
                                    {packet.psychography.inferred_state}
                                </div>
                            ) : packet?.status === "SOVEREIGN_ZKP" ? (
                                <div className="space-y-2">
                                    <div className="text-4xl md:text-5xl font-black text-emerald-500 tracking-tighter">
                                        VERIFIED BY PROOF
                                    </div>
                                    <div className="text-xs font-mono text-emerald-400 bg-emerald-950/40 p-1 px-3 rounded-full inline-block border border-emerald-800">
                                        π_PROOF: {zkpStatus}
                                    </div>
                                </div>
                            ) : (
                                <div className="text-4xl md:text-6xl font-bold text-neutral-700 font-mono tracking-widest blur-[2px]">
                                    ENCRYPTED
                                </div>
                            )}

                            {/* RAW VALUE HASH */}
                            <div className="mt-4 font-mono text-xs bg-black/50 p-2 rounded border border-neutral-800 inline-block text-neutral-400">
                                {packet?.status === "EXPOSED" ?
                                    `RISK LEVEL: ${packet.psychography.privacy_risk}` :
                                    (packet?.status === "SOVEREIGN_ZKP" ?
                                        `ZERO KNOWLEDGE: ${packet.psychography.privacy_risk}` :
                                        `HASH: ${packet?.psychography.inferred_state.substring(0, 24)}...`)
                                }
                            </div>
                        </div>

                        {/* BACKGROUND GRID */}
                        <div className="absolute inset-0 grid grid-cols-12 grid-rows-6 pointer-events-none opacity-10">
                            {Array.from({ length: 72 }).map((_, i) => (
                                <div key={i} className="border border-cyan-900/30 w-full h-full"></div>
                            ))}
                        </div>

                        {/* SVG LINE */}
                        <svg viewBox={`0 0 100 ${height}`} className="w-full h-full absolute inset-0 z-10 pointer-events-none" preserveAspectRatio="none">
                            <polyline
                                fill="none"
                                stroke={consent ? "#06b6d4" : "#404040"}
                                strokeWidth="0.5"
                                strokeOpacity={consent ? "0.8" : "0.3"}
                                points={getPolylinePoints()}
                                vectorEffect="non-scaling-stroke"
                            />
                        </svg>

                        {/* NOISE OVERLAY FOR ENCRYPTION */}
                        {!consent && (
                            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 contrast-150 brightness-50 z-15 pointer-events-none"></div>
                        )}
                    </div>

                    <CardContent className="py-2 bg-neutral-950 border-t border-neutral-800 flex justify-between text-xs font-mono text-neutral-500">
                        <span>SENSOR: AF7 (Frontal Lobe)</span>
                        <span>LATENCY: 12ms</span>
                        <span>DEVICE: CORTEX-BCI-001</span>
                    </CardContent>
                </Card>

                {/* STATS ROW */}
                <div className="grid grid-cols-2 gap-4">
                    <Card className="bg-neutral-900 border-neutral-800">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-sm text-neutral-400 flex items-center gap-2">
                                <ShieldAlert size={16} /> BLOCKED ACCESS ATTEMPTS
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-4xl font-bold text-red-500 font-mono">
                                {blockedCount.toString().padStart(4, '0')}
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-neutral-900 border-neutral-800">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-sm text-neutral-400 flex items-center gap-2">
                                <FileKey size={16} /> CURRENT BLOCK HEIGHT
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-4xl font-bold text-amber-500 font-mono">
                                #{ledger.length}
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>

            {/* 2. LEDGER LOG (Right Col) */}
            <div className="lg:col-span-1 h-full">
                <Card className="bg-neutral-900 border-neutral-800 h-full flex flex-col">
                    <CardHeader className="border-b border-neutral-800">
                        <CardTitle className="flex items-center gap-2 text-amber-500 text-base">
                            <Activity size={18} /> CONSENT CHAIN® LEDGER
                        </CardTitle>
                        <CardDescription className="text-xs">Immutable Audit Log (Local HashChain)</CardDescription>
                    </CardHeader>
                    <CardContent className="flex-1 overflow-y-auto p-0 scrollbar-thin scrollbar-thumb-neutral-700">
                        <div className="flex flex-col">
                            {ledger.map((block) => (
                                <div key={block.index} className="p-4 border-b border-neutral-800 hover:bg-neutral-800/50 transition-colors">
                                    <div className="flex justify-between items-center mb-2">
                                        <Badge variant={block.action === "GRANT" ? "default" : "secondary"} className={`text-[10px] ${block.action === "REVOKE" ? 'bg-neutral-700 text-neutral-300' : 'bg-red-900 text-red-200 hover:bg-red-800'}`}>
                                            {block.action === "GRANT" ? "CONSENT_OFF (EXPOSED)" : "CONSENT_REVOKED"}
                                        </Badge>
                                        <span className="text-[10px] text-neutral-500 font-mono">#{block.index}</span>
                                    </div>
                                    <div className="font-mono text-[10px] text-neutral-400 break-all space-y-1">
                                        <p><span className="text-neutral-600">HASH:</span> {block.hash.substring(0, 16)}...</p>
                                        <p><span className="text-neutral-600">PREV:</span> {block.previous_hash.substring(0, 16)}...</p>
                                        <p><span className="text-neutral-600">TIME:</span> {new Date(block.timestamp * 1000).toLocaleTimeString()}</p>
                                    </div>
                                </div>
                            ))}
                            {ledger.length === 0 && <div className="p-4 text-center text-sm text-neutral-500 italic">Initializing Genesis Block...</div>}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
