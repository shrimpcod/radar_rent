export interface User {
    id: number
    email: string
    login: string
    fullname: string
    user_type: string
    ip_address: string
    is_active: boolean
    is_superuser: boolean
    agency_id: number
    position_id: number
    created_at: string
}

export interface LoginRequest {
    email_or_login: string
    password: string
}

export interface LoginResponse {
    access_token: string
    token_type: string
    user: User
}