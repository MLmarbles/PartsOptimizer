import { useState } from 'react';
import BuildForm from '../components/BuildForm';
import BuildResult from '../components/BuildResult';
import { generateBuild } from '../services/api';

import type { BuildResponse } from '../types/build';

const BuildPage = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [buildResult, setBuildResult] = useState<BuildResponse | null>(null);

    const handleGenerateBuild = async (budget: number, useCase: string) => {
        setIsLoading(true);
        setError(null);
        try {
            const data = await generateBuild(budget, useCase);
            setBuildResult(data);
        } catch (error) {
            console.error("Error generating build:", error);
            setError(error instanceof Error ? error.message : 'Failed to generate build');
        } finally {
            setIsLoading(false);
        }
    };

    const resetBuild = () => {
        setBuildResult(null);
    };

    if (buildResult) {
        return <BuildResult build={buildResult} onReset={resetBuild} />;
    }

    return (
        <>
            {error && <p role="alert" className="px-6 pt-6 text-center text-red-600">{error}</p>}
            <BuildForm onGenerate={handleGenerateBuild} isLoading={isLoading} />
        </>
    );
};

export default BuildPage;
