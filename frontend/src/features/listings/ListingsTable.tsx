import { useState } from 'react';
import type { Lead } from '../../types/listings'

interface Props{
    leads: Lead[];
}

export default function ListingsTable({ leads }: Props) {
    const [favorites, setFavorites] = useState<'all' | 'favorites' | 'filters'>('all')

    const filterButtons = [
        {label: 'Все', value: 'all'},
        {label: 'Избранные', value: 'favorites'},
        {label: 'Фильтры', value: 'filters'}
    ]   

    const tableHeadRow = [
        {label: 'Дата и время'}, 
        {label: 'Объект'}, 
        {label: 'Источник'}, 
        {label: 'Цена (руб.)'}, 
        {label: 'Адрес'}, 
        {label: 'Контакт'}, 
        {label: 'Статус'}, 
        {label: 'Действия'}, 
    ]

    return(
        <div className='bg-white rounded-xl shadow-sm'>
            <div className='flex gap-2 p-4 border-b border-gray-100'>
                {filterButtons.map((btn) => (
                    <button
                        key={btn.value}
                        onClick={() => setFavorites(btn.value as 'all' | 'favorites')}
                        className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${favorites===btn.value ? 'bg-[#3D3FAA] text-white' : 'text-gray-500 hover:bg-gray-100'}`}
                    >
                        {btn.label}
                    </button>
                ))}
            </div>

            <table className='w-full'>
                <thead>
                    <tr className='text-left text-xs text-gray-400 uppercase'>
                        {tableHeadRow.map((thr) => (
                            <th key={thr.label} className='px-4 py-3'>{thr.label}</th>
                        ))}
                    </tr>
                </thead>

                <tbody>
                    {leads.map((lead) => (
                        <tr key={lead.id} className='border-t border-gray-100 hover:bg-gray-50 text-sm text-gray-700'>
                            <td className='px-4 py-3'>{lead.created_offer_at ? new Date(lead.created_offer_at).toLocaleString('ru-RU') : '-'}</td>
                            <td className='px-4 py-3'>{lead.rooms_count}-к, {lead.area} м², {lead.floor}/{lead.floors_count} эт.</td>
                            <td className='px-4 py-3'>ЦИАН</td>
                            <td className='px-4 py-3'>{lead.price.toLocaleString('ru-RU')}</td>
                            <td className='px-4 py-3'>{lead.address}</td>
                            <td className='px-4 py-3'>{lead.phone_number}</td>
                            <td className='px-4 py-3'>Статус</td>
                            <td className='px-4 py-3'>
                                <button className='text-[#3D3FAA] hover:underline text-xs'>П</button>
                            </td>
                        </tr>
                    ))}
                </tbody>

            </table>
        </div>
    )
}