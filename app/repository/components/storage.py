from sqlalchemy import case
from sqlalchemy.orm import Session

from app.models.storage import Storage
from app.repository.criteria import StorageCriteria

def get_best_storage(db: Session, max_price: float, criteria: StorageCriteria) -> Storage | None:
    interface_rank = case(
        *((Storage.interface.contains(label, autoescape=True), rank) for label, rank in criteria.interface_ranks),
        else_=0,
    )
    return (
        db.query(Storage)
        .filter(Storage.price > 0, Storage.price <= max_price,
                Storage.type == 'SSD', Storage.capacity_gb > 0)
        .order_by(Storage.capacity_gb.desc(), interface_rank.desc(), Storage.price, Storage.id).first()
    )


def get_storage_alternatives(
    db: Session, min_price: float, max_price: float, exclude_id: int,
) -> list[Storage]:
    return (
        db.query(Storage)
        .filter(Storage.price > 0, Storage.price >= min_price, Storage.price <= max_price,
                Storage.id != exclude_id, Storage.type == 'SSD', Storage.capacity_gb > 0)
        .order_by(Storage.capacity_gb.desc(), Storage.price, Storage.id).limit(2).all()
    )
