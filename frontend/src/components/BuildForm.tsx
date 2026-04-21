import { useState } from 'react';

interface BuildFormProps {
    onGenerate: (budget: number, useCase: string) => void;
    isLoading: boolean;
}

const useCases = [
    { value: 'Gaming', description: 'Optimized for high FPS gaming' },
    { value: 'Video Editing', description: 'Powerful rendering & editing' },
    { value: 'Machine Learning', description: 'GPU-accelerated compute' },
];

const BuildForm = ({ onGenerate, isLoading }: BuildFormProps) => {
    const [budget, setBudget] = useState<number>(500);
    const [useCase, setUseCase] = useState<string>('Gaming');

    const handleSubmit = () => {
        onGenerate(budget, useCase);
    };

    const getBudgetLabel = () => {
        if (budget <= 500) return 'Entry Level';
        if (budget <= 1000) return 'Budget';
        if (budget <= 2000) return 'Mid Range';
        if (budget <= 3500) return 'High End';
        return 'Enthusiast';
    };

    return (
        <div className="min-h-screen bg-white text-black font-sans">
            <div className="max-w-5xl mx-auto px-6 py-16 space-y-16">

                {/* Header */}
                <div className="text-center space-y-4">
                    <h1 className="text-5xl font-extrabold tracking-tight text-black">
                        The Best Machine For Any Budget
                    </h1>
                    <p className="text-neutral-500 text-lg max-w-lg mx-auto">
                        Set your budget and use case and we'll do the rest!
                    </p>
                </div>

                {/* Budget Section */}
                <div className="space-y-6">
                    <div className="flex items-end justify-between">
                        <div>
                            <h2 className="text-xs font-bold uppercase tracking-wider text-neutral-400 mb-1">Budget</h2>
                            <div className="flex items-baseline gap-3">
                                <span className="text-5xl font-extrabold text-black tabular-nums">${budget.toLocaleString()}</span>
                                <span className="text-sm font-semibold text-neutral-400 bg-neutral-100 px-3 py-1 rounded-full">
                                    {getBudgetLabel()}
                                </span>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-3">
                        <input
                            type="range"
                            min="500"
                            max="5000"
                            step="50"
                            value={budget}
                            onChange={(e) => setBudget(parseInt(e.target.value))}
                            className="w-full h-2 bg-neutral-200 rounded-lg appearance-none cursor-pointer accent-black transition-all"
                        />
                        <div className="flex justify-between text-xs text-neutral-400 font-medium">
                            <span>$500</span>
                            <span>$1,000</span>
                            <span>$2,000</span>
                            <span>$3,000</span>
                            <span>$4,000</span>
                            <span>$5,000</span>
                        </div>
                    </div>
                </div>

                <div className="border-t border-neutral-200" />

                <div className="space-y-5">
                    <h2 className="text-xs font-bold uppercase tracking-wider text-neutral-400">Use Case</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {useCases.map((uc) => (
                            <button
                                key={uc.value}
                                onClick={() => setUseCase(uc.value)}
                                className={`text-left p-6 rounded-2xl border-2 transition-all ${useCase === uc.value
                                    ? 'border-black bg-black text-white shadow-lg scale-[1.02]'
                                    : 'border-neutral-200 bg-neutral-50 text-black hover:border-neutral-400 hover:shadow-sm'
                                    }`}
                            >
                                <span className="text-lg font-bold block mb-1">{uc.value}</span>
                                <span className={`text-sm ${useCase === uc.value ? 'text-neutral-300' : 'text-neutral-500'}`}>
                                    {uc.description}
                                </span>
                            </button>
                        ))}
                    </div>
                </div>

                <div className="border-t border-neutral-200" />

                <div className="flex justify-center">
                    <button
                        onClick={handleSubmit}
                        disabled={isLoading}
                        className="px-12 py-4 bg-black text-white hover:bg-neutral-800 text-lg font-bold rounded-2xl shadow-lg transform transition-all flex items-center gap-3"
                    >
                        {isLoading ? "Generating..." : "Generate Build"}
                    </button>
                </div>

            </div>
        </div>
    );
};

export default BuildForm;
