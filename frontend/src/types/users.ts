export type UserType = 'private' | 'corporate' | 'supervisor';

export interface User {
    id: number;
    email: string;
    login: string;
    fullname: string;
    user_type: UserType;
    ip_address: string | null;
    agency_id: number | null;
    position_id: number | null;
    is_active: boolean;
    is_superuser: boolean;
    created_at: string;
    updated_at: string;
}

export interface UserCreate {
    email: string;
    login: string;
    fullname: string;
    password: string;
    ip_address?: string;
    user_type?: UserType;
    agency_id?: number;
    position_id?: number;
}

export interface UserUpdate {
    email?: string;
    login?: string;
    fullname?: string;
    ip_address?: string;
    user_type?: UserType;
    agency_id?: number;
    position_id?: number;
    is_active?: boolean;
}