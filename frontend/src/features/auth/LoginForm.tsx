import { useForm } from 'react-hook-form'
import { useAuthStore } from '../../store/authStore'
import { useNavigate } from 'react-router-dom'
import { login } from '../../api/auth'
import type { LoginRequest } from '../../types/auth'
import { colors } from '../../utils/colors'

export default function LoginForm() {
    const setAuth = useAuthStore((state) => state.setAuth)
    const { register, handleSubmit } = useForm<LoginRequest>()
    const navigate = useNavigate()

    const onSubmit = async (data: LoginRequest) => {
        const response = await login(data)
        setAuth(response.access_token, response.user)
        navigate('/listings')
    }

    const c = colors.loginText

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 w-full">
            <div className="flex flex-col gap-1">
                <label className="text-xs uppercase tracking-widest font-rubik-bubbles" style={{ color: c }}>
                    Email или логин
                </label>
                <input
                    {...register('email_or_login')}
                    className="w-full bg-white rounded-lg px-4 py-3 outline-none transition"
                    style={{ color: c, border: `1px solid ${c}` }}
                />
            </div>
            <div className="flex flex-col gap-1">
                <label className="text-xs uppercase tracking-widest font-rubik-bubbles" style={{ color: c }}>
                    Пароль
                </label>
                <input
                    {...register('password')}
                    type="password"
                    className="w-full bg-white rounded-lg px-4 py-3 outline-none transition"
                    style={{ color: c, border: `1px solid ${c}` }}
                />
            </div>
            <button
                type="submit"
                className="w-full text-white font-semibold rounded-lg py-3 mt-2 hover:opacity-90 transition cursor-pointer font-rubik-bubbles"
                style={{ backgroundColor: c }}
            >
                Войти
            </button>
        </form>
    )
}
