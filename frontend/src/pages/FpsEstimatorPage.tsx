import { useState, useEffect } from 'react';
import FpsEstimate from '../components/FpsEstimate';
import type { FpsEstimateData } from '../types/fps';
import type { PartOption } from '../types/parts';
import SearchableDropdown from '../components/SearchableDropdown';
import { estimateStandaloneFps, getParts } from '../services/api';

const FpsEstimatorPage = () => {
    const [cpus, setCpus] = useState<PartOption[]>([]);
    const [gpus, setGpus] = useState<PartOption[]>([]);

    const [selectedCpu, setSelectedCpu] = useState('');
    const [selectedGpu, setSelectedGpu] = useState('');
    const [gameName, setGameName] = useState('');

    const [fpsData, setFpsData] = useState<FpsEstimateData | null>(null);
    const [loading, setLoading] = useState(false);
    const [partsLoading, setPartsLoading] = useState(true);
    const [partsError, setPartsError] = useState<string | null>(null);

    useEffect(() => {
        const fetchParts = async () => {
            try {
                const [cpuData, gpuData] = await getParts();
                setCpus(cpuData);
                setGpus(gpuData);
            } catch (error) {
                console.error('Error fetching parts:', error);
                setPartsError(error instanceof Error ? error.message : 'Failed to load components');
            } finally {
                setPartsLoading(false);
            }
        };
        fetchParts();
    }, []);

    const canEstimate = selectedCpu && selectedGpu && gameName.trim();

    const handleEstimate = async () => {
        if (!canEstimate) return;
        setLoading(true);
        setFpsData(null);
        try {
            const data = await estimateStandaloneFps(selectedCpu, selectedGpu, gameName.trim());
            setFpsData(data);
        } catch (error) {
            console.error('Error estimating FPS:', error);
            setFpsData({
                estimates: [],
                disclaimer: error instanceof Error ? error.message : 'Failed to connect to FPS estimation service.',
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center min-h-screen bg-white text-black p-6 font-sans">
            <div className="w-full max-w-3xl py-12 space-y-10 animate-fade-in">

                {/* Header */}
                <div className="text-center space-y-3">
                    <h1 className="text-4xl font-extrabold tracking-tight text-black">
                        FPS Estimator
                    </h1>
                    <p className="text-neutral-500 text-lg max-w-md mx-auto">
                        Select your components and a game to get AI-generated FPS estimates.
                    </p>
                </div>

                {/* Selection Card */}
                <div className="bg-neutral-50 border border-neutral-200 rounded-3xl p-8 space-y-6 shadow-sm">
                    {partsError && <p role="alert" className="text-sm text-red-600">{partsError}</p>}
                    {!partsLoading && (
                        <>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                                <SearchableDropdown
                                    label="CPU"
                                    options={cpus}
                                    value={selectedCpu}
                                    onChange={setSelectedCpu}
                                    placeholder="Select a CPU..."
                                />
                                <SearchableDropdown
                                    label="GPU"
                                    options={gpus}
                                    value={selectedGpu}
                                    onChange={setSelectedGpu}
                                    placeholder="Select a GPU..."
                                />
                            </div>

                            {/* Game Name Input */}
                            <div>
                                <label className="block text-xs font-bold uppercase tracking-wider text-neutral-500 mb-2">
                                    Game
                                </label>
                                <input
                                    type="text"
                                    value={gameName}
                                    onChange={e => setGameName(e.target.value)}
                                    placeholder="e.g. Cyberpunk 2077, Fortnite, Minecraft..."
                                    className="w-full px-4 py-3 bg-white border border-neutral-200 rounded-xl text-sm text-black placeholder-neutral-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black transition-all"
                                    onKeyDown={e => {
                                        if (e.key === 'Enter' && canEstimate && !loading) handleEstimate();
                                    }}
                                />
                            </div>

                            {/* Estimate Button */}
                            <div className="flex justify-center pt-2">
                                <button
                                    onClick={handleEstimate}
                                    disabled={!canEstimate || loading}
                                    className="px-8 py-3 bg-neutral-900 text-white hover:bg-neutral-700 font-semibold rounded-xl border border-neutral-700 transition-all hover:scale-105 active:scale-95 flex items-center gap-2"
                                >
                                    {loading ? "Estimating..." : "Estimate FPS"}
                                </button>
                            </div>
                        </>
                    )}
                </div>

                {/* Results */}
                {fpsData && (
                    <div className="bg-neutral-50 border border-neutral-200 rounded-3xl p-8 shadow-sm animate-fade-in">
                        <FpsEstimate data={fpsData} />
                    </div>
                )}
            </div>
        </div>
    );
};

export default FpsEstimatorPage;
