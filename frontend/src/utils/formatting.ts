import type { ComponentSpecs } from '../types/build';

export function describeComponent(
    type: string,
    specs: ComponentSpecs,
    useCase: string,
    isAlternative = false,
): string {
    const value = (spec: string | number | null | undefined) => spec ?? 'N/A';
    switch (type) {
        case 'GPU':
            return `VRAM: ${value(specs.vram_gb)}GB, Score: ${value(specs.benchmark_score)}`;
        case 'CPU': {
            const score = useCase === 'Video Editing' ? specs.multi_core_score : specs.single_core_score;
            return `Cores: ${value(specs.cores)}, Score: ${value(score)}`;
        }
        case 'RAM':
            return `${value(specs.capacity_gb)}GB ${value(specs.type)}-${value(specs.speed_mhz)}`;
        case 'Motherboard':
            return `Socket: ${value(specs.socket)}, Form: ${value(specs.form_factor)}`;
        case 'Storage':
            return `${value(specs.capacity_gb)}GB ${value(specs.type)} (${value(specs.interface)})`;
        case 'PSU':
            return isAlternative
                ? `${value(specs.wattage)}W, ${value(specs.efficiency_rating)}`
                : `Wattage: ${value(specs.wattage)}W`;
        default:
            return '';
    }
}

export function describeBuild(useCase: string): string {
    return `Optimized for ${useCase}`;
}

export function formatPrice(price: number): string {
    return `$${price.toFixed(2)}`;
}
