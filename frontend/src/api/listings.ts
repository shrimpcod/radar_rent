import client from "./client"
import type { Lead, LeadAction } from "../types/listings"
import axios from "axios"

export const getLeads = async (skip = 0, limit = 10): Promise<Lead[]> => {
    const response = await client.get<Lead[]>("/leads", { params: { skip, limit } })
    return response.data
}

export const getLeadsCount = async (): Promise<number> => {
    const response = await client.get<{count: number}>('/leads/count')
    return response.data.count
}

export const downloadPhotos = async (photoUrls: string[], source: string): Promise<void> => {
    const response = await axios.post(
        'http://localhost:8001/remove',
        { image_urls: photoUrls, source },
        { responseType: 'blob' }
    )
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'photos.zip')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
}

export const getLeadAction = async (leadId: number) => {
    const response = await client.get(`/lead_actions/${leadId}`)
    return response.data
}

export const patchLeadAction = async (leadId: number, params: {is_favorite?: boolean, lead_status_id?: number}) => {
    const response = await client.patch(`/lead_actions/${leadId}`, null, { params })
    return response.data
}

export const getUserLeadActions = async (): Promise<LeadAction[]> => {
    const response = await client.get<LeadAction[]>('/lead_actions')
    return response.data
}