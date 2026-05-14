import { useState } from 'react'
import AgenciesTab from '../features/admin/agency/AgenciesTab'
import TeamsTab from '../features/admin/team/TeamsTab'
import PositionTab from '../features/admin/position/PositionsTab'
import UsersTab from '../features/admin/user/UsersTab'

const tabs = ['Агентства', 'Команды', 'Должности', 'Пользователи']

export default function AdminPage() {
    const [activeTab, setActiveTab] = useState(0)

    return(
        <div className='p-6'>
            <h1 className='text-2xl font-bold mb-6' style={{ color: '#3D3FAA'}}>
                Панель администратора
            </h1>

            <div className='flex gap-2 mb-6'>
                {tabs.map((tab, i) => (
                    <button
                        key={tab}
                        onClick={() => setActiveTab(i)}
                        className='px-4 py-2 rounded-lg text-sm font-medium transition cursor-pointer'
                        style={{
                            background: activeTab === i ? '#3D3FAA' : 'white',
                            color: activeTab === i ? '#DFE2FA' : '#3D3FAA',
                            border: '1px solid #3D3FAA'
                        }}
                    >
                        {tab}
                    </button>
                ))}
            </div>

            <div>
                {activeTab === 0 && <AgenciesTab />}
                {activeTab === 1 && <TeamsTab />}
                {activeTab === 2 && <PositionTab />}
                {activeTab === 3 && <UsersTab />}
            </div>
        </div>
    )
}