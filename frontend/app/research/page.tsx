"use client"

import ResearchLab from "@/src/features/research/ResearchLab"

export default function ResearchPage() {
    return (
        <main className="flex min-h-screen flex-col items-center bg-black py-4">
            <div className="w-full max-w-7xl px-4 flex flex-col h-full">
                <h1 className="text-2xl font-bold text-neutral-200 mb-2 flex items-center gap-3">
                    <span className="text-cyan-500 font-mono">AI SCIENTIST //</span> Autonomous Research Hub
                </h1>
                <ResearchLab />
            </div>
        </main>
    )
}
