import React, { useState } from 'react';
import FpsEstimate from './FpsEstimate';
import type { FpsEstimateData } from '../types/fps';
import ComponentCard from './ComponentCard';
import { estimateBuildFps } from '../services/api';

import type { BuildResponse } from '../types/build';
import { describeBuild, describeComponent, formatPrice } from '../utils/formatting';

interface BuildResultProps {
    build: BuildResponse;
    onReset: () => void;
}


const BuildResult: React.FC<BuildResultProps> = ({ build, onReset }) => {
    const [fpsData, setFpsData] = useState<FpsEstimateData | null>(null);
    const [fpsLoading, setFpsLoading] = useState(false);
    const [showFps, setShowFps] = useState(false);
    const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

    const handleSavePdf = async () => {
        const { saveBuildPdf } = await import('../utils/buildPdf');
        saveBuildPdf(build, fpsData);
    };

    const selectedPart = selectedIndex !== null ? build.components[selectedIndex] : null;

    const handleEstimateFps = async () => {
        if (fpsData) {
            setShowFps(!showFps);
            return;
        }

        setFpsLoading(true);
        setShowFps(true);
        try {
            const data = await estimateBuildFps(build.components);
            setFpsData(data);
        } catch (error) {
            console.error("Error estimating FPS:", error);
            setFpsData({
                estimates: [],
                disclaimer: error instanceof Error ? error.message : 'Failed to connect to FPS estimation service.',
            });
        } finally {
            setFpsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-white text-black font-sans">
            <div className="max-w-5xl mx-auto px-6 py-16 space-y-16 animate-fade-in">

                {/* Header */}
                <div className="text-center space-y-4">
                    <h1 className="text-5xl font-extrabold tracking-tight text-black">
                        Selection Complete
                    </h1>
                    <p className="text-neutral-500 text-lg">{describeBuild(build.use_case)}</p>
                </div>

                {/* Price */}
                <div className="flex justify-center gap-8">
                    <div className="text-center">
                        <p className="text-xs font-bold uppercase tracking-wider text-neutral-400 mb-1">Total Price</p>
                        <p className="text-4xl font-extrabold text-black tabular-nums">{formatPrice(build.total_price)}</p>
                    </div>
                    <div className="border-l border-neutral-200" />
                    <div className="text-center">
                        <p className="text-xs font-bold uppercase tracking-wider text-neutral-400 mb-1">Remaining</p>
                        <p className="text-4xl font-extrabold text-neutral-300 tabular-nums">{formatPrice(build.remaining_budget)}</p>
                    </div>
                </div>

                <div className="border-t border-neutral-200" />

                {/* Components */}
                <div className="space-y-5">
                    <h2 className="text-xs font-bold uppercase tracking-wider text-neutral-400">Components</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                        {build.components.map((part, index) => (
                            <ComponentCard
                                key={index}
                                part={part}
                                useCase={build.use_case}
                                isSelected={selectedIndex === index}
                                onClick={() => setSelectedIndex(selectedIndex === index ? null : index)}
                            />
                        ))}
                    </div>
                </div>

                {/* Alternative */}
                {selectedPart && (
                    <div
                        className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
                        onClick={() => setSelectedIndex(null)}
                    >
                        <div
                            className="bg-white rounded-3xl shadow-2xl w-full max-w-lg max-h-[85vh] overflow-y-auto p-8 space-y-6"
                            onClick={e => e.stopPropagation()}
                        >
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-xs font-bold uppercase tracking-wider text-neutral-400">{selectedPart.alternatives ? 'Alternatives for' : 'Details'}</p>
                                    <p className="text-lg font-bold text-black mt-1">{selectedPart.type}</p>
                                </div>
                                <button
                                    onClick={() => setSelectedIndex(null)}
                                    className="w-8 h-8 flex items-center justify-center rounded-lg bg-neutral-200 hover:bg-neutral-300 transition-colors"
                                >
                                    ✕
                                </button>
                            </div>

                            {/* Currently selected */}
                            <div className="bg-black text-white rounded-2xl p-6">
                                <p className="text-xs font-bold uppercase tracking-wider text-neutral-400 mb-2">Current Selection</p>
                                <p className="text-base font-bold leading-snug">{selectedPart.name}</p>
                                <div className="flex justify-between items-end mt-3">
                                    <p className="text-sm text-neutral-300">{describeComponent(selectedPart.type, selectedPart.specs, build.use_case)}</p>
                                    <p className="text-lg font-bold ml-3">{formatPrice(selectedPart.price)}</p>
                                </div>
                                {selectedPart.tier && (
                                    <div className="mt-3 pt-3 border-t border-neutral-700">
                                        <span className="text-xs font-bold uppercase tracking-wider text-neutral-400">Tier {selectedPart.tier}</span>
                                    </div>
                                )}
                            </div>

                            {/* Alternative cards */}
                            {selectedPart.alternatives && selectedPart.alternatives.length > 0 ? (
                                <div className="space-y-4">
                                    <p className="text-xs font-bold uppercase tracking-wider text-neutral-400">Other Options</p>
                                    {selectedPart.alternatives.map((alt, i) => {
                                        const priceDiff = alt.price - selectedPart.price;
                                        return (
                                            <div key={i} className="bg-white border-2 border-neutral-200 rounded-2xl p-5 hover:border-black hover:shadow-md transition-all cursor-pointer">
                                                <div className="flex items-center gap-2 mb-2">
                                                    <span className="text-xs font-bold uppercase tracking-wider text-neutral-400">{alt.brand}</span>
                                                    {priceDiff !== 0 && (
                                                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${priceDiff < 0 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-500'}`}>
                                                            {priceDiff > 0 ? '+' : '-'}{formatPrice(Math.abs(priceDiff))}
                                                        </span>
                                                    )}
                                                </div>
                                                <p className="text-base font-bold text-black leading-snug">{alt.name}</p>
                                                <div className="flex justify-between items-end mt-2">
                                                    <p className="text-sm text-neutral-500">{describeComponent(selectedPart.type, alt.specs, build.use_case, true)}</p>
                                                    <p className="text-lg font-bold text-black ml-3">{formatPrice(alt.price)}</p>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            ) : (
                                <p className="text-sm text-neutral-400 text-center py-4">No alternatives available for this component.</p>
                            )}
                        </div>
                    </div>
                )}

                <p className="text-[11px] text-neutral-400 mt-2">
                    *Prices are based from Summer 2025 and may vary.
                </p>

                <div className="border-t border-neutral-200" />

                {/* FPS Estimate Section */}
                <div className="space-y-8">
                    <div className="flex justify-center">
                        <button
                            onClick={handleEstimateFps}
                            disabled={fpsLoading}
                            className="px-10 py-4 bg-neutral-900 text-white hover:bg-neutral-700 text-lg font-semibold rounded-2xl border border-neutral-700 transition-all hover:scale-105 active:scale-95 flex items-center gap-3"
                        >
                            {fpsLoading ? (
                                "Estimating..."
                            ) : showFps && fpsData ? (
                                "Hide FPS Estimates"
                            ) : (
                                "Estimate FPS"
                            )}
                        </button>
                    </div>

                    {showFps && fpsData && <FpsEstimate data={fpsData} />}
                </div>

                <div className="border-t border-neutral-200" />

                <div className="flex justify-center gap-4">
                    <button
                        onClick={onReset}
                        className="px-10 py-4 bg-white hover:bg-neutral-50 text-black text-lg font-semibold rounded-2xl border border-neutral-300 transition-all hover:scale-105 active:scale-95"
                    >
                        Build Another
                    </button>
                    <button
                        onClick={handleSavePdf}
                        className="px-10 py-4 bg-black text-white hover:bg-neutral-800 text-lg font-bold rounded-2xl shadow-lg transition-all hover:scale-105 active:scale-95 flex items-center gap-3"
                    >
                        Save Build
                    </button>
                </div>

            </div>
        </div>
    );
};

export default BuildResult;
