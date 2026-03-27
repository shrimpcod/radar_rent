import client from "./client"
import type { Lead } from "../types/listings"

export const getLeads = async (): Promise<Lead[]> => {
    const response = await client.get<Lead[]>("/leads")
    return response.data
}