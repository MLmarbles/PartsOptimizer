import type { BuildResponse, ComponentSummary } from '../types/build';
import type { FpsEstimateData } from '../types/fps';
import type { PartOption } from '../types/parts';

async function requestJson<T>(path: string, errorMessage: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`/api/v1${path}`, options);
    if (!response.ok) {
        const data: unknown = await response.json().catch(() => null);
        const detail = data && typeof data === 'object' && 'detail' in data ? data.detail : null;
        throw new Error(typeof detail === 'string' ? detail : errorMessage);
    }
    return response.json();
}

function postJson<T>(path: string, body: unknown, errorMessage: string): Promise<T> {
    return requestJson<T>(path, errorMessage, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });
}

export function generateBuild(budget: number, useCase: string): Promise<BuildResponse> {
    return postJson('/build/generate', { budget, use_case: useCase }, 'Failed to generate build');
}

export function getParts(): Promise<[PartOption[], PartOption[]]> {
    return Promise.all([
        requestJson<PartOption[]>('/cpu/', 'Failed to load CPUs'),
        requestJson<PartOption[]>('/gpu/', 'Failed to load GPUs'),
    ]);
}

export function estimateBuildFps(components: ComponentSummary[]): Promise<FpsEstimateData> {
    return postJson('/build/estimate-fps', { components }, 'Failed to estimate FPS');
}

export function estimateStandaloneFps(cpuName: string, gpuName: string, game: string): Promise<FpsEstimateData> {
    return postJson('/build/estimate-fps-standalone', {
        cpu_name: cpuName,
        gpu_name: gpuName,
        game,
    }, 'Failed to estimate FPS');
}
