import { NavLink, useNavigate } from 'react-router-dom'
import { useSidebarStore } from '../../store/sidebarStore'
import { useAuthStore } from '../../store/authStore'
import { MdApartment, MdWork, MdPeople, MdBarChart, MdLogout, MdAdminPanelSettings} from 'react-icons/md'
import { colors } from '../../utils/colors'

const navItems = [
    {icon: MdAdminPanelSettings, label: 'Админ панель', to: '/admin' },
    {icon: MdApartment, label: 'База объявлений', to: '/listings'},
    {icon: MdWork, label: 'Объекты в работе', to: '/my_objects'},
    {icon: MdPeople, label: 'База клиентов', to: '/clients'},
    {icon: MdBarChart, label: 'График', to: '/schedule'}
]

const sidebarStyle = {
    background: colors.sidebarBg
}

export default function Sidebar(){
    const { collapsed, toggle } = useSidebarStore()
    const { logout } = useAuthStore()
    const navigate = useNavigate()

    return(
        <aside
            style={sidebarStyle}
            className={`h-screen flex flex-col transition-all duration-300 ${collapsed ? 'w-16' : 'w-56'}`}
        >
            <button
                onClick = {toggle}
                className='text-left px-4 py-5 font-bold text-lg tracking-wide cursor-pointer ml-2'
                style={{ color: colors.text}}
            >
                {collapsed ? 'Р' : 'Радар Рент'}
            </button>
            <nav
                className='flex flex-col gap-1 p-2 flex-1'
            >
                {navItems.map(({ icon: Icon, label, to }) => 
                    <NavLink
                        key={to}
                        to={to}
                        className={({ isActive }) => 
                            `flex items-center gap-3 py-2.5 rounded-lg transition cursor-pointer pl-3 ${isActive ? colors.activeItemSidebar : 'hover:bg-white/10'}`
                        }
                    >
                        <Icon className="text-xl shrink-0" style={{ color: colors.text }}/>
                        {!collapsed && (
                            <span className='text-sm' style={{ color: colors.text}}>
                                {label}
                            </span>
                        )}

                    </NavLink>
                )}
            </nav>
            
            <button 
                className="flex items-center px-4 py-4 text-sm text-left hover:bg-white/10 transition border-t border-white/10 cursor-pointer"
                style={{ color: colors.text }}
                onClick={() => { logout(); navigate("/login")}}
            >
                <MdLogout className='text-xl' style={{ color: colors.text}} />
                {!collapsed && <span>Выйти</span>}
            </button>
        </aside>
    )
}