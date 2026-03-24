import type { LeadStats } from "../../types/listings"

interface Props{
    stats: LeadStats
}

export default function StatsCards({ stats }: Props) {
    const conversion = stats.total_calls > 0 ? Math.round((stats.closed / stats.total_calls) * 100) : 0

    const cards = [
        {label: 'Всего звонков', value: stats.total_calls, color: '#3B82F6'},
        {label: 'Закрыл', value: stats.closed, color: '#22C55E'},
        {label: 'Недозвон', value: stats.no_answer, color: '#EAB308'},
        {label: 'Не закрыл', value: stats.not_closed, color: '#EF4444'},
        {label: 'Конверсия ', value: `${conversion}%`, color: '#3B82F6'},
    ]

    return(
        <div className="inline-flex gap-4 mb-6">
            {cards.map((card) => (
                <div 
                    key={card.label}    
                    className="flex items-center gap-4 bg-white rounded-xl px-5 py-4 shadow-sm w-48"
                    style={{ borderLeft: `4px solid ${card.color}`}}
                >
                    <span className="text-2xl font-bold" style={{ color: card.color }}>{card.value}</span>
                    <span className="text-sm text-gray-400">{card.label}</span>
                </div>
            ))}
        </div>
    )
}