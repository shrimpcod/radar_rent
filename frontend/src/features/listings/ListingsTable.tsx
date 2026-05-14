import { useState } from 'react';
import type { Lead, LeadAction } from '../../types/listings'
import { IoIosLink } from "react-icons/io";
import { RxDownload } from "react-icons/rx";
import { FaRegStar, FaStar } from "react-icons/fa";
import { BiSolidPhoneCall } from "react-icons/bi";
import { downloadPhotos, patchLeadAction } from '../../api/listings';
import { useQueryClient } from "@tanstack/react-query"

interface Props{
    leads: Lead[]
    newLeadIds: Set<number>
    userActions: LeadAction[]
}

export default function ListingsTable({ leads, newLeadIds, userActions }: Props) {
    const [favorites, setFavorites] = useState<'all' | 'favorites' | 'filters'>('all')
    const favoriteIds = new Set(userActions.filter(a => a.is_favorite).map(a => a.lead_id))
    const filteredLeads = favorites === "favorites" ? leads.filter(l => favoriteIds.has(l.id)) : leads
    const queryClient = useQueryClient()

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

    const commonActionsStyles = "text-lg cursor-pointer text-gray-700"
    const tableActions = [
        {
            label: 'открыть ссылку', 
            element: (_lead: Lead) => <IoIosLink />, 
            fn: (lead: Lead) => lead.external_url && window.open(lead.external_url, '_blank', 'noopener,noreferrer'), 
            currentStyle: ''
        },
        {
            label: 'скачать изображения', 
            element: (_lead: Lead) => <RxDownload />, 
            fn: (lead: Lead) => { 
                if (lead.photo_urls && lead.photo_urls.length > 0) {
                    downloadPhotos(lead.photo_urls, lead.source ?? 'cian')
                }
            }, 
            currentStyle: ''
        },
        {
            label: 'добавить в избранное', 
            element: (lead: Lead) => favoriteIds.has(lead.id) ? <FaStar className='text-yellow-400' /> : <FaRegStar />, 
            fn: (lead: Lead) => patchLeadAction(lead.id, {is_favorite: !favoriteIds.has(lead.id)}).then(() => queryClient.invalidateQueries({ queryKey: ["lead-actions"]})), 
            currentStyle: ''
        },
        {
            label: 'позвонить собственнику', 
            element: (_lead: Lead) => <BiSolidPhoneCall />, 
            fn: (lead: Lead) => alert(`Звоним ${lead.id} по номеру ${lead.phone_number}`), 
            currentStyle: ''
        }, 
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
                    {filteredLeads.length === 0 ? (
                        <tr>                                                                                                                                       
                            <td colSpan={8} className="px-4 py-8 text-center text-sm text-gray-400">
                                Нет данных
                            </td>
                        </tr>
                    ) : (
                        filteredLeads.map((lead) => (
                            <tr 
                                key={lead.id} 
                                className={`border-t border-gray-100 text-sm text-gray-700 transition-colors duration-300 ${newLeadIds.has(lead.id) ? 'bg-green-100' : 'hover:bg-gray-50'}`}>
                                    <td className='px-4 py-3'>{lead.created_offer_at ? new Date(lead.created_offer_at).toLocaleString('ru-RU') : '-'}</td>
                                    <td className='px-4 py-3'>{lead.rooms_count === 0 ? 'Ст.' : `${lead.rooms_count}-к`} , {lead.area} м², {lead.floor}/{lead.floors_count} эт.</td>
                                    <td className='px-4 py-3'>ЦИАН</td>
                                    <td className='px-4 py-3'>{lead.price.toLocaleString('ru-RU')}</td>
                                    <td className='px-4 py-3'>{lead.address}</td>
                                    <td className='px-4 py-3'>{lead.phone_number}</td>
                                    <td className='px-4 py-3'>Статус</td>
                                    <td className='flex gap-3 px-4 py-3'>
                                        {tableActions.map((ta, index) => (
                                            <button
                                                key={index}
                                                title={ta.label}
                                                onClick={() => ta.fn(lead)}
                                                className={`${ta.currentStyle} ${commonActionsStyles}`}
                                            >
                                                {ta.element(lead)}
                                            </button>
                                        ))}
                                    </td>
                            </tr>
                        ))
                    )}
                </tbody>

            </table>
        </div>
    )
}