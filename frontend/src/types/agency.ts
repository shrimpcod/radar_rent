export interface Agency {
    id: number;
    name: string;
}

export interface AgencyCreate {
    name: string
}

export interface AgencyUpdate {
    name?: string
}