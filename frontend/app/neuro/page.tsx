"use client"

import NeuroDashboard from "@/src/features/neuro/NeuroDashboard"
import MeshDashboard from "@/src/features/neuro/MeshDashboard"

export default function NeuroPage() {
    return (
        <main className="flex min-h-screen flex-col items-center bg-black py-4">
            <div className="w-full max-w-7xl px-4 flex flex-col h-full gap-4">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-600 bg-clip-text text-transparent mb-1 flex items-center gap-3">
                    Cortex-Sec // Neuro-Rights Defense
                </h1>
                <p className="text-neutral-400 text-xs mb-2 uppercase tracking-widest font-mono">Status: Hardened // Mesh: Cryptographically Linked</p>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2">
                        <NeuroDashboard />
                    </div>
                    <div>
                        <MeshDashboard />
                    </div>
                </div>
            </div>
        </main>
    )
}
