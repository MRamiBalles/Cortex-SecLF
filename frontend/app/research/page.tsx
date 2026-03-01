"use client"

import ResearchLab from "@/src/features/research/ResearchLab"
import MartDashboard from "@/src/features/scientist/MartDashboard"

export default function ResearchPage() {
    return (
        <main className="flex min-h-screen flex-col items-center bg-black py-4">
            <div className="w-full max-w-7xl px-4 flex flex-col h-full space-y-8">
                <div>
                    <h1 className="text-2xl font-bold text-neutral-200 mb-2 flex items-center gap-3">
                        <span className="text-cyan-500 font-mono">MART CLUSTER //</span> Distributed Coordination
                    </h1>
                    <MartDashboard />
                </div>

                <div>
                    <h2 className="text-xl font-bold text-neutral-400 mb-4 flex items-center gap-3">
                        <span className="text-fuchsia-500 font-mono">LOCAL_HIVE //</span> Pipeline Execution
                    </h2>
                    <ResearchLab />
                </div>
            </div>
        </main>
    )
}
