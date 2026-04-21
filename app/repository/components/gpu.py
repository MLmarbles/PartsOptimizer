from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.gpu import GPU
from app.repository.criteria import GPUCriteria


def _prefix_filter(prefixes):
    return or_(False, *(func.upper(GPU.name).startswith(prefix.upper(), autoescape=True) for prefix in prefixes))


def _gpu_filters(criteria: GPUCriteria):
    return (
        GPU.price > 0, GPU.benchmark_score.isnot(None),
        _prefix_filter(criteria.prefixes),
    )


def _gpu_order(criteria: GPUCriteria):
    if criteria.prioritize_vram:
        return GPU.vram_gb.desc(), GPU.benchmark_score.desc()
    return GPU.benchmark_score.desc(), GPU.vram_gb.desc()


def get_best_gpu(
    db: Session, max_price: float, *, criteria: GPUCriteria,
    allow_over_budget: bool = False,
) -> GPU | None:
    query = db.query(GPU).filter(*_gpu_filters(criteria))
    gpu = (
        query.filter(GPU.price <= max_price)
        .order_by(*_gpu_order(criteria), GPU.price, GPU.id).first()
    )
    if gpu is None and allow_over_budget:
        return query.order_by(GPU.price, *_gpu_order(criteria), GPU.id).first()
    return gpu


def get_gpu_alternatives(
    db: Session, min_price: float, max_price: float, exclude_id: int, *,
    criteria: GPUCriteria,
    brand_prefixes: tuple[str, ...] | None = None,
) -> list[GPU]:
    query = (
        db.query(GPU)
        .filter(*_gpu_filters(criteria), GPU.id != exclude_id,
                GPU.price >= min_price, GPU.price <= max_price)
    )
    if brand_prefixes is not None:
        query = query.filter(_prefix_filter(brand_prefixes))
    return query.order_by(*_gpu_order(criteria), GPU.price, GPU.id).all()
