"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Database, Search, FileCode, ShieldCheck, History, Clock } from "lucide-react"
import { Input } from "@/components/ui/input"

export default function ArchivePage() {
    // Mock archive data reflecting the RAG collections
    const collections = [
        { name: "DOCTRINE", count: 124, status: "READY", icon: ShieldCheck, color: "text-blue-400" },
        { name: "TRENCH", count: 89, status: "INDEXING", icon: FileCode, color: "text-amber-400" },
    ]

    const entries = [
        { id: "0X-AF1", collection: "DOCTRINE", title: "Cortex Security Protocol III", date: "2024-05-12", authority: 0.98 },
        { id: "0X-TR2", collection: "TRENCH", title: "Memory Corruption in Kernel v6.1", date: "2024-05-11", authority: 0.75 },
        { id: "0X-AF3", collection: "DOCTRINE", title: "Autonomous Containment Ethics", date: "2024-05-10", authority: 0.95 },
        { id: "0X-TR4", collection: "TRENCH", title: "LLM-Aided Fuzzing Techniques", date: "2024-05-09", authority: 0.82 },
    ]

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-1000">
            <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <h1 className="text-4xl font-black tracking-tighter text-white flex items-center gap-3">
                        <Database className="text-cyan-500" size={36} /> CANONICAL ARCHIVE
                    </h1>
                    <p className="text-neutral-500 font-mono text-sm mt-2 uppercase tracking-widest">
                        Permanent Knowledge Ledger for Sovereign Governance
                    </p>
                </div>
                <div className="flex gap-2">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-600" size={16} />
                        <Input
                            className="bg-neutral-900 border-neutral-800 pl-10 w-64 text-xs font-mono focus:border-cyan-500"
                            placeholder="SEARCH ACROSS REGISTRIES..."
                        />
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* COLLECTIONS INFO */}
                <div className="md:col-span-1 space-y-6">
                    {collections.map((c) => (
                        <Card key={c.name} className="bg-neutral-900 border-neutral-800 hover:border-neutral-700 transition-colors shadow-xl">
                            <CardHeader className="flex flex-row items-center justify-between pb-2">
                                <div className="flex items-center gap-3">
                                    <div className={`p-2 bg-black/50 rounded-lg ${c.color}`}>
                                        <c.icon size={20} />
                                    </div>
                                    <div>
                                        <CardTitle className="text-sm font-bold tracking-widest uppercase">{c.name}</CardTitle>
                                        <CardDescription className="text-[10px] font-mono">COLLECTION CORE</CardDescription>
                                    </div>
                                </div>
                                <Badge variant="outline" className={`text-[10px] font-mono ${c.status === 'READY' ? 'border-blue-900 text-blue-400' : 'border-amber-900 text-amber-400'}`}>
                                    {c.status}
                                </Badge>
                            </CardHeader>
                            <CardContent>
                                <div className="flex items-end justify-between">
                                    <div className="text-3xl font-black text-white">{c.count}</div>
                                    <div className="text-[10px] text-neutral-500 font-mono uppercase">Indexed Artifacts</div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}

                    <Card className="bg-neutral-950 border-neutral-800/50 border-dashed border-2">
                        <CardContent className="h-32 flex flex-col items-center justify-center text-neutral-700 font-mono text-xs uppercase text-center p-6">
                            <Clock size={24} className="mb-2 opacity-50" />
                            Next Sync Scheduled in 4h 12m
                        </CardContent>
                    </Card>
                </div>

                {/* LEDGER ENTRIES */}
                <Card className="md:col-span-2 bg-neutral-900/50 border-neutral-800 shadow-2xl flex flex-col overflow-hidden">
                    <CardHeader className="border-b border-neutral-800 bg-neutral-950/50">
                        <CardTitle className="text-xs font-mono text-neutral-400 flex items-center gap-2">
                            <History size={14} /> RECENT REGISTRY UPDATES
                        </CardTitle>
                    </CardHeader>
                    <ScrollArea className="flex-1 h-[600px]">
                        <div className="divide-y divide-neutral-800">
                            {entries.map((e) => (
                                <div key={e.id} className="p-4 hover:bg-black/30 transition-colors flex items-center justify-between group">
                                    <div className="flex items-center gap-4">
                                        <div className="text-xs font-mono text-neutral-600 w-16">{e.id}</div>
                                        <div>
                                            <div className="text-sm font-bold text-neutral-200 group-hover:text-cyan-400 transition-colors">{e.title}</div>
                                            <div className="flex gap-2 mt-1">
                                                <Badge className="bg-black text-[10px] font-mono border-neutral-700 h-4 px-1">{e.collection}</Badge>
                                                <span className="text-[10px] text-neutral-600 font-mono">{e.date}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-[10px] text-neutral-500 font-mono uppercase mb-1 tracking-tighter">Authority Score</div>
                                        <div className="h-1.5 w-24 bg-neutral-800 rounded-full overflow-hidden">
                                            <div
                                                className="h-full bg-cyan-600"
                                                style={{ width: `${e.authority * 100}%` }}
                                            />
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </ScrollArea>
                </Card>
            </div>
        </div>
    )
}
