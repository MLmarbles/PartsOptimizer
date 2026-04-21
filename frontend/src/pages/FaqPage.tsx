import { useState } from "react";

interface FaqItem {
    title: string;
    content: string;
}

const faqs: FaqItem[] = [
    { title: "How are components chosen based on use case?", content: "Each use case has a different budget split across the GPU, CPU, and RAM. For gaming, most of the budget goes towards the GPU as it is important for rendering textures, lighting and frames. A significant portion also goes towards the CPU to prevent bottlenecking. In video editing, the CPU is the most important, handling encoding and effects. RAM also helps in storing large video files and previews while the GPU helps with rendering.With machine learning, the most important part by far is the GPU. Machine learning training relies heavly on GPU compute and NVIDIA GPUs dominate this space due to their CUDA support. VRAM is also taken into consideration as it allows loading larger machine learning models." },
    { title: "How does power supply tiers work?", content: "Power supplies (or PSU) rankings are taken from the Cultists PSU Tier List, a highly regarded community maintained ranking. Rankings range from S to F, though only PSUs tier C and above are considered in the recommendation system as it's the lowest acceptable tier. The rankings are based on variables such as the quality of internal components like capacitors and transformers, protections, and voltage regulation. A higher wattage PSU does not neccesarily mean more output as it could deliver less power on the 12V rail which is where parts get their power from. And so choosing a quality PSU is important for stability and safety." },
    { title: "What do the FPS estimates mean?", content: "FPS estimates are taken from GPT 4o mini model and give a rough guide on what real in game results can be expected. Results have been fairly accurate from my testing cross referencing games like Fortnite and Minecraft.However, results should be taken with a grain of salt and users should always check true results on Youtube." },
    { title: "Where do benchmark scores come from?", content: "Scores are taken from Geekbench, with CPUs tested on Geekbench 6 and GPUs tested on OpenCL. The recommendation system takes these scores into account and chooses the highest scoring CPU/GPU within the assigned budget." },
];

const FaqPage = () => {
    const [selected, setSelected] = useState<FaqItem | null>(null);

    return (
        <div className="min-h-screen bg-white text-black font-sans">
            <div className="max-w-3xl mx-auto px-6 py-16">
                <h1 className="text-4xl font-bold mb-2">FAQ</h1>
                <p className="text-neutral-500 mb-12">Here you can find info on how the site works and info on parts.</p>

                <div className="space-y-4">
                    {faqs.map((faq, i) => (
                        <div
                            key={i}
                            onClick={() => setSelected(faq)}
                            className="border-2 border-neutral-200 rounded-2xl p-6 cursor-pointer hover:border-neutral-400 hover:shadow-md transition-all"
                        >
                            <h2 className="text-base font-bold text-black">{faq.title}</h2>
                        </div>
                    ))}
                </div>
            </div>

            {selected && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
                    onClick={() => setSelected(null)}
                >
                    <div
                        className="bg-white rounded-3xl shadow-2xl w-full max-w-lg max-h-[85vh] overflow-y-auto p-8 space-y-6"
                        onClick={e => e.stopPropagation()}
                    >
                        <div className="flex items-center justify-between">
                            <h2 className="text-lg font-bold text-black">{selected.title}</h2>
                            <button
                                onClick={() => setSelected(null)}
                                className="w-8 h-8 flex items-center justify-center rounded-lg bg-neutral-200 hover:bg-neutral-300 transition-colors"
                            >
                                ✕
                            </button>
                        </div>
                        <p className="text-neutral-600 leading-relaxed">{selected.content}</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default FaqPage;
