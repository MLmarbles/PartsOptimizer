import type { FC } from 'react';
import type { ComponentSummary } from '../types/build';
import { describeComponent, formatPrice } from '../utils/formatting';

const tierColors: Record<string, string> = {
    A: 'bg-black/5 text-black border-black/20',
    B: 'bg-neutral-100 text-neutral-600 border-neutral-300',
    C: 'bg-neutral-100 text-neutral-400 border-neutral-200',
};

interface ComponentCardProps {
    part: ComponentSummary;
    useCase: string;
    isSelected: boolean;
    onClick: () => void;
}

const ComponentCard: FC<ComponentCardProps> = ({ part, useCase, isSelected, onClick }) => {
    const hasAlts = part.alternatives && part.alternatives.length > 0;

    return (
        <div
            onClick={onClick}
            className={`relative bg-white border-2 rounded-2xl p-6 transition-all cursor-pointer ${isSelected
                ? 'border-black shadow-lg scale-[1.02]'
                : 'border-neutral-200 hover:border-neutral-400 hover:shadow-md'
                }`}
        >
            <div className="flex justify-between items-start mb-3">
                <div className="flex items-center gap-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-neutral-400">{part.type}</span>
                    {part.tier && (
                        <span className={`text-[10px] font-bold uppercase px-1.5 py-0.5 rounded border ${tierColors[part.tier] || 'bg-neutral-100 text-neutral-400 border-neutral-200'}`}>
                            Tier {part.tier}
                        </span>
                    )}
                </div>
                <span className="text-sm font-bold text-black">{formatPrice(part.price)}</span>
            </div>
            <h3 className="text-lg font-bold text-black mb-2 line-clamp-2">{part.name}</h3>
            <p className="text-xs text-neutral-500 leading-relaxed">{describeComponent(part.type, part.specs, useCase)}</p>

            {hasAlts && (
                <div className={`mt-3 flex items-center gap-1.5 text-[11px] font-medium transition-colors ${isSelected ? 'text-black' : 'text-neutral-400'
                    }`}>
                    {isSelected ? 'Viewing alternatives' : 'Click for alternatives'}
                </div>
            )}
        </div>
    );
};

export default ComponentCard;
