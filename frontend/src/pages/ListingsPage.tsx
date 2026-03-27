import StatsCards from "../features/listings/StatsCards"
import ListingsTable from "../features/listings/ListingsTable"
import type { LeadStats, Lead } from "../types/listings"
import { useQuery } from "@tanstack/react-query"
import { getLeads } from "../api/listings"

const mockStats: LeadStats = {
    total_calls: 12,
    closed: 4,
    no_answer: 5,
    not_closed: 3
}

export default function ListingsPage() {
    const { data: leads, isLoading } = useQuery<Lead[]>({
        queryKey: ["leads"],
        queryFn: getLeads 
    })

    return(
        <div className="p-6" style={{ minHeight: '100%' }}>
            <StatsCards stats={mockStats} />
            {isLoading ? (
                <div className="text-gray-400 text-sm p-4">Загрузка...</div>
            ) : (
                <ListingsTable leads={leads ?? []} />
            )}
        </div>
    )
}