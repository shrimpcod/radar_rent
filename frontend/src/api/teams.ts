import client from "./client"
import type { Team, TeamCreate, TeamUpdate } from "../types/teams"

export async function getTeams(): Promise<Team[]> {
    const response = await client.get<Team[]>("/teams")
    return response.data
}

export async function getTeamsById(id: number): Promise<Team> {
    const response = await client.get<Team>(`/teams/${id}`)
    return response.data
}

export async function createTeam(data: TeamCreate): Promise<Team> {
    const response = await client.post<Team>("/teams", data)
    return response.data
}

export async function updateTeam(id: number, data: TeamUpdate): Promise<Team> {
    const response = await client.put<Team>(`/teams/${id}`, data)
    return response.data
}

export async function deleteTeam(id: number): Promise<void> {
    await client.delete(`/teams/${id}`)
}