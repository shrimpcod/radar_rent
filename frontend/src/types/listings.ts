export interface Lead {
    id: number;                                                                                                                                    
    external_id: string;
    external_url: string | null;
    price: number;
    rooms_count: number;
    area: number;
    floor: number;
    floors_count: number;
    city: string;
    metro_station: string | null;
    address: string;
    phone_number: string | null;
    is_early_access: boolean;
    phone_reveal_at: string | null;
    published_offer_at: string | null;
    created_offer_at: string | null;
    source: string | null;
    photo_urls: string[] | null;
}

export interface LeadStats{
    total_calls: number;
    closed: number;
    no_answer: number;
    not_closed: number;
}

export interface LeadAction {
    id: number
    user_id: number
    lead_id: number
    is_favorite: boolean
    lead_status_id: number | null
    call_id: number | null
    last_action_time: string
}