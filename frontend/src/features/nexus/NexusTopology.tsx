"use client"

import React, { useEffect, useRef, useState } from 'react';
import { Card, CardContent } from "@/src/components/ui/card"
import { Share2, Shield, Database, Microscope, Zap, Lock, Link } from 'lucide-react'

interface NodePos {
    id: string
    x: number
    y: number
    label: string
    icon: React.ReactNode
    color: string
}

export default function NexusTopology() {
    const canvasRef = useRef<HTMLCanvasElement>(null)
    const [hoveredNode, setHoveredNode] = useState<string | null>(null)

    const nodes: NodePos[] = [
        { id: 'archive', x: 200, y: 150, label: 'ARCHIVE_VAULT', icon: <Database size={16} />, color: '#3b82f6' },
        { id: 'ipfs', x: 100, y: 250, label: 'IPFS_MESH', icon: <Link size={16} />, color: '#06b6d4' },
        { id: 'tpm', x: 550, y: 300, label: 'TPM2_ROOT', icon: <Lock size={16} />, color: '#f59e0b' },
        { id: 'scientist', x: 400, y: 100, label: 'HIVE_SCIENTIST', icon: <Microscope size={16} />, color: '#a855f7' },
        { id: 'dojo', x: 600, y: 150, label: 'DOJO_RANGE', icon: <Zap size={16} />, color: '#eab308' },
        { id: 'neuro', x: 400, y: 300, label: 'NEURO_DEFENCE', icon: <Shield size={16} />, color: '#ef4444' },
        { id: 'core', x: 400, y: 200, label: 'LATTICE_CORE', icon: <Share2 size={16} />, color: '#10b981' },
    ]

    const edges = [
        ['archive', 'ipfs'],
        ['ipfs', 'core'],
        ['core', 'tpm'],
        ['tpm', 'neuro'],
        ['archive', 'scientist'],
        ['scientist', 'dojo'],
        ['dojo', 'core'],
        ['core', 'neuro'],
        ['core', 'archive'],
        ['scientist', 'core']
    ]

    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return
        const ctx = canvas.getContext('2d')
        if (!ctx) return

        let animationFrameId: number

        const draw = (time: number) => {
            ctx.clearRect(0, 0, canvas.width, canvas.height)

            // DRAW EDGES
            edges.forEach(([fromId, toId]) => {
                const from = nodes.find(n => n.id === fromId)!
                const to = nodes.find(n => n.id === toId)!

                ctx.beginPath()
                ctx.moveTo(from.x, from.y)
                ctx.lineTo(to.x, to.y)
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)'
                ctx.lineWidth = 1
                ctx.stroke()

                // Animated Pulse
                const progress = (time / 2000) % 1
                const px = from.x + (to.x - from.x) * progress
                const py = from.y + (to.y - from.y) * progress

                ctx.beginPath()
                ctx.arc(px, py, 2, 0, Math.PI * 2)
                ctx.fillStyle = from.color + '44'
                ctx.fill()
            })

            // DRAW GLOWS
            nodes.forEach(node => {
                const gradient = ctx.createRadialGradient(node.x, node.y, 0, node.x, node.y, 40)
                gradient.addColorStop(0, node.color + '22')
                gradient.addColorStop(1, 'transparent')
                ctx.fillStyle = gradient
                ctx.fillRect(node.x - 40, node.y - 40, 80, 80)
            })

            animationFrameId = requestAnimationFrame(draw)
        }

        draw(0)
        return () => cancelAnimationFrame(animationFrameId)
    }, [])

    return (
        <Card className="bg-black border-neutral-900 overflow-hidden relative group">
            <div className="absolute top-4 left-4 z-10">
                <h3 className="text-[10px] font-black text-neutral-600 uppercase tracking-[0.3em] mb-1">Infrastructure Matrix</h3>
                <div className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span className="text-[8px] font-mono text-emerald-500/70 uppercase">Lattice Mesh Active</span>
                </div>
            </div>

            <canvas
                ref={canvasRef}
                width={800}
                height={400}
                className="w-full h-auto opacity-80"
            />

            <div className="absolute inset-0 pointer-events-none">
                {nodes.map(node => (
                    <div
                        key={node.id}
                        className="absolute -translate-x-1/2 -translate-y-1/2 pointer-events-auto cursor-crosshair"
                        style={{ left: `${(node.x / 800) * 100}%`, top: `${(node.y / 400) * 100}%` }}
                        onMouseEnter={() => setHoveredNode(node.id)}
                        onMouseLeave={() => setHoveredNode(null)}
                    >
                        <div className="flex flex-col items-center gap-2">
                            <div className={`p-2 rounded-lg bg-black border transition-all duration-500 ${hoveredNode === node.id ? 'border-neutral-400 scale-110 shadow-[0_0_20px_rgba(255,255,255,0.1)]' : 'border-neutral-800'}`} style={{ color: node.color }}>
                                {node.icon}
                            </div>
                            <span className="text-[7px] font-mono text-neutral-600 bg-black/80 px-1 uppercase tracking-tighter">
                                {node.label}
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            <div className="absolute bottom-4 right-4 text-right">
                <p className="text-[8px] font-mono text-neutral-700 uppercase">Topology Mode: Dynamic</p>
                <p className="text-[6px] font-mono text-neutral-800 uppercase mt-1">Coord: 0x44.77.22.99 // Sec: Hardened</p>
            </div>
        </Card>
    )
}
