import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'

export default function AppLayout() {
    return(
        <div className='flex h-screen'>
            <Sidebar />
            <div className='flex flex-col flex-1 overflow-hidden'>
                <Header />
                <main className='flex-1 overflow-auto  bg-[#EEF0F8]'>
                    <Outlet />
                </main>
            </div>
        </div>
    )
}