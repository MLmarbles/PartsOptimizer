export interface ComponentSpecs {
    vram_gb?: number | null;
    benchmark_score?: number | null;
    cores?: number | null;
    single_core_score?: number | null;
    multi_core_score?: number | null;
    capacity_gb?: number | null;
    type?: string | null;
    speed_mhz?: number | null;
    socket?: string | null;
    form_factor?: string | null;
    interface?: string | null;
    wattage?: number | null;
    efficiency_rating?: string | null;
}

export interface AlternativeSummary {
    brand: string;
    name: string;
    price: number;
    specs: ComponentSpecs;
}

export interface ComponentSummary {
    type: string;
    name: string;
    price: number;
    specs: ComponentSpecs;
    tier?: string | null;
    alternatives?: AlternativeSummary[] | null;
}

export interface BuildResponse {
    components: ComponentSummary[];
    total_price: number;
    remaining_budget: number;
    use_case: string;
}
