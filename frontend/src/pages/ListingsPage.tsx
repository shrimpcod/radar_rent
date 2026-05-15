import { useState, useEffect } from "react"
import { useQuery } from "@tanstack/react-query"
import StatsCards from "../features/listings/StatsCards"
import ListingsTable from "../features/listings/ListingsTable"
import type { LeadStats, Lead, LeadAction, Favorite } from "../types/listings"
import { getLeads, getLeadsCount, getUserLeadActions, getUserFavorites } from "../api/listings"

const mockStats: LeadStats = {
    total_calls: 0,
    closed: 0,
    no_answer: 0,
    not_closed: 0
}

export default function ListingsPage() {
    const [page, setPage] = useState(1)
    const limit = 12

    const { data, isLoading } = useQuery<Lead[]>({
        queryKey: ["leads", page],
        queryFn: () => getLeads((page - 1) * limit, limit)
    })

    const { data: count } = useQuery<number>({
        queryKey: ["leads-count"],
        queryFn: getLeadsCount
    })

    const {data: userActions } = useQuery<LeadAction[]>({
        queryKey: ["lead-actions"],
        queryFn: getUserLeadActions
    })

    const { data: favorites } = useQuery<Favorite[]>({
        queryKey: ["favorites"],
        queryFn: getUserFavorites
    })

    const [leads, setLeads] = useState<Lead[]>([])
    const [newLeadIds, setNewLeadIds] = useState<Set<number>>(new Set())

    useEffect(() => {
        if (data) setLeads(data)
    }, [data])

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/api/v1/ws")
        ws.onmessage = (event) => {
            const newLead: Lead = JSON.parse(event.data)
            if (page === 1) {
                setLeads(prev => {
                    if (prev.some(l => l.id === newLead.id)) return prev
                    return [newLead, ...prev.slice(0, limit - 1)]
                })
            }
            setNewLeadIds(prev => new Set(prev).add(newLead.id))
            setTimeout(() => {
                setNewLeadIds(prev => {
                    const next = new Set(prev)
                    next.delete(newLead.id)
                    return next
                })
            }, 5000)
        }
        return () => ws.close()
    }, [page])

    const totalPages = count ? Math.ceil(count / limit) : 1

    return (
        <div className="p-6" style={{ minHeight: '100%' }}>
            <StatsCards stats={mockStats} />
            {isLoading ? (
                <div className="text-gray-400 text-sm p-4">Загрузка...</div>
            ) : (
                <ListingsTable 
                    leads={leads} 
                    newLeadIds={newLeadIds} 
                    userActions={userActions ?? []}
                    favorites={favorites ?? []}
                />
            )}
            <div className="flex justify-end gap-2 mt-4">
                {(() => {
                    const pages: (number | '...')[] = []

                    if (totalPages <= 7) {
                        for (let i = 1; i <= totalPages; i++) pages.push(i)
                    } else {
                        pages.push(1)
                        if (page > 3) pages.push('...')
                        for (let i = Math.max(2, page - 1); i <= Math.min(totalPages - 1, page + 1); i++) {
                            pages.push(i)
                        }
                        if (page < totalPages - 2) pages.push('...')
                        pages.push(totalPages)
                    }

                    return pages.map((p, i) =>
                        p === '...' ? (
                            <span key={`dots-${i}`} className="px-3 py-1.5 text-sm text-gray-400">...</span>
                        ) : (
                            <button
                                key={p}
                                onClick={() => setPage(p)}
                                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                                    page === p ? 'bg-[#3D3FAA] text-white' : 'bg-white text-gray-500 hover:bg-gray-100'
                                }`}
                            >
                                {p}
                            </button>
                        )
                    )
                })()}
            </div>
        </div>
    )
}
