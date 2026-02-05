"use client"

import GapDashboard from "@/src/features/gap_analysis/GapDashboard"

export default function GapPage() {
    return (
        <main className="flex min-h-screen flex-col items-center bg-black py-10">
            <div className="w-full max-w-7xl px-4">
                <h1 className="text-3xl font-bold bg-gradient-to-r from-red-500 to-orange-600 bg-clip-text text-transparent mb-2">
                    Gap Detection Engine
                </h1>
                <p className="text-neutral-400 mb-8">Analyzing Knowledge Asymmetries and Missing Doctrine.</p>
                <GapDashboard />
            </div>
        </main>
    )
}
