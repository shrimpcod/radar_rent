import client from "./client"
import type { Lead } from "../types/listings"

export const getLeads = async (skip = 0, limit = 10): Promise<Lead[]> => {
    const response = await client.get<Lead[]>("/leads", { params: { skip, limit } })
    return response.data
}

export const getLeadsCount = async (): Promise<number> => {
    const response = await client.get<{count: number}>('/leads/count')
    return response.data.count
}