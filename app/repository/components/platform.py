import re
from collections.abc import Mapping

from sqlalchemy.orm import Session

from app.models.cpu import CPU
from app.models.motherboard import Motherboard
from app.models.ram import RAM


def _memory_type(board: Motherboard, socket_memory_types: Mapping[str, list[str]]) -> str | None:
    supported_types = socket_memory_types.get(board.socket, [])
    match = re.search(r'(?<![A-Z0-9_])(?:DDR|D)([345])(?![A-Z0-9_])', board.name.upper())
    if match:
        memory_type = f'DDR{match.group(1)}'
        return memory_type if memory_type in supported_types else None
    return supported_types[0] if len(supported_types) == 1 else None


def get_best_cpu(db: Session, max_price: float, sort_key: str) -> CPU | None:
    score = getattr(CPU, sort_key)
    available_sockets = db.query(Motherboard.socket).filter(Motherboard.price > 0)
    return (
        db.query(CPU)
        .filter(CPU.price > 0, CPU.price <= max_price, score.isnot(None),
                CPU.socket.in_(available_sockets))
        .order_by(score.desc(), CPU.price, CPU.id).first()
    )


def get_compatible_platform(
    db: Session, cpu: CPU, ram_budget: float, socket_memory_types: Mapping[str, list[str]], *,
    min_ram_capacity_gb: int = 0,
) -> tuple[Motherboard, RAM] | None:
    boards = (
        db.query(Motherboard)
        .filter(Motherboard.socket == cpu.socket, Motherboard.price > 0)
        .order_by(Motherboard.price, Motherboard.id).all()
    )
    for board in boards:
        memory_type = _memory_type(board, socket_memory_types)
        if memory_type is None:
            continue
        ram_query = db.query(RAM).filter(
            RAM.price > 0, RAM.type == memory_type,
            RAM.capacity_gb > 0, RAM.capacity_gb >= min_ram_capacity_gb,
            RAM.modules > 0, RAM.modules <= board.memory_slots,
        )
        if board.max_memory_gb is not None:
            ram_query = ram_query.filter(RAM.capacity_gb <= board.max_memory_gb)
        ram = (
            ram_query.filter(RAM.price <= ram_budget)
            .order_by(RAM.capacity_gb.desc(), RAM.speed_mhz.desc(), RAM.price, RAM.id).first()
        )
        if ram is None:
            ram = ram_query.order_by(RAM.price, RAM.capacity_gb.desc(), RAM.speed_mhz.desc(), RAM.id).first()
        if ram is not None:
            return board, ram
    return None


def get_cpu_alternatives(
    db: Session, min_price: float, max_price: float, brand: str, sort_key: str, *,
    ram: RAM, socket_memory_types: Mapping[str, list[str]],
) -> list[tuple[CPU, Motherboard]]:
    candidates = (
        db.query(CPU, Motherboard).select_from(CPU)
        .join(Motherboard, Motherboard.socket == CPU.socket)
        .filter(CPU.price > 0, CPU.price >= min_price, CPU.price <= max_price,
                CPU.brand.ilike(brand), getattr(CPU, sort_key).isnot(None), Motherboard.price > 0)
        .order_by(getattr(CPU, sort_key).desc(), Motherboard.price, CPU.price, CPU.id, Motherboard.id).all()
    )
    return [
        (cpu, board) for cpu, board in candidates
        if ram.type == _memory_type(board, socket_memory_types)
        and 0 < ram.modules <= board.memory_slots
        and ram.capacity_gb > 0
        and (board.max_memory_gb is None or ram.capacity_gb <= board.max_memory_gb)
    ]
