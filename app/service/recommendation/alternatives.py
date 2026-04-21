from sqlalchemy.orm import Session

from app.database import Base
from app.models.cpu import CPU
from app.models.gpu import GPU
from app.models.motherboard import Motherboard
from app.repository import components as repository
from app.repository.criteria import GPUCriteria
from app.service.recommendation import generator
from app.service.recommendation.rules import (
    ALTERNATIVE_PSU_TIERS, COMPONENT_PRICE_RANGE, CPU_BRANDS, GPU_BRAND_PREFIXES, GPU_PROFILES,
    SOCKET_DDR_MAP, STORAGE_PRICE_RANGE,
)


def _price_range(price: float, multipliers: tuple[float, float]) -> tuple[float, float]:
    return round(price * multipliers[0], 2), round(price * multipliers[1], 2)


def find_gpu_alternatives(db: Session, parts: dict[str, Base], use_case: str) -> list[tuple[str, GPU]]:
    selected = parts['GPU']
    min_price, max_price = _price_range(selected.price, COMPONENT_PRICE_RANGE)
    brands = {'NVIDIA': None} if use_case == 'Machine Learning' else GPU_BRAND_PREFIXES
    alternatives = []
    profile = GPU_PROFILES[use_case]
    criteria = GPUCriteria(
        prefixes=tuple(profile["prefixes"]),
        prioritize_vram=profile["prioritize_vram"],
    )
    for brand, prefixes in brands.items():
        if use_case != 'Machine Learning' and brand == selected.brand.upper():
            continue
        candidates = repository.get_gpu_alternatives(
            db, min_price, max_price, selected.id,
            criteria=criteria,
            brand_prefixes=tuple(prefixes) if prefixes is not None else None,
        )
        gpu = next((candidate for candidate in candidates
                    if generator.calculate_required_wattage(parts['CPU'], candidate) <= parts['PSU'].wattage), None)
        if gpu is not None:
            alternatives.append((brand.capitalize(), gpu))
    return alternatives


def find_cpu_alternatives(
    db: Session, parts: dict[str, Base], sort_key: str,
) -> tuple[list[tuple[str, CPU]], list[tuple[str, Motherboard]]]:
    selected = parts['CPU']
    min_price, max_price = _price_range(selected.price, COMPONENT_PRICE_RANGE)
    cpus, boards = [], []
    for brand in CPU_BRANDS:
        if brand == selected.brand.upper():
            continue
        candidates = repository.get_cpu_alternatives(
            db, min_price, max_price, brand, sort_key,
            ram=parts['RAM'], socket_memory_types=SOCKET_DDR_MAP,
        )
        result = next(((cpu, board) for cpu, board in candidates
                       if generator.calculate_required_wattage(cpu, parts['GPU']) <= parts['PSU'].wattage), None)
        if result is not None:
            cpu, board = result
            cpus.append((brand.capitalize(), cpu))
            boards.append((brand.capitalize(), board))
    return cpus, boards


def find_build_alternatives(db: Session, parts: dict[str, Base], use_case: str, cpu_sort_key: str) -> dict:
    cpus, boards = find_cpu_alternatives(db, parts, cpu_sort_key)
    storage = parts['Storage']
    min_price, max_price = _price_range(storage.price, STORAGE_PRICE_RANGE)
    drives = repository.get_storage_alternatives(
        db, min_price, max_price,
        storage.id,
    )
    psus = repository.get_psu_alternatives(
        db, generator.calculate_required_wattage(parts['CPU'], parts['GPU']),
        tuple(ALTERNATIVE_PSU_TIERS), parts['PSU'].id,
    )
    return {
        'CPU': cpus, 'Motherboard': boards,
        'GPU': find_gpu_alternatives(db, parts, use_case),
        'Storage': [(drive.type, drive) for drive in drives],
        'PSU': [(f'Tier {psu.tier}', psu) for psu in psus],
    }
