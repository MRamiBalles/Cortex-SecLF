"use client"

import NeuroDashboard from "@/src/features/neuro/NeuroDashboard"

export default function NeuroPage() {
    return (
        <main className="flex min-h-screen flex-col items-center bg-black py-4">
            <div className="w-full max-w-7xl px-4 flex flex-col h-full">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-600 bg-clip-text text-transparent mb-2 flex items-center gap-3">
                    Cortex-Sec // Neuro-Rights Defense
                </h1>
                <p className="text-neutral-400 text-sm mb-4">ConsentChain™ Node: Active // Enforcement: Hardware-Level</p>
                <NeuroDashboard />
            </div>
        </main>
    )
}
