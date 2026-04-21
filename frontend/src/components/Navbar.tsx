import { useState } from 'react';
import { NavLink } from 'react-router-dom';

const Navbar = () => {
    const [menuOpen, setMenuOpen] = useState(false);

    const linkClass = ({ isActive }: { isActive: boolean }) =>
        `text-sm font-medium transition-colors ${isActive ? 'text-black' : 'text-neutral-400 hover:text-black'}`;

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-neutral-200">
            <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                <NavLink to="/" className="flex items-center gap-2" onClick={() => setMenuOpen(false)}>
                    <img
                        src="/logo.png"
                        alt="PC Builder Logo"
                        className="h-10 w-10 object-cover rounded-lg"
                    />
                    <span className="text-lg font-bold text-black">Parts Optimizer</span>
                </NavLink>

                {/* Desktop links */}
                <div className="hidden md:flex items-center gap-8">
                    <NavLink to="/build" className={linkClass}>Build</NavLink>
                    <NavLink to="/faq" className={linkClass}>FAQ</NavLink>
                    <NavLink to="/fps-estimator" className={linkClass}>AI FPS Estimator</NavLink>
                </div>

                {/* Mobile hamborger */}
                <button
                    className="md:hidden p-2 rounded-lg hover:bg-neutral-100 transition-colors"
                    onClick={() => setMenuOpen(!menuOpen)}
                    aria-label="Toggle menu"
                >
                    {menuOpen ? "X" : "☰"}
                </button>
            </div>

            {/* Menu */}
            {menuOpen && (
                <div className="md:hidden bg-white border-t border-neutral-200 px-6 py-4 space-y-3">
                    <NavLink to="/build" className={linkClass} onClick={() => setMenuOpen(false)}>
                        <span className="block py-2">Build</span>
                    </NavLink>
                    <NavLink to="/faq" className={linkClass} onClick={() => setMenuOpen(false)}>
                        <span className="block py-2">FAQ</span>
                    </NavLink>
                    <NavLink to="/fps-estimator" className={linkClass} onClick={() => setMenuOpen(false)}>
                        <span className="block py-2">AI FPS Estimator</span>
                    </NavLink>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
