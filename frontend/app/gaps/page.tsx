"use client"

import GapDashboard from "@/src/features/gaps/GapDashboard"

export default function GapsPage() {
    return (
        <main className="flex min-h-screen flex-col items-center bg-black py-4">
            <div className="w-full max-w-7xl px-4 flex flex-col h-full">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-orange-400 to-red-600 bg-clip-text text-transparent mb-2 flex items-center gap-3">
                    Cortex-Sec // Knowledge Gap Analyzer
                </h1>
                <p className="text-neutral-400 text-sm mb-4">HIVE Bridge: ACTIVE // Red-Blue Parity: CALCULATING</p>
                <GapDashboard />
            </div>
        </main>
    )
}
