import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getAgencies } from '../../../api/agencies'
import type { TeamCreate, TeamUpdate } from '../../../types/teams'

interface CreateProps {
    mode: 'create'
    onSubmit: (data: TeamCreate) => void
    onClose: () => void
    isPending?: boolean
}

interface EditProps {
    mode: 'edit'
    defaultValue: { name: string; agency_id: number }
    onSubmit: (data: TeamUpdate) => void
    onClose: () => void
    isPending?: boolean
}

type Props = CreateProps | EditProps

const inputClass = "w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 outline-none focus:border-[#3D3FAA]"
const labelClass = "block text-sm text-gray-600 mb-1"

export default function TeamForm(props: Props) {
    const { onClose, isPending } = props

    const defaultValue = props.mode === 'edit' ? props.defaultValue : undefined

    const [name, setName] = useState(defaultValue?.name ?? '')
    const [agencyId, setAgencyId] = useState<number | undefined>(defaultValue?.agency_id)

    const { data: agencies } = useQuery({ queryKey: ['agencies'], queryFn: getAgencies })

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (props.mode === 'create') {
            props.onSubmit({ name, agency_id: agencyId! })
        } else {
            props.onSubmit({ name })
        }
    }

    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div>
                <label className={labelClass}>Название</label>
                <input
                    type="text"
                    value={name}
                    onChange={e => setName(e.target.value)}
                    className={inputClass}
                    placeholder="Введите название команды"
                    required
                />
            </div>
            {props.mode === 'create' && (
                <div>
                    <label className={labelClass}>Агентство</label>
                    <select
                        value={agencyId ?? ''}
                        onChange={e => setAgencyId(e.target.value ? Number(e.target.value) : undefined)}
                        className={inputClass}
                        required
                    >
                        <option value="">— Выберите агентство —</option>
                        {agencies?.map(a => (
                            <option key={a.id} value={a.id}>{a.name}</option>
                        ))}
                    </select>
                </div>
            )}
            <div className="flex justify-end gap-2">
                <button type="button" onClick={onClose}
                    className="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 cursor-pointer">
                    Отмена
                </button>
                <button type="submit" disabled={isPending}
                    className="px-4 py-2 text-sm bg-[#3D3FAA] text-white rounded-lg cursor-pointer disabled:opacity-50">
                    {isPending ? 'Сохранение...' : 'Сохранить'}
                </button>
            </div>
        </form>
    )
}
