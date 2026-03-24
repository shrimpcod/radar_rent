import StatsCards from "../features/listings/StatsCards"
import ListingsTable from "../features/listings/ListingsTable"
import type { LeadStats, Lead } from "../types/listings"

const mockStats: LeadStats = {
    total_calls: 12,
    closed: 4,
    no_answer: 5,
    not_closed: 3
}

const mockLeads: Lead[] = [
    {
        id: 1,
        created_offer_at: '20.03.2026 10:30',
        object_info: '37 м², 0-к, 5/16 эт.',
        source: 'ЦИАН',
        price: 60000,
        address: 'Россия, Москва, Керамический проезд, 63к1',
        phone_number: '+79862741953',
    }, 
    {
        id: 2,
        created_offer_at: '20.03.2026 10:30',
        object_info: '37 м², 0-к, 5/16 эт.',
        source: 'ЦИАН',
        price: 60000,
        address: 'Россия, Москва, Керамический проезд, 63к1',
        phone_number: '+79862741953',
    }
]

export default function ListingsPage() {
    return(
        <div className="p-6" style={{ minHeight: '100%' }}>
            <StatsCards stats={mockStats} />
            <ListingsTable leads={mockLeads} />
        </div>
    )
}