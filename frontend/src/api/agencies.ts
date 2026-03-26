import client from "./client"
import type { Agency, AgencyCreate, AgencyUpdate } from "../types/agency"


export async function getAgencies(): Promise<Agency[]> {
    const response = await client.get<Agency[]>("/agencies")
    return response.data
}

export async function getAgencyById(id: number): Promise<Agency> {
    const response = await client.get<Agency>(`/agencies/${id}`)
    return response.data
}

export async function createAgency(data: AgencyCreate): Promise<Agency> {
    const response = await client.post("/agencies", data)
    return response.data
}

export async function updateAgency(id: number, data: AgencyUpdate): Promise<Agency> {
    const response = await client.put(`/agencies/${id}`, data)
    return response.data
}

export async function deleteAgency(id: number): Promise<void> {
    await client.delete(`/agencies/${id}`)
}