import { useState } from 'react';
import type { Lead, LeadAction, Favorite } from '../../types/listings'
import { IoIosLink } from "react-icons/io";
import { RxDownload } from "react-icons/rx";
import { FaRegStar, FaStar } from "react-icons/fa";
import { BiSolidPhoneCall } from "react-icons/bi";
import { downloadPhotos, postLeadAction, addToFavorites, removeFromFavorites } from '../../api/listings';
import { useQueryClient } from "@tanstack/react-query"

interface Props{
    leads: Lead[]
    newLeadIds: Set<number>
    userActions: LeadAction[]
    favorites: Favorite[]
}

export default function ListingsTable({ leads, newLeadIds, userActions, favorites }: Props) {
    const [filterState, setFilterState] = useState<'all' | 'favorites' | 'filters'>('all')
    const queryClient = useQueryClient()

    const favoriteIds = new Set(favorites.map(f => f.lead_id))
    const filteredLeads = filterState === "favorites" ? leads.filter(l => favoriteIds.has(l.id)) : leads

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

    const commonActionsStyles = "text-lg cursor-pointer text-gray-700 hover:text-[#3D3FAA] transition-colors"
    const tableActions = [
        {
            label: 'открыть ссылку', 
            element: (_lead: Lead) => <IoIosLink />, 
            fn: (lead: Lead) => {
                if (lead.external_id) {window.open(lead.external_url ?? "", '_blank', 'noopener,noreferrer')};
                postLeadAction({lead_id: lead.id, action_type: 'GO_LINK'})
            },
            currentStyle: ''
        },
        {
            label: 'скачать изображения', 
            element: (_lead: Lead) => <RxDownload />, 
            fn: (lead: Lead) => { 
                if (lead.photo_urls && lead.photo_urls.length > 0) {
                    downloadPhotos(lead.photo_urls, lead.source ?? "")
                    postLeadAction({lead_id: lead.id, action_type: "DOWNLOAD_PHOTOS"})
                }
            }, 
            currentStyle: ''
        },
        {
            label: 'добавить в избранное', 
            element: (lead: Lead) => favoriteIds.has(lead.id) ? <FaStar className='text-yellow-400' /> : <FaRegStar />, 
            fn: async (lead: Lead) => {
                if (favoriteIds.has(lead.id)) {
                    await removeFromFavorites(lead.id)
                    postLeadAction({lead_id: lead.id, action_type: 'DELETE_FAVORITE'}) 
                } else {
                    await addToFavorites(lead.id)
                    postLeadAction({lead_id: lead.id, action_type: 'ADD_FAVORITE'})
                }
                queryClient.invalidateQueries({ queryKey: ['favorites']})
            },
            currentStyle: ''
        },
        {
            label: 'позвонить собственнику', 
            element: (_lead: Lead) => <BiSolidPhoneCall />, 
            fn: (lead: Lead) => {
                alert(`Звоним ${lead.id} по номеру ${lead.phone_number}`)
                postLeadAction({lead_id: lead.id, action_type: 'CALL'})
            }, 
            currentStyle: ''
        }, 
    ]

    return(
        <div className='bg-white rounded-xl shadow-sm'>
            <div className='flex gap-2 p-4 border-b border-gray-100'>
                {filterButtons.map((btn) => (
                    <button
                        key={btn.value}
                        onClick={() => setFilterState(btn.value as 'all' | 'favorites')}
                        className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${filterState===btn.value ? 'bg-[#3D3FAA] text-white' : 'text-gray-500 hover:bg-gray-100'}`}
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
                                    <td className='px-4 py-3'>{lead.source}</td>
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