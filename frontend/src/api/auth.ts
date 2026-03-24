import client from "./client"
import type { LoginRequest, LoginResponse } from "../types/auth" 

export async function login(data: LoginRequest): Promise<LoginResponse> {
    const response = await client.post<LoginResponse>('/auth/login', data)
    return response.data
}

export async function logout() {
    
}