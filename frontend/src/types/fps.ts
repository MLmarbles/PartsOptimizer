export interface FpsRange {
    min: number;
    max: number;
}

export interface ResolutionFps {
    resolution: string;
    low: FpsRange;
    medium: FpsRange;
    high: FpsRange;
    ultra: FpsRange;
}

export interface GameFpsEstimate {
    game: string;
    resolutions: ResolutionFps[];
}

export interface FpsEstimateData {
    estimates: GameFpsEstimate[];
    disclaimer: string;
}
