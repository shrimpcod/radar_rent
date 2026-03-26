export type TeamPosition = 'head' | 'member'

export interface TeamMember {
    id: number;
    team_id: number;
    user_id: number;
    team_position: TeamPosition
}

export interface TeamMemberCreate {
    team_id: number;
    user_id: number;
    team_position: TeamPosition;
}

export interface TeamMemberUpdate {
    team_position?: TeamPosition;
}