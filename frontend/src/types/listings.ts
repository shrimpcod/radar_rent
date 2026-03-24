export interface Lead{
    id: number;
    created_offer_at: string;
    object_info: string;
    source: string;
    price: number;
    address: string;
    phone_number: string;
    status?: string;
}

export interface LeadStats{
    total_calls: number;
    closed: number;
    no_answer: number;
    not_closed: number;
}