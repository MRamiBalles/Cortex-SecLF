"use client"

import Link from 'next/link'
import React from 'react'
import { Shield, Cpu, Activity, Database, Zap, Brain, ExternalLink } from 'lucide-react'

export default function LandingPage() {
    return (
        <main className="flex min-h-screen flex-col items-center bg-black text-white p-8 md:p-24 overflow-x-hidden relative">
            {/* BACKGROUND ANIMATION */}
            <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none opacity-20">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-cyan-500/20 blur-[120px] rounded-full animate-pulse"></div>
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-500/20 blur-[120px] rounded-full animate-pulse"></div>
            </div>

            {/* HERO SECTION */}
            <div className="z-10 text-center mb-20 max-w-4xl pt-10">
                <div className="inline-block px-4 py-1 mb-6 rounded-full border border-neutral-800 bg-neutral-900/50 text-cyan-400 text-[10px] font-mono tracking-[0.3em] uppercase animate-in fade-in slide-in-from-bottom-4 duration-1000">
                    Sovereign AI Governance // Phase 2: Active
                </div>
                <h1 className="text-6xl md:text-8xl font-black mb-6 tracking-tighter bg-gradient-to-b from-white to-neutral-500 bg-clip-text text-transparent italic">
                    NEXUS <span className="not-italic text-cyan-500 text-4xl md:text-5xl align-top">v2.0</span>
                </h1>
                <p className="text-neutral-400 text-lg md:text-xl font-medium max-w-2xl mx-auto leading-relaxed">
                    The local-first command interface for the <span className="text-white">Cortex-SecLF</span> autonomous security lattice.
                </p>
            </div>

            {/* MODULE GRID - 2x3 for all 6 modules */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full max-w-7xl z-10 mb-20">

                <ModuleCard
                    title="Agent Lab"
                    description="Real-time security monitoring and active containment of AI agents."
                    icon={<Shield size={24} />}
                    href="/lab"
                    color="red"
                />

                <ModuleCard
                    title="Scientist"
                    description="Autonomous research cycles grounded in factual canonical data."
                    icon={<Cpu size={24} />}
                    href="/research"
                    color="purple"
                />

                <ModuleCard
                    title="Dojo"
                    description="Interactive environments for defensive training and vulnerability auditing."
                    icon={<Zap size={24} />}
                    href="/dojo"
                    color="emerald"
                />

                <ModuleCard
                    title="Archive"
                    description="The Sovereign Knowledge Ledger. Auditable records of all system data."
                    icon={<Database size={24} />}
                    href="/archive"
                    color="blue"
                />

                <ModuleCard
                    title="Neuro-Rights"
                    description="Mental privacy defense via HIVE-Net Distributed Consensus."
                    icon={<Brain size={24} />}
                    href="/neuro"
                    color="purple"
                />

                <ModuleCard
                    title="Gap Analyzer"
                    description="Identifies knowledge asymmetry and triggers autonomous patching."
                    icon={<Activity size={24} />}
                    href="/gaps"
                    color="orange"
                />

            </div>

            {/* FOOTER / SYSTEM STATUS */}
            <div className="w-full max-w-7xl flex flex-col lg:flex-row justify-between items-center border-t border-neutral-900 pt-8 text-[10px] font-mono text-neutral-600 gap-4 z-10">
                <div className="flex gap-8 uppercase tracking-widest">
                    <span>Air-Gap Mode: <span className="text-emerald-500">ENFORCED</span></span>
                    <span>Vector DB: <span className="text-white">CHROMA_LOCAL</span></span>
                    <span>Agent Model: <span className="text-white">OLLAMA/L3B</span></span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="flex -space-x-2">
                        {[1, 2, 3].map(i => <div key={i} className="w-5 h-5 rounded-full border border-black bg-neutral-800 flex items-center justify-center text-[8px] text-neutral-400">A{i}</div>)}
                    </div>
                    <span className="ml-2 uppercase tracking-widest text-neutral-400">Neural Lattice Active</span>
                </div>
            </div>
        </main>
    )
}

function ModuleCard({ title, description, icon, href, color }: { title: string, description: string, icon: React.ReactNode, href: string, color: string }) {
    const colorMap: Record<string, string> = {
        blue: "group-hover:text-blue-400 group-hover:bg-blue-500/10",
        red: "group-hover:text-red-400 group-hover:bg-red-500/10",
        purple: "group-hover:text-purple-400 group-hover:bg-purple-500/10",
        emerald: "group-hover:text-emerald-400 group-hover:bg-emerald-500/10",
        orange: "group-hover:text-orange-400 group-hover:bg-orange-500/10"
    }

    const borderColor: Record<string, string> = {
        blue: "group-hover:border-blue-500/50",
        red: "group-hover:border-red-500/50",
        purple: "group-hover:border-purple-500/50",
        emerald: "group-hover:border-emerald-500/50",
        orange: "group-hover:border-orange-500/50"
    }

    return (
        <Link href={href} className="group relative">
            <div className={`p-8 bg-neutral-900/40 border border-neutral-800 rounded-3xl h-full transition-all duration-500 hover:-translate-y-2 backdrop-blur-sm shadow-xl ${borderColor[color] || 'group-hover:border-cyan-500/50'}`}>
                <div className={`mb-6 p-4 rounded-xl w-fit transition-all duration-500 ${colorMap[color] || 'group-hover:text-cyan-400 group-hover:bg-cyan-500/10'} bg-neutral-800 text-neutral-500`}>
                    {icon}
                </div>
                <h2 className="text-2xl font-bold mb-4 group-hover:tracking-tight transition-all">
                    {title} <ExternalLink size={14} className="inline opacity-0 group-hover:opacity-100 transition-all -translate-y-1 ml-1" />
                </h2>
                <p className="text-sm text-neutral-500 leading-relaxed font-medium">
                    {description}
                </p>

                <div className="absolute bottom-6 right-8 text-[10px] font-mono text-neutral-800 group-hover:text-neutral-500 transition-colors uppercase tracking-widest">
                    Initialize Module
                </div>
            </div>
        </Link>
    )
}
