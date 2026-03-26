import client from "./client"
import type { Position, PositionCreate } from "../types/positions"

export async function getPositions(): Promise<Position[]> {
    const response = await client.get<Position[]>("/positions")
    return response.data
}

export async function getPositionById(id: number): Promise<Position> {
    const response = await client.get<Position>(`/positions/${id}`)
    return response.data
}

export async function createPosition(data: PositionCreate): Promise<Position> {
    const response = await client.post<Position>("/positions", data)
    return response.data
}

export async function deletePosition(id: number): Promise<void> {
    await client.delete(`/positions/${id}`)
}
