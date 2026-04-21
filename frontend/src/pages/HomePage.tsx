import { Link } from 'react-router-dom';

const HomePage = () => {
    return (
        <div className="min-h-screen text-white font-sans">
            <div className="flex bg-black flex-col md:flex-row items-center justify-center gap-10 md:gap-20 lg:gap-46 px-6 md:px-16 py-20 md:py-54">
                <div className="text-center md:text-left space-y-6 max-w-lg">
                    <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-white">
                        Parts Optimizer
                    </h1>
                    <p className="text-neutral-400 text-base md:text-lg">
                        Getting started with PC building and not sure where to start? Try Parts Optimizer now to configure your opitmal build!
                    </p>
                    <Link
                        to="/build"
                        className="inline-block px-10 md:px-12 py-4 bg-white text-black hover:bg-neutral-200 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105 active:scale-95 font-bold text-base md:text-lg tracking-wide"
                    >
                        Start Building
                    </Link>
                </div>

                <div className="shrink-0">
                    <img
                        src="/hero-pc.png"
                        alt="Custom gaming PC"
                        className="w-64 md:w-80 lg:w-125 h-auto rounded-2xl shadow-2xl"
                    />
                </div>

            </div>

            <div className="bg-white px-6 md:px-16 pt-12 md:pt-16 pb-20 md:pb-54 text-black">
                <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight text-center mb-8 md:mb-12">
                    New to PC Building?
                </h2>
                <p className="text-neutral-500 text-base md:text-lg text-center max-w-2xl mx-auto mb-10 md:mb-16">
                    Check out these videos to get started on your PC building journey.
                </p>

                <div className="flex flex-col md:flex-row items-center md:items-start justify-center gap-10 md:gap-16">
                    <div className="flex flex-col items-center w-full max-w-md md:w-md">
                        <h3 className="text-lg font-bold mb-1 text-center">How to Build a PC</h3>
                        <p className="text-neutral-500 text-sm text-center mb-4 min-h-10">A complete step-by-step guide to assembling your first PC from scratch.</p>
                        <div className="w-full aspect-video rounded-2xl overflow-hidden shadow-lg">
                            <iframe
                                className="w-full h-full"
                                src="https://www.youtube.com/embed/BL4DCEp7blY"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowFullScreen
                            />
                        </div>
                    </div>

                    <div className="flex flex-col items-center w-full max-w-md md:w-md">
                        <h3 className="text-lg font-bold mb-1 text-center">Picking the Right Parts</h3>
                        <p className="text-neutral-500 text-sm text-center mb-4 min-h-10">Learn how to choose compatible components that fit your budget and needs.</p>
                        <div className="w-full aspect-video rounded-2xl overflow-hidden shadow-lg">
                            <iframe
                                className="w-full h-full"
                                src="https://www.youtube.com/embed/j_DcWgxMZ3k"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowFullScreen
                            />
                        </div>
                    </div>

                    <div className="flex flex-col items-center w-full max-w-md md:w-md">
                        <h3 className="text-lg font-bold mb-1 text-center">PC Parts Explained</h3>
                        <p className="text-neutral-500 text-sm text-center mb-4 min-h-10">You'll learn what each component of your pc does in this video.</p>
                        <div className="w-full aspect-video rounded-2xl overflow-hidden shadow-lg">
                            <iframe
                                className="w-full h-full"
                                src="https://www.youtube.com/embed/ExxFxD4OSZ0"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowFullScreen
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HomePage;
