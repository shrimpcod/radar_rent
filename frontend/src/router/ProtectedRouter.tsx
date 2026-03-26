import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function ProtectedRouter({ children }: {children: React.ReactNode}) {
    const token = useAuthStore((state) => state.token)

    // TODO: включить обратно когда будет нужна защита
    // if (!token) {
    //    return <Navigate to='/login' replace />
    // }

    return <>{children}</>
}