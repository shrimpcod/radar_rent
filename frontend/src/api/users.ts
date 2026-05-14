import client from "./client"
import type { User, UserCreate, UserUpdate } from "../types/users"

export async function getUsers(): Promise<User[]> {
    const response = await client.get<User[]>("/users")
    return response.data
}

export async function getUserById(id: number): Promise<User> {
    const response = await client.get<User>(`/users/${id}`)
    return response.data
}

export async function createUser(data: UserCreate): Promise<User> {
    const response = await client.post<User>("/users", data)
    return response.data
}

export async function updateUser(id: number, data: UserUpdate): Promise<User> {
    const response = await client.put<User>(`/users/${id}`, data)
    return response.data
}

export async function deleteUser(id: number): Promise<void> {
    await client.delete(`/users/${id}`)
}
