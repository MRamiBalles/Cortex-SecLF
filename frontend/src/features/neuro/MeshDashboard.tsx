"use client"

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/src/components/ui/card"
import { Badge } from "@/src/components/ui/badge"
import { Shield, Share2, CPU, Fingerprint, Activity } from 'lucide-react'

interface MeshNode {
    id: string
    fingerprint: string
    status: string
    last_seen: number
    algo: string
}

export default function MeshDashboard() {
    const [nodes, setNodes] = useState<MeshNode[]>([])
    const [loading, setLoading] = useState(true)

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    const fetchNodes = async () => {
        try {
            const res = await fetch(`${API_URL}/neuro/nodes`)
            const data = await res.json()
            setNodes(data.nodes || [])
        } catch (e) {
            console.error("MESH_TELEMETRY_FAILURE:", e)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchNodes()
        const interval = setInterval(fetchNodes, 5000)
        return () => clearInterval(interval)
    }, [API_URL])

    if (loading) return (
        <div className="text-cyan-500 animate-pulse font-mono text-[10px] py-10 uppercase tracking-widest text-center h-full flex items-center justify-center">
            Synchronising Mesh Identity Fingerprints...
        </div>
    )

    return (
        <Card className="bg-neutral-950 border-neutral-800 shadow-2xl overflow-hidden">
            <CardHeader className="p-4 bg-gradient-to-r from-cyan-950/20 to-transparent border-b border-neutral-800 flex flex-row items-center justify-between">
                <div>
                    <CardTitle className="text-cyan-400 flex items-center gap-2 font-black italic tracking-tighter text-sm">
                        <Share2 size={16} className="animate-spin-slow" /> HIVE-NET SOVEREIGN MESH
                    </CardTitle>
                    <CardDescription className="text-[10px] uppercase tracking-widest text-neutral-600">P2P Decentralised Consensus Infrastructure</CardDescription>
                </div>
                <div className="flex gap-2 items-center">
                    <Badge variant="outline" className="border-cyan-900 text-cyan-500 text-[8px] font-mono uppercase bg-cyan-950/10 h-5 px-2">
                        {nodes.length} PERS ACTIVE
                    </Badge>
                </div>
            </CardHeader>
            <CardContent className="p-4 bg-black/40">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {nodes.map((node) => (
                        <div key={node.id} className="p-4 rounded-xl border border-neutral-900 bg-neutral-950/50 hover:bg-neutral-900/50 transition-all group">
                            <div className="flex justify-between items-start mb-3">
                                <div className="p-1.5 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 group-hover:bg-cyan-500/20 transition-colors">
                                    <CPU size={14} />
                                </div>
                                <Badge className="bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 text-[8px] h-4">
                                    {node.status}
                                </Badge>
                            </div>

                            <h4 className="text-[10px] font-black text-neutral-400 mb-1 tracking-wider uppercase">{node.id}</h4>

                            <div className="space-y-3">
                                <div className="relative group/fp">
                                    <div className="flex items-center gap-1.5 mb-1">
                                        <Fingerprint size={10} className="text-neutral-600" />
                                        <span className="text-[8px] font-mono text-neutral-700 uppercase tracking-widest">Public Key Signature</span>
                                    </div>
                                    <div className="bg-black p-2 rounded-lg border border-neutral-800 break-all h-10 overflow-hidden group-hover/fp:overflow-visible group-hover/fp:h-auto group-hover/fp:absolute group-hover/fp:z-50 group-hover/fp:w-full group-hover/fp:shadow-2xl transition-all">
                                        <code className="text-[8px] font-mono text-cyan-600 leading-tight">
                                            {node.fingerprint}
                                        </code>
                                    </div>
                                </div>

                                <div className="flex justify-between items-center pt-2 border-t border-neutral-900">
                                    <div className="text-[7px] font-mono text-neutral-700 uppercase">Algo: <span className="text-neutral-500">{node.algo}</span></div>
                                    <div className="flex items-center gap-1 text-[7px] font-mono text-emerald-500/60">
                                        <Activity size={8} /> HEARTBEAT_LOCK
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="mt-4 p-3 rounded-xl border border-neutral-900 bg-red-950/5 flex items-center justify-between text-[8px] font-mono text-neutral-600 uppercase tracking-[0.2em]">
                    <span className="flex items-center gap-2">
                        <Shield size={10} className="text-red-500" /> Mesh Integrity: Cryptographically Hardened
                    </span>
                    <span className="text-neutral-700">Consensus Mode: ByzFT (Sim)</span>
                </div>
            </CardContent>
        </Card>
    )
}
