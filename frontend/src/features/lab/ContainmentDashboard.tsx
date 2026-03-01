"use client"

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/src/components/ui/card"
import { Button } from "@/src/components/ui/button"
import { Badge } from "@/src/components/ui/badge"
import { ShieldAlert, ShieldCheck, ShieldOff, Activity, History, ZapOff } from 'lucide-react'

interface Incident {
    id: string
    timestamp: string
    agent_id: string
    policy: string
    breach_type: string
    evidence: string
    action: string
}

export default function ContainmentDashboard() {
    const [policy, setPolicy] = useState<any>(null)
    const [incidents, setIncidents] = useState<Incident[]>([])
    const [loading, setLoading] = useState(true)

    const fetchData = async () => {
        try {
            const pRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/containment/policy`)
            const iRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/containment/incidents`)
            const pData = await pRes.json()
            const iData = await iRes.json()
            setPolicy(pData)
            setIncidents(iData.incidents)
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    const updatePolicy = async (pName: string) => {
        try {
            await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/containment/policy`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ policy: pName })
            })
            fetchData()
        } catch (e) {
            console.error(e)
        }
    }

    useEffect(() => {
        fetchData()
        const interval = setInterval(fetchData, 5000)
        return () => clearInterval(interval)
    }, [])

    if (loading) return <div className="text-red-500 animate-pulse font-mono">Loading Containment Protocols...</div>

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {policy?.available_policies.map((pName: string) => (
                    <Card
                        key={pName}
                        className={`cursor-pointer border-2 transition-all duration-500 ${policy.active_policy === pName ? 'bg-red-950/20 border-red-500 shadow-[0_0_20px_rgba(239,68,68,0.2)]' : 'bg-neutral-900 border-neutral-800 hover:border-neutral-600'}`}
                        onClick={() => updatePolicy(pName)}
                    >
                        <CardHeader className="p-4">
                            <CardTitle className="text-sm flex items-center justify-between">
                                {pName}
                                {policy.active_policy === pName && <Badge className="bg-red-500">ACTIVE</Badge>}
                            </CardTitle>
                            <CardDescription className="text-[10px]">
                                {pName === 'STRICT' && "Zero-Tolerance. Auto-Kill on first anomaly."}
                                {pName === 'BALANCED' && "Standard Isolation. Pause & Audit."}
                                {pName === 'PERMISSIVE' && "Logging Only. No automated containment."}
                            </CardDescription>
                        </CardHeader>
                    </Card>
                ))}
            </div>

            <Card className="bg-black border-neutral-800">
                <CardHeader className="flex flex-row items-center justify-between">
                    <div>
                        <CardTitle className="text-red-500 flex items-center gap-2">
                            <History size={18} /> FORENSIC INCIDENT LEDGER
                        </CardTitle>
                        <CardDescription>Live audit of autonomous containment actions</CardDescription>
                    </div>
                    <Badge variant="outline" className="border-red-900 text-red-700">{incidents.length} INCIDENTS</Badge>
                </CardHeader>
                <CardContent className="space-y-2 max-h-[400px] overflow-y-auto scrollbar-thin scrollbar-thumb-red-900">
                    {incidents.length === 0 ? (
                        <div className="text-center py-10 text-neutral-600 font-mono text-xs italic">
                            No policy violations detected. System status: SECURE.
                        </div>
                    ) : (
                        incidents.map((incident) => (
                            <div key={incident.id} className="p-4 border border-red-900/30 bg-red-950/5 rounded-lg flex flex-col gap-2 hover:bg-red-950/10 transition-colors">
                                <div className="flex justify-between items-start">
                                    <span className="text-xs font-bold text-red-500 font-mono">{incident.id} // {incident.breach_type}</span>
                                    <Badge variant="destructive" className="text-[8px] bg-red-900/80 uppercase">
                                        <ZapOff size={8} className="mr-1" /> {incident.action}
                                    </Badge>
                                </div>
                                <div className="text-[10px] text-neutral-400 font-mono">
                                    <span className="text-neutral-600">AGENT:</span> {incident.agent_id} |
                                    <span className="text-neutral-600 ml-2">POLICY:</span> {incident.policy} |
                                    <span className="text-neutral-600 ml-2">TIME:</span> {incident.timestamp}
                                </div>
                                <div className="bg-black p-2 rounded border border-neutral-800 text-[10px] font-mono text-red-400/90 break-all">
                                    {incident.evidence}
                                </div>
                            </div>
                        ))
                    )}
                </CardContent>
            </Card>
        </div>
    )
}
