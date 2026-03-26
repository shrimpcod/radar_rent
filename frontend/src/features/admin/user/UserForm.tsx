import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getAgencies } from '../../../api/agencies'
import { getPositions } from '../../../api/positions'
import type { UserCreate, UserUpdate, UserType } from '../../../types/users'

interface CreateProps {
    mode: 'create'
    onSubmit: (data: UserCreate) => void
    onClose: () => void
    isPending?: boolean
}

interface EditProps {
    mode: 'edit'
    defaultValue: UserUpdate & { fullname: string }
    onSubmit: (data: UserUpdate) => void
    onClose: () => void
    isPending?: boolean
}

type Props = CreateProps | EditProps

const userTypeOptions: { value: UserType; label: string }[] = [
    { value: 'private', label: 'Частный' },
    { value: 'corporate', label: 'Корпоративный' },
    { value: 'supervisor', label: 'Руководитель' },
]

const inputClass = "w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 outline-none focus:border-[#3D3FAA]"
const labelClass = "block text-sm text-gray-600 mb-1"

export default function UserForm(props: Props) {
    const { onClose, isPending } = props

    const defaultValue = props.mode === 'edit' ? props.defaultValue : undefined

    const [form, setForm] = useState({
        email: defaultValue?.email ?? '',
        login: defaultValue?.login ?? '',
        fullname: defaultValue?.fullname ?? '',
        password: '',
        user_type: defaultValue?.user_type ?? 'private' as UserType,
        agency_id: defaultValue?.agency_id ?? undefined as number | undefined,
        position_id: defaultValue?.position_id ?? undefined as number | undefined,
        ip_address: defaultValue?.ip_address ?? '',
        is_active: defaultValue?.is_active ?? true,
    })

    const { data: agencies } = useQuery({ queryKey: ['agencies'], queryFn: getAgencies })
    const { data: positions } = useQuery({ queryKey: ['positions'], queryFn: getPositions })

    const set = (field: string, value: string | number | boolean | undefined) =>
        setForm(prev => ({ ...prev, [field]: value }))

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (props.mode === 'create') {
            props.onSubmit({
                email: form.email,
                login: form.login,
                fullname: form.fullname,
                password: form.password,
                user_type: form.user_type,
                agency_id: form.agency_id,
                position_id: form.position_id,
                ip_address: form.ip_address || undefined,
            })
        } else {
            props.onSubmit({
                email: form.email,
                login: form.login,
                fullname: form.fullname,
                user_type: form.user_type,
                agency_id: form.agency_id,
                position_id: form.position_id,
                ip_address: form.ip_address || undefined,
                is_active: form.is_active,
            })
        }
    }

    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
            <div>
                <label className={labelClass}>Email</label>
                <input type="email" value={form.email} onChange={e => set('email', e.target.value)}
                    className={inputClass} placeholder="example@mail.com" required />
            </div>
            <div>
                <label className={labelClass}>Логин</label>
                <input type="text" value={form.login} onChange={e => set('login', e.target.value)}
                    className={inputClass} placeholder="Введите логин" required />
            </div>
            <div>
                <label className={labelClass}>Полное имя</label>
                <input type="text" value={form.fullname} onChange={e => set('fullname', e.target.value)}
                    className={inputClass} placeholder="Иванов Иван Иванович" required />
            </div>

            {props.mode === 'create' && (
                <div>
                    <label className={labelClass}>Пароль</label>
                    <input type="password" value={form.password} onChange={e => set('password', e.target.value)}
                        className={inputClass} placeholder="Минимум 6 символов" required />
                </div>
            )}

            <div>
                <label className={labelClass}>Тип пользователя</label>
                <select value={form.user_type} onChange={e => set('user_type', e.target.value)}
                    className={inputClass}>
                    {userTypeOptions.map(opt => (
                        <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                </select>
            </div>
            <div>
                <label className={labelClass}>Агентство</label>
                <select
                    value={form.agency_id ?? ''}
                    onChange={e => set('agency_id', e.target.value ? Number(e.target.value) : undefined)}
                    className={inputClass}
                >
                    <option value="">— Не выбрано —</option>
                    {agencies?.map(a => (
                        <option key={a.id} value={a.id}>{a.name}</option>
                    ))}
                </select>
            </div>
            <div>
                <label className={labelClass}>Должность</label>
                <select
                    value={form.position_id ?? ''}
                    onChange={e => set('position_id', e.target.value ? Number(e.target.value) : undefined)}
                    className={inputClass}
                >
                    <option value="">— Не выбрано —</option>
                    {positions?.map(p => (
                        <option key={p.id} value={p.id}>{p.name}</option>
                    ))}
                </select>
            </div>
            <div>
                <label className={labelClass}>IP адрес</label>
                <input type="text" value={form.ip_address} onChange={e => set('ip_address', e.target.value)}
                    className={inputClass} placeholder="192.168.0.1" />
            </div>

            {props.mode === 'edit' && (
                <div className="flex items-center gap-2">
                    <input type="checkbox" id="is_active" checked={form.is_active}
                        onChange={e => set('is_active', e.target.checked)} className="cursor-pointer" />
                    <label htmlFor="is_active" className="text-sm text-gray-600 cursor-pointer">Активен</label>
                </div>
            )}

            <div className="flex justify-end gap-2 mt-1">
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
