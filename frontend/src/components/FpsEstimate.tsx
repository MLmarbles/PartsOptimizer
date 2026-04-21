import React, { useState } from 'react';

import type { FpsEstimateData, FpsRange } from '../types/fps';

interface FpsEstimateProps {
    data: FpsEstimateData;
}

const FpsCell: React.FC<{ range: FpsRange }> = ({ range }) => (
    <td className="px-4 py-3 text-center text-sm text-neutral-700 font-semibold">
        {range.min}–{range.max}
    </td>
);

const FpsEstimate: React.FC<FpsEstimateProps> = ({ data }) => {
    const [selectedRes, setSelectedRes] = useState('1080p');

    if (data.estimates.length === 0) {
        return (
            <div className="text-center py-6 text-neutral-500">
                <p>{data.disclaimer}</p>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex justify-center gap-2">
                {['1080p', '1440p', '4K'].map((res) => (
                    <button
                        key={res}
                        onClick={() => setSelectedRes(res)}
                        className={`px-5 py-2 rounded-lg text-sm font-semibold transition-all ${selectedRes === res
                            ? 'bg-black text-white'
                            : 'bg-neutral-100 text-neutral-500 hover:bg-neutral-200'
                            }`}
                    >
                        {res}
                    </button>
                ))}
            </div>

            <div className="overflow-x-auto rounded-xl border border-neutral-200">
                <table className="w-full text-left">
                    <thead>
                        <tr className="bg-neutral-100 border-b border-neutral-200">
                            <th className="px-4 py-3 text-xs font-bold uppercase tracking-wider text-neutral-500">Game</th>
                            <th className="px-4 py-3 text-xs font-bold uppercase tracking-wider text-neutral-500 text-center">Low</th>
                            <th className="px-4 py-3 text-xs font-bold uppercase tracking-wider text-neutral-500 text-center">Medium</th>
                            <th className="px-4 py-3 text-xs font-bold uppercase tracking-wider text-neutral-500 text-center">High</th>
                            <th className="px-4 py-3 text-xs font-bold uppercase tracking-wider text-neutral-500 text-center">Ultra</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.estimates.map((game, i) => {
                            const resFps = game.resolutions.find(r => r.resolution === selectedRes);
                            if (!resFps) return null;
                            return (
                                <tr key={i} className="border-b border-neutral-100 hover:bg-neutral-50 transition-colors">
                                    <td className="px-4 py-3 text-sm font-semibold text-black">{game.game}</td>
                                    <FpsCell range={resFps.low} />
                                    <FpsCell range={resFps.medium} />
                                    <FpsCell range={resFps.high} />
                                    <FpsCell range={resFps.ultra} />
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>

            <p className="text-[11px] text-neutral-400 text-center italic leading-relaxed">
                {data.disclaimer}
            </p>
        </div>
    );
};

export default FpsEstimate;
