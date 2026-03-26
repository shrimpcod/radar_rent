import { useAuthStore } from "../../store/authStore"
import { colors } from "../../utils/colors"
import { NavLink } from "react-router-dom"

export default function Header() {
    const user = useAuthStore((state) => state.user)

    return(
        <header
            style={{ background: colors.headerBg}}
            className="h-17 flex items-center justify-end px-6"
        >
            <div className="flex items-center gap3">
                <NavLink
                    key={'/profile'}
                    to={'/profile'}
                >
                    <div
                      className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold border border-white/10 mr-3"
                      style={{ backgroundColor: colors.activeItemSidebar, color: colors.text }}
                    >
                      {user?.fullname?.[0] ?? '?'}
                    </div>
                </NavLink>
                <div className="text-right">
                    <p className="text-sm font-medium" style={{color: colors.text}}>
                        {user?.fullname ?? 'Неизвестный пользователь'}
                    </p>
                    <p className="text-xs opacity-50" style={{color: colors.text}}>
                        {user?.agency_id ? `Агентство #${user.agency_id}` : 'нет данных'}
                    </p>
                </div>
                
            </div>
        </header>
    )
} 