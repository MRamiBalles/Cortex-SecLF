"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/src/components/ui/card"
import { Badge } from "@/src/components/ui/badge"
import { Globe, ShieldCheck, Zap, Server, Network } from 'lucide-react'

interface PeerLattice {
    id: string
    status: string
    latency: string
    location: string
}

export default function FederationMap() {
    const [peers, setPeers] = useState<PeerLattice[]>([
        { id: 'LATTICE-OSLO-01', status: 'SYNCHRONIZED', latency: '42ms', location: 'EU-NORTH' },
        { id: 'LATTICE-TOKYO-09', status: 'SYNCHRONIZED', latency: '180ms', location: 'AP-NORTHEAST' },
        { id: 'LATTICE-VIRGINIA-04', status: 'VALIDATING', latency: '95ms', location: 'US-EAST' }
    ])

    const [globalQuorum, setGlobalQuorum] = useState({ active: true, consensus: '84%', votes: '4/5' })

    return (
        <Card className="bg-black border-neutral-900 overflow-hidden shadow-2xl">
            <CardHeader className="border-b border-neutral-900 bg-neutral-900/20">
                <CardTitle className="text-xs uppercase tracking-widest text-neutral-400 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Globe size={14} className="text-cyan-500" />
                        Federation Command Hub
                    </div>
                    <Badge variant="outline" className="text-[10px] border-emerald-900 text-emerald-500 animate-pulse">
                        META_QUORUM_ESTABLISHED
                    </Badge>
                </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
                <div className="grid grid-cols-1 lg:grid-cols-4 min-h-[300px]">
                    {/* INFRASTRUCTURE MONITOR */}
                    <div className="lg:col-span-1 border-r border-neutral-900 p-4 space-y-6 bg-neutral-900/10">
                        <div className="space-y-4">
                            <h3 className="text-[10px] text-neutral-500 uppercase font-bold">Global Consensus</h3>
                            <div className="bg-neutral-900/50 p-3 rounded border border-neutral-800">
                                <div className="flex justify-between items-center mb-1">
                                    <span className="text-[10px] text-neutral-400">Total Votes</span>
                                    <span className="text-xs font-mono text-cyan-500">{globalQuorum.votes}</span>
                                </div>
                                <div className="w-full bg-neutral-800 h-1.5 rounded-full overflow-hidden">
                                    <div className="bg-cyan-500 h-full w-[80%]" />
                                </div>
                            </div>
                        </div>

                        <div className="space-y-4">
                            <h3 className="text-[10px] text-neutral-500 uppercase font-bold">Lattice Bridges</h3>
                            <div className="space-y-2">
                                <div className="flex items-center gap-2 text-[10px] text-emerald-500">
                                    <ShieldCheck size={12} /> P2P_HANDSHAKE_OK
                                </div>
                                <div className="flex items-center gap-2 text-[10px] text-cyan-500">
                                    <Zap size={12} /> DHT_DISCOVERY_ACTIVE
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* INTERACTIVE MAP / MESH VIEW */}
                    <div className="lg:col-span-3 p-6 relative bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-cyan-950/20 via-black to-black">
                        <div className="absolute inset-0 opacity-10 pointer-events-none"
                            style={{ backgroundImage: 'radial-gradient(#333 1px, transparent 1px)', backgroundSize: '20px 20px' }} />

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 relative z-10">
                            {peers.map(peer => (
                                <div key={peer.id} className="p-4 rounded-lg bg-neutral-900/40 border border-neutral-800 hover:border-cyan-900 transition-colors group">
                                    <div className="flex justify-between items-start mb-3">
                                        <div className="flex items-center gap-2">
                                            <div className="p-1.5 rounded bg-cyan-950/30 text-cyan-500">
                                                <Server size={14} />
                                            </div>
                                            <div>
                                                <div className="text-xs font-mono text-neutral-200">{peer.id}</div>
                                                <div className="text-[8px] text-neutral-500">{peer.location}</div>
                                            </div>
                                        </div>
                                        <Badge variant="outline" className={`text-[8px] ${peer.status === 'SYNCHRONIZED' ? 'border-emerald-900 text-emerald-500' : 'border-orange-900 text-orange-500 animate-pulse'}`}>
                                            {peer.status}
                                        </Badge>
                                    </div>
                                    <div className="flex items-center justify-between text-[9px] font-mono">
                                        <span className="text-neutral-600">LATENCY</span>
                                        <span className="text-cyan-500">{peer.latency}</span>
                                    </div>
                                </div>
                            ))}

                            {/* THE LOCAL LATTICE */}
                            <div className="p-4 rounded-lg bg-cyan-950/10 border border-cyan-500/30 ring-1 ring-cyan-500/20 relative overflow-hidden">
                                <div className="absolute -right-4 -bottom-4 text-cyan-500/10 rotate-12">
                                    <Network size={80} />
                                </div>
                                <div className="flex justify-between items-start mb-3">
                                    <div className="flex items-center gap-2">
                                        <div className="p-1.5 rounded bg-cyan-500 text-black">
                                            <Server size={14} />
                                        </div>
                                        <div>
                                            <div className="text-xs font-mono text-cyan-400 font-bold">LOCAL_LATTICE_01</div>
                                            <div className="text-[8px] text-cyan-600">MASTER_COORDINATOR</div>
                                        </div>
                                    </div>
                                    <Badge className="text-[8px] bg-cyan-500 text-black border-none ring-1 ring-cyan-400">
                                        SOVEREIGN_ROOT
                                    </Badge>
                                </div>
                                <div className="grid grid-cols-2 gap-2 text-[8px] font-mono">
                                    <div className="text-cyan-700 uppercase">Mesh Status: STABLE</div>
                                    <div className="text-cyan-700 uppercase">Uptime: 99.99%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
