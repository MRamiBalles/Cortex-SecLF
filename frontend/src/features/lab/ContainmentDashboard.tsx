"use client"

import React, { useState, useEffect, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/src/components/ui/card"
import { Button } from "@/src/components/ui/button"
import { Badge } from "@/src/components/ui/badge"
import { Input } from "@/src/components/ui/input"
import { ShieldAlert, ShieldCheck, History, ZapOff, Search } from 'lucide-react'

interface Incident {
    id: string
    timestamp: string
    agent_id: string
    policy: string
    breach_type: string
    evidence: string
    action: string
}

interface PolicyData {
    active_policy: string
    available_policies: string[]
    [key: string]: any
}

export default function ContainmentDashboard() {
    const [policy, setPolicy] = useState<PolicyData | null>(null)
    const [incidents, setIncidents] = useState<Incident[]>([])
    const [loading, setLoading] = useState(true)
    const [searchTerm, setSearchTerm] = useState("")
    const [filterAction, setFilterAction] = useState<string | null>(null)

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    const fetchData = async () => {
        try {
            const pRes = await fetch(`${API_URL}/containment/policy`)
            const iRes = await fetch(`${API_URL}/containment/incidents`)
            const pData: PolicyData = await pRes.json()
            const iData = await iRes.json()
            setPolicy(pData)
            setIncidents(iData.incidents || [])
        } catch (e: unknown) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    const updatePolicy = async (pName: string) => {
        try {
            await fetch(`${API_URL}/containment/policy`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ policy: pName })
            })
            fetchData()
        } catch (e: unknown) {
            console.error(e)
        }
    }

    useEffect(() => {
        fetchData()
        const interval = setInterval(fetchData, 5000)
        return () => clearInterval(interval)
    }, [API_URL])

    const filteredIncidents = useMemo(() => {
        return incidents.filter((inc: Incident) => {
            const matchesSearch = inc.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                inc.breach_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
                inc.evidence.toLowerCase().includes(searchTerm.toLowerCase());
            const matchesFilter = filterAction ? inc.action === filterAction : true;
            return matchesSearch && matchesFilter;
        });
    }, [incidents, searchTerm, filterAction]);

    if (loading) return (
        <div className="flex items-center justify-center p-20">
            <div className="text-red-500 animate-pulse font-mono uppercase tracking-[0.3em] text-xs">
                Establishing Secure Link...
            </div>
        </div>
    )

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {policy?.available_policies.map((pName: string) => (
                    <Card
                        key={pName}
                        className={`cursor-pointer border-2 transition-all duration-500 group relative ${policy.active_policy === pName ? 'bg-red-950/20 border-red-500 shadow-[0_0_30px_rgba(239,68,68,0.2)]' : 'bg-neutral-900 border-neutral-800 hover:border-neutral-600'}`}
                        onClick={() => updatePolicy(pName)}
                    >
                        <CardHeader className="p-4">
                            <CardTitle className="text-sm flex items-center justify-between mb-1">
                                <span className={`${policy.active_policy === pName ? 'text-red-400' : 'text-neutral-400'} font-black tracking-tighter`}>{pName}</span>
                                {policy.active_policy === pName && <Badge className="bg-red-500 animate-pulse text-[8px] h-4">ACTIVE</Badge>}
                            </CardTitle>
                            <CardDescription className="text-[10px] leading-tight text-neutral-500 group-hover:text-neutral-300">
                                {pName === 'STRICT' && "Zero-Tolerance. Kernel-level termination."}
                                {pName === 'BALANCED' && "Standard Isolation. Pause & Audit flow."}
                                {pName === 'PERMISSIVE' && "Logging Only. No automated enforcement."}
                            </CardDescription>
                        </CardHeader>
                    </Card>
                ))}
            </div>

            <Card className="bg-black border-neutral-800 shadow-2xl overflow-hidden flex flex-col h-[500px]">
                <CardHeader className="flex flex-row items-center justify-between bg-neutral-900/30 border-b border-neutral-800 p-4">
                    <div className="space-y-1">
                        <CardTitle className="text-red-500 flex items-center gap-2 font-black italic tracking-tighter text-base">
                            <History size={18} className="animate-spin-slow" /> INCIDENT LEDGER
                        </CardTitle>
                    </div>

                    <div className="flex items-center gap-2">
                        <div className="relative">
                            <Search size={12} className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-600" />
                            <Input
                                placeholder="SEARCH..."
                                className="h-8 w-32 bg-neutral-950 border-neutral-800 pl-8 text-[9px] font-mono focus:ring-1 focus:ring-red-500"
                                value={searchTerm}
                                onChange={(e: any) => setSearchTerm(e.target.value)}
                            />
                        </div>

                        <div className="flex gap-1">
                            {['KILLED', 'PAUSED'].map(act => (
                                <Button
                                    key={act}
                                    variant="outline"
                                    className={`h-7 px-2 text-[8px] border-neutral-800 ${filterAction === act ? 'bg-red-900/40 border-red-500 text-red-500' : 'text-neutral-500'}`}
                                    onClick={() => setFilterAction(filterAction === act ? null : act)}
                                >
                                    {act}
                                </Button>
                            ))}
                        </div>
                    </div>
                </CardHeader>

                <CardContent className="p-0 flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-red-900/50">
                    {filteredIncidents.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-20 text-neutral-700 font-mono text-[10px] gap-3">
                            <ShieldCheck size={32} className="opacity-10" />
                            <p className="tracking-[0.2em]">SYSTEM SECURE // NO BREACHES</p>
                        </div>
                    ) : (
                        <div className="divide-y divide-neutral-900">
                            {filteredIncidents.map((incident: Incident) => (
                                <div key={incident.id} className="p-5 hover:bg-red-500/[0.02] transition-colors group">
                                    <div className="flex justify-between items-start mb-2">
                                        <div className="text-[9px] font-black text-red-500 font-mono uppercase">
                                            {incident.id} // {incident.breach_type}
                                        </div>
                                        <Badge className="text-[8px] bg-red-950/40 text-red-500 border-red-900 border px-2 py-0 h-4">
                                            <ZapOff size={8} className="mr-1" /> {incident.action}
                                        </Badge>
                                    </div>

                                    <div className="flex gap-3 text-[9px] text-neutral-600 font-mono mb-3 uppercase tracking-tighter">
                                        <span>AGNT: {incident.agent_id}</span>
                                        <span>POL: {incident.policy}</span>
                                        <span>TS: {incident.timestamp}</span>
                                    </div>

                                    <div className="bg-neutral-950 p-3 rounded border border-neutral-800">
                                        <pre className="text-[9px] font-mono text-red-400/70 whitespace-pre-wrap">
                                            {incident.evidence}
                                        </pre>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </CardContent>

                <div className="p-2 bg-neutral-900/50 border-t border-neutral-800 flex justify-between items-center text-[7px] font-mono text-neutral-700 uppercase tracking-widest">
                    <span>Immutable Ledger Active</span>
                    <span className="flex items-center gap-1">
                        <span className="w-1 h-1 rounded-full bg-emerald-500 animate-pulse"></span>
                        Lattice Sync Online
                    </span>
                </div>
            </Card>
        </div>
    )
}
