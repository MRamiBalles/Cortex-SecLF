"use client"

import AgentLabDashboard from "@/src/features/lab/AgentLabDashboard"

export default function LabPage() {
    return (
        <main className="flex min-h-screen flex-col items-center bg-black py-4">
            <div className="w-full max-w-7xl px-4 flex flex-col h-full">
                <h1 className="text-2xl font-bold text-neutral-200 mb-2 flex items-center gap-3">
                    <span className="bg-red-600 w-3 h-3 rounded-full animate-pulse"></span>
                    Cortex-Sec // Agent Containment Lab
                </h1>
                <AgentLabDashboard />
            </div>
        </main>
    )
}
