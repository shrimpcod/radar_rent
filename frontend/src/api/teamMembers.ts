import client from "./client"
import type { TeamMember,  TeamMemberCreate, TeamMemberUpdate } from "../types/teamMembers"

export async function getTeamMembers(teamId: number): Promise<TeamMember[]> {
    const response = await client.get<TeamMember[]>("/team_members", { params: { team_id: teamId } })
    return response.data
}

export async function getTeamMemberById(id: number): Promise<TeamMember> {
    const response = await client.get<TeamMember>(`/team_members/${id}`)
    return response.data
}

export async function createTeamMember(data: TeamMemberCreate): Promise<TeamMember> {
    const response = await client.post<TeamMember>("/team_members", data)
    return response.data
}

export async function updateTeamMember(id: number, data: TeamMemberUpdate): Promise<TeamMember> {
    const response = await client.put<TeamMember>(`/team_members/${id}`, data)
    return response.data
}

export async function deleteTeamMember(id: number): Promise<void> {
    await client.delete(`/team_members/${id}`)
}