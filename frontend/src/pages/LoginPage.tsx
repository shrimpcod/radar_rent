import LoginForm from "../features/auth/LoginForm"
import { FaTelegram, FaVk } from 'react-icons/fa'
import { colors } from '../utils/colors'

const socials = [
    { icon: FaTelegram, href: "https://t.me/" },
    { icon: FaVk, href: "https://vk.com/" },
]

export default function LoginPage() {
    return (
        <div
            className="h-screen w-screen bg-cover bg-center relative overflow-hidden"
            style={{ backgroundImage: 'url(/login-bg-7.png)' }}
        >
            <div
                className="absolute right-0 top-0 h-full w-[40%] bg-white flex flex-col justify-center px-16"
                style={{ borderTopLeftRadius: '180px'}}
            >
                <h1 className="text-5xl font-bold font-rubik-distressed" style={{ color: colors.loginText }}>Добро пожаловать!</h1>
                <p className="text-left text-xl font-rubik-bubbles" style={{ color: colors.loginText, marginTop: '12px' }}>Войдите в свой аккаунт Радар Рент</p>
                <div style={{ marginTop: '84px' }}>
                    <LoginForm />
                </div>


                <div className="text-center" style={{ marginTop: '115px' }}>
                    <p className="text-xs mb-3 font-rubik-bubbles" style={{ color: colors.loginText }}>Мы в соцсетях</p>
                    <div className="flex justify-center gap-5">
                        {socials.map(({ icon: Icon, href }) => (
                            <a key={href} href={href} target="_blank" rel="noopener noreferrer"
                                className="transition text-2xl" style={{ color: colors.loginText }}>
                                <Icon />
                            </a>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
