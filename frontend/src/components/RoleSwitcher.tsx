"use client"

import React from 'react';
import { useRole, UserRole } from '@/src/context/RoleContext';
import { User, Shield, Briefcase, ChevronRight } from 'lucide-react';

export default function RoleSwitcher() {
    const { role, setRole } = useRole();

    const roles: { id: UserRole, icon: React.ReactNode, label: string }[] = [
        { id: 'CISO', icon: <Shield size={12} />, label: 'Chief Info Security Officer' },
        { id: 'ARCHITECT', icon: <Briefcase size={12} />, label: 'Security Architect' },
        { id: 'ANALYST', icon: <User size={12} />, label: 'Forensic Analyst' },
    ];

    return (
        <div className="fixed bottom-6 left-6 z-[100] group">
            <div className="bg-neutral-900 border border-neutral-800 rounded-full py-2 px-4 shadow-2xl flex items-center gap-3 hover:border-neutral-600 transition-all cursor-pointer overflow-hidden max-w-[40px] group-hover:max-w-[500px] duration-500 group-hover:pr-6 whitespace-nowrap">
                <div className="text-cyan-500 animate-pulse">
                    {roles.find(r => r.id === role)?.icon}
                </div>

                <div className="flex items-center gap-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <span className="text-[10px] font-black tracking-tighter text-neutral-400 font-mono uppercase">{role}</span>
                    <div className="flex gap-2">
                        {roles.map(r => (
                            <button
                                key={r.id}
                                onClick={() => setRole(r.id)}
                                className={`text-[8px] font-mono px-2 py-0.5 rounded border transition-all ${role === r.id ? 'bg-cyan-500/20 border-cyan-500 text-cyan-500' : 'bg-neutral-950 border-neutral-900 text-neutral-600 hover:border-neutral-700'}`}
                            >
                                {r.id}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="group-hover:hidden absolute right-3 top-1/2 -translate-y-1/2 text-neutral-700">
                    <ChevronRight size={10} />
                </div>
            </div>
        </div>
    );
}
