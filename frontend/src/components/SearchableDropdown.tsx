import { useEffect, useRef, useState } from 'react';
import type { FC } from 'react';
import type { PartOption } from '../types/parts';

interface SearchableDropdownProps {
    label: string;
    options: PartOption[];
    value: string;
    onChange: (value: string) => void;
    placeholder: string;
}

const SearchableDropdown: FC<SearchableDropdownProps> = ({ label, options, value, onChange, placeholder }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [search, setSearch] = useState('');
    const dropdownRef = useRef<HTMLDivElement>(null);

    const filtered = options.filter(opt =>
        opt.name.toLowerCase().includes(search.toLowerCase())
    );

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    return (
        <div ref={dropdownRef} className="relative">
            <label className="block text-xs font-bold uppercase tracking-wider text-neutral-500 mb-2">{label}</label>
            <button
                type="button"
                onClick={() => setIsOpen(!isOpen)}
                className={`w-full text-left px-4 py-3 bg-white border rounded-xl transition-all text-sm ${isOpen ? 'border-black ring-1 ring-black' : 'border-neutral-200 hover:border-neutral-400'
                    } ${value ? 'text-black font-medium' : 'text-neutral-400'}`}
            >
                <div className="flex items-center justify-between">
                    <span className="truncate">{value || placeholder}</span>
                    <span className={`text-neutral-400 text-xs transition-transform ${isOpen ? 'rotate-180 inline-block' : ''}`}>▼</span>
                </div>
            </button>
            {isOpen && (
                <div className="absolute z-30 left-0 right-0 mt-2 bg-white border border-neutral-200 rounded-xl shadow-xl overflow-hidden animate-fade-in">
                    <div className="p-2 border-b border-neutral-100">
                        <input
                            type="text"
                            value={search}
                            onChange={e => setSearch(e.target.value)}
                            placeholder="Search..."
                            autoFocus
                            className="w-full px-3 py-2 text-sm bg-neutral-50 border border-neutral-200 rounded-lg focus:outline-none focus:border-black focus:ring-1 focus:ring-black transition-all"
                        />
                    </div>
                    <div className="max-h-60 overflow-y-auto">
                        {filtered.length === 0 ? (
                            <div className="px-4 py-3 text-sm text-neutral-400 text-center">No results found</div>
                        ) : (
                            filtered.map(opt => (
                                <button
                                    key={opt.id}
                                    type="button"
                                    onClick={() => {
                                        onChange(opt.name);
                                        setSearch('');
                                        setIsOpen(false);
                                    }}
                                    className={`w-full text-left px-4 py-2.5 text-sm transition-colors ${value === opt.name
                                        ? 'bg-black text-white'
                                        : 'text-black hover:bg-neutral-50'
                                        }`}
                                >
                                    {opt.name}
                                </button>
                            ))
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default SearchableDropdown;
