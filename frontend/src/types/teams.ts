export interface Team {
    id: number;
    name: string;
    agency_id: number;
}

export interface TeamCreate {
    name: string;
    agency_id: number;
}

export interface TeamUpdate {
    name?: string
}