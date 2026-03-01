import Link from "next/link";
import { Activity, Database, Shield, Cpu, ExternalLink, Zap } from "lucide-react";

export default function Home() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-between p-8 lg:p-24 bg-[#0a0a0a] text-white selection:bg-cyan-500/30">
            {/* TOP BAR / NAVIGATION HEADER */}
            <div className="z-20 max-w-7xl w-full flex items-center justify-between font-mono text-sm mb-12">
                <div className="flex items-center gap-3 bg-neutral-900/50 px-4 py-2 rounded-full border border-neutral-800 backdrop-blur-md">
                    <span className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(6,182,212,0.8)]"></span>
                    <span className="text-neutral-400">CORTEX-SEC <span className="text-white font-bold">LOCAL FORGE</span></span>
                    <span className="text-neutral-600">|</span>
                    <code className="text-cyan-500">v1.2.0-Sovereign</code>
                </div>

                <div className="hidden lg:flex items-center gap-6 text-neutral-500">
                    <div className="flex items-center gap-2">
                        <Activity size={14} className="text-emerald-500" />
                        <span>HIVE: <span className="text-white">ACTIVE</span></span>
                    </div>
                    <div className="flex items-center gap-2">
                        <Shield size={14} className="text-blue-500" />
                        <span>ISOLATION: <span className="text-white">LEVEL-4</span></span>
                    </div>
                </div>
            </div>

            {/* HERO SECTION */}
            <div className="relative flex flex-col items-center justify-center py-20 z-10 text-center">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-cyan-500/10 rounded-full blur-[120px] pointer-events-none"></div>

                <h1 className="text-8xl font-black tracking-tighter mb-4 italic">
                    <span className="text-transparent bg-clip-text bg-gradient-to-b from-white to-neutral-600">NEXUS</span>
                </h1>
                <p className="text-neutral-500 font-mono tracking-widest text-xs uppercase max-w-md">
                    Autonomous AI Governance & Cybersecurity Sovereignty Engine
                </p>

                <div className="mt-12 flex gap-4">
                    <div className="h-[1px] w-20 bg-gradient-to-r from-transparent to-neutral-800 mt-3"></div>
                    <Zap className="text-cyan-500 animate-bounce" size={20} />
                    <div className="h-[1px] w-20 bg-gradient-to-l from-transparent to-neutral-800 mt-3"></div>
                </div>
            </div>

            {/* MODULE GRID */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 w-full max-w-7xl z-10 mb-20">

                <ModuleCard
                    title="Archive"
                    description="Canonical RAG Engine grounded in technical doctrine and exploit lore."
                    icon={<Database />}
                    href="/archive"
                    color="blue"
                />

                <ModuleCard
                    title="Agent Lab"
                    description="Secure containment and Kill-Switch protocols for testing rogue agents."
                    icon={<Shield />}
                    href="/lab"
                    color="red"
                />

                <ModuleCard
                    title="Scientist"
                    description="Autonomous research cycles: Hypothesis -> Realization -> Peer Review."
                    icon={<Cpu />}
                    href="/research"
                    color="purple"
                />

                <ModuleCard
                    title="Dojo"
                    description="Managed vulnerable environments for defensive training and auditing."
                    icon={<Activity />}
                    href="/dojo"
                    color="emerald"
                />

            </div>

            {/* FOOTER / SYSTEM STATUS */}
            <div className="w-full max-w-7xl flex flex-col lg:flex-row justify-between items-center border-t border-neutral-900 pt-8 text-[10px] font-mono text-neutral-600 gap-4">
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
    );
}

function ModuleCard({ title, description, icon, href, color }: { title: string, description: string, icon: React.ReactNode, href: string, color: string }) {
    const colorMap: any = {
        blue: "group-hover:text-blue-400 group-hover:bg-blue-500/10",
        red: "group-hover:text-red-400 group-hover:bg-red-500/10",
        purple: "group-hover:text-purple-400 group-hover:bg-purple-500/10",
        emerald: "group-hover:text-emerald-400 group-hover:bg-emerald-500/10"
    }

    const borderColor: any = {
        blue: "group-hover:border-blue-500/50",
        red: "group-hover:border-red-500/50",
        purple: "group-hover:border-purple-500/50",
        emerald: "group-hover:border-emerald-500/50"
    }

    return (
        <Link href={href} className="group relative">
            <div className={`p-8 bg-neutral-900/40 border border-neutral-800 rounded-3xl h-full transition-all duration-500 hover:-translate-y-2 backdrop-blur-sm shadow-xl ${borderColor[color]}`}>
                <div className={`mb-6 p-4 rounded-xl w-fit transition-all duration-500 ${colorMap[color]} bg-neutral-800 text-neutral-500`}>
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
