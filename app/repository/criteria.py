from dataclasses import dataclass


@dataclass(frozen=True)
class GPUCriteria:
    prefixes: tuple[str, ...]
    prioritize_vram: bool = False


@dataclass(frozen=True)
class StorageCriteria:
    interface_ranks: tuple[tuple[str, int], ...]
