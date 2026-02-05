"use client"

import ChatInterface from "@/src/features/archive/ChatInterface"

export default function ArchivePage() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-center bg-black">
            <div className="w-full max-w-6xl p-4">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-emerald-600 bg-clip-text text-transparent mb-4">
                    Cortex-Sec // Archive // Nexus
                </h1>
                <ChatInterface />
            </div>
        </main>
    )
}
