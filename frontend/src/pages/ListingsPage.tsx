import StatsCards from "../features/listings/StatsCards"
import ListingsTable from "../features/listings/ListingsTable"
import type { LeadStats, Lead } from "../types/listings"
import { useQuery } from "@tanstack/react-query"
import { getLeads } from "../api/listings"
import { useState, useEffect } from "react"

const mockStats: LeadStats = {
    total_calls: 12,
    closed: 4,
    no_answer: 5,
    not_closed: 3
}

export default function ListingsPage() {
    const { data, isLoading } = useQuery<Lead[]>({
        queryKey: ["leads"],
        queryFn: getLeads 
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
            setLeads(prev => {
                if (prev.some(l => l.id === newLead.id)) return prev
                return [newLead, ...prev]
            })
            setNewLeadIds(prev => new Set(prev).add(newLead.id))
            setTimeout(() => {
                setNewLeadIds(prev => {
                    const next = new Set(prev)
                    next.delete(newLead.id)
                    return next
                })
            }, 3000)
        }
        return () => ws.close()
    }, [])

    return(
        <div className="p-6" style={{ minHeight: '100%' }}>
            <StatsCards stats={mockStats} />
            {isLoading ? (
                <div className="text-gray-400 text-sm p-4">Загрузка...</div>
            ) : (
                <ListingsTable leads={leads ?? []} newLeadIds={newLeadIds}/>
            )}
        </div>
    )
}