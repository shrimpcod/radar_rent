import { useAuthStore } from "../store/authStore"

const userTypeLabel: Record<string, string> = {
    private: 'Частный специалист',
    corporate: 'Корпоративный сотрудник',
    supervisor: 'Руководитель'
}

export default function ProfilePage() {
    const user = useAuthStore((state) => state.user)

    if (!user) return null

    const avatar = user.fullname.charAt(0).toUpperCase()

    const info = [
        {label: 'Почта', value: user.email},
        {label: 'Логин', value: user.login},
        {label: 'Должность', value: user.position_id ? `#${user.position_id}` : 'нет данных'},
        {label: 'Ip-адреса', value: user.ip_address ?? 'нет данных'},
        {label: 'В системе с', value: new Date(user.created_at).toLocaleDateString('ru-RU')},
        {label: 'Статус', value: user.is_active ? 'Активен' : 'Заблокирован' }, 
    ]

    return(
        <div className="p-6 max-w-2xl" style={{ backgroundColor: '#EEF0F8', minHeight: '100%'}}>
            <div className="bg-white rounded-xl shadow-sm p-6 flex items-center gap-6 mb-4"> 
                <div
                    className="w-20 h-20 rounded-full flex items-center justify-center text-3xl font-bold text-white flex-shrink-0"
                    style={{ background: 'linear-gradient(180deg, #232589B3 6%, #0A112A 100%)'}}
                >
                    {avatar}
                </div>
                <div>
                    <h1 className="text-xl font-semibold text-gray-800">{user.fullname}</h1>
                    <p className="text-sm text-gray-500 mt-1">{userTypeLabel[user.user_type] ?? user.user_type}</p>
                    <p className="text-sm text-gray-400">Агентство #{user.agency_id ?? '—'}</p>
                </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
                <h2 className="text-sm font-semibold text-gray-400 uppercase mb-4">Основная информация</h2>
                <div className="divide-y divide-gray-100">
                    {info.map((row) => (
                        <div key={row.label} className="flex justify-between py-3 text-sm">
                            <span className="text-gray-400">{row.label}</span>
                            <span className="text-gray-800 font-medium">{row.value}</span>
                        </div>   
                    ))}
                </div>
            </div>
        </div>
    )
}