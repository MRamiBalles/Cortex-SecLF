"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/src/components/ui/card"
import { Badge } from "@/src/components/ui/badge"
import { Activity, Users, ShieldAlert, Cpu, Share2 } from 'lucide-react'

interface MartyrInsight {
    team_id: string
    type: string
    data: any
    timestamp: number
}

export default function MartDashboard() {
    const [insights, setInsights] = useState<MartyrInsight[]>([])
    const [activeTeams, setActiveTeams] = useState<string[]>(['HIVE-ALPHA', 'HIVE-BETA', 'HIVE-SIGMA'])

    // Simulated WebSocket/Event listener for MART pulses
    useEffect(() => {
        const interval = setInterval(() => {
            const mockTeam = activeTeams[Math.floor(Math.random() * activeTeams.length)]
            const mockInsight: MartyrInsight = {
                team_id: mockTeam,
                type: 'RESEARCH_PULSE',
                data: { status: 'DISCOVERY', detail: 'Identified potential bypass in XSS filter' },
                timestamp: Date.now()
            }
            setInsights(prev => [mockInsight, ...prev].slice(0, 10))
        }, 3000)
        return () => clearInterval(interval)
    }, [])

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
            {/* ACTIVE TEAMS PANEL */}
            <Card className="md:col-span-1 bg-black border-neutral-900">
                <CardHeader>
                    <CardTitle className="text-[10px] uppercase tracking-widest text-neutral-500 flex items-center gap-2">
                        <Users size={12} className="text-cyan-500" /> Coordinated Teams
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    {activeTeams.map(team => (
                        <div key={team} className="flex items-center justify-between p-3 rounded-lg border border-neutral-800 bg-neutral-900/50">
                            <div className="flex flex-col">
                                <span className="text-xs font-mono text-neutral-200">{team}</span>
                                <span className="text-[8px] text-emerald-500 font-mono">STATUS: OPTIMIZING</span>
                            </div>
                            <Activity size={16} className="text-emerald-500 animate-pulse" />
                        </div>
                    ))}
                </CardContent>
            </Card>

            {/* COLLABORATIVE EXPLOIT GRAPH (MOCK VISUAL) */}
            <Card className="md:col-span-2 bg-black border-neutral-900 overflow-hidden relative">
                <CardHeader>
                    <CardTitle className="text-[10px] uppercase tracking-widest text-neutral-500 flex items-center gap-2">
                        <Share2 size={12} className="text-fuchsia-500" /> Collaborative Exploit Graph
                    </CardTitle>
                </CardHeader>
                <CardContent className="h-64 flex flex-col justify-end p-0">
                    <div className="p-4 space-y-4 max-h-full overflow-y-auto font-mono text-[9px]">
                        {insights.map((ins, i) => (
                            <div key={i} className="flex gap-4 items-start border-l border-neutral-800 pl-4 animate-in fade-in slide-in-from-left-4">
                                <div className="text-cyan-500 font-bold min-w-[80px]">{ins.team_id}</div>
                                <div className="text-neutral-400">
                                    <span className="text-neutral-600 mr-2">[{new Date(ins.timestamp).toLocaleTimeString()}]</span>
                                    {ins.data.detail}
                                </div>
                            </div>
                        ))}
                        {insights.length === 0 && (
                            <div className="flex items-center justify-center h-full text-neutral-700 italic">
                                Awaiting P2P Insight Propagation...
                            </div>
                        )}
                    </div>

                    <div className="absolute bottom-4 right-4 flex gap-2">
                        <Badge variant="outline" className="text-[8px] border-neutral-800 text-neutral-500">MAPPING_ATTACK_SURFACE</Badge>
                        <Badge variant="outline" className="text-[8px] border-neutral-800 text-orange-500 animate-pulse">LATTICE_SYNC_OK</Badge>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
