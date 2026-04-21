from sqlalchemy.orm import Session

from app.database import Base
from app.dto.build import BuildResponse
from app.models.cpu import CPU
from app.models.gpu import GPU
from app.repository import components as repository
from app.repository.criteria import GPUCriteria, StorageCriteria
from app.service.recommendation import alternatives
from app.service.recommendation.response import build_response
from app.service.recommendation.rules import (
    ACCEPTABLE_PSU_TIERS, BUDGET_WEIGHTS, GPU_PROFILES, OTHER_COMPONENT_WATTAGE,
    PSU_POWER_MULTIPLIER, SOCKET_DDR_MAP, STORAGE_INTERFACE_RANKS,
)


def calculate_required_wattage(cpu: CPU, gpu: GPU) -> int:
    return int((cpu.tdp + gpu.tdp + OTHER_COMPONENT_WATTAGE) * PSU_POWER_MULTIPLIER)


class _BuildPlanner:
    def __init__(self, db: Session, budget: int, use_case: str):
        self.db = db
        self.budget = budget
        self.targets = {kind: budget * weight for kind, weight in BUDGET_WEIGHTS[use_case].items()}
        self.cpu_sort_key = 'multi_core_score' if use_case == 'Video Editing' else 'single_core_score'
        self.storage_criteria = StorageCriteria(STORAGE_INTERFACE_RANKS)
        profile = GPU_PROFILES[use_case]
        self.gpu_criteria = GPUCriteria(
            prefixes=tuple(profile['prefixes']),
            prioritize_vram=profile['prioritize_vram'],
        )

    def initial_build(self) -> dict[str, Base]:
        cpu = repository.get_best_cpu(self.db, self.targets['CPU'], self.cpu_sort_key)
        platform = repository.get_compatible_platform(self.db, cpu, self.targets['RAM'], SOCKET_DDR_MAP)
        board, ram = platform
        storage = repository.get_best_storage(self.db, self.targets['Storage'], self.storage_criteria)
        parts = {'CPU': cpu, 'Motherboard': board, 'RAM': ram, 'Storage': storage}
        gpu = repository.get_best_gpu(
            self.db, self.targets['GPU'], criteria=self.gpu_criteria, allow_over_budget=True,
        )
        return {**parts, 'GPU': gpu}

    def remaining_budget(self, parts: dict[str, Base]) -> float:
        return round(self.budget - sum(part.price for part in parts.values()), 2)

    def improve_cpu(self, parts: dict[str, Base]) -> dict[str, Base]:
        remaining = self.remaining_budget(parts)
        if remaining <= 0:
            return parts
        cpu = repository.get_best_cpu(self.db, parts['CPU'].price + remaining, self.cpu_sort_key)
        if cpu is None or getattr(cpu, self.cpu_sort_key) <= getattr(parts['CPU'], self.cpu_sort_key):
            return parts
        platform = repository.get_compatible_platform(
            self.db, cpu, max(self.targets['RAM'], parts['RAM'].price), SOCKET_DDR_MAP,
            min_ram_capacity_gb=parts['RAM'].capacity_gb,
        )
        if platform is None:
            return parts
        board, ram = platform
        return {**parts, 'CPU': cpu, 'Motherboard': board, 'RAM': ram}

    def improve_gpu(self, parts: dict[str, Base]) -> dict[str, Base]:
        remaining = self.remaining_budget(parts)
        if remaining <= 0:
            return parts
        gpu = repository.get_best_gpu(
            self.db, parts['GPU'].price + remaining, criteria=self.gpu_criteria,
        )
        return {**parts, 'GPU': gpu} if gpu is not None else parts

    def select_psu(self, parts: dict[str, Base]) -> dict[str, Base]:
        psu = repository.get_best_psu(
            self.db, calculate_required_wattage(parts['CPU'], parts['GPU']),
            tuple(ACCEPTABLE_PSU_TIERS),
        )
        if psu is None:
            raise ValueError('No adequate PSU is available for the final build.')
        return {**parts, 'PSU': psu}


def generate_build(db: Session, budget: int, use_case: str) -> BuildResponse:
    planner = _BuildPlanner(db, budget, use_case)
    parts = planner.initial_build()
    upgrades = (planner.improve_cpu, planner.improve_gpu) if use_case == 'Video Editing' else (
        planner.improve_gpu, planner.improve_cpu,
    )
    for upgrade in upgrades:
        parts = upgrade(parts)
    parts = planner.select_psu(parts)
    build_alternatives = alternatives.find_build_alternatives(db, parts, use_case, planner.cpu_sort_key)
    parts = {kind: parts[kind] for kind in ('GPU', 'CPU', 'RAM', 'Motherboard', 'Storage', 'PSU')}
    return build_response(parts, build_alternatives, budget, use_case)
