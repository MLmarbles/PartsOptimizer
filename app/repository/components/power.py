from sqlalchemy.orm import Session

from app.models.psu import PSU


def get_best_psu(
    db: Session, min_wattage: int, tiers: tuple[str, ...],
) -> PSU | None:
    return (
        db.query(PSU)
        .filter(PSU.price > 0, PSU.wattage >= min_wattage, PSU.tier.in_(tiers))
        .order_by(PSU.price, PSU.id).first()
    )


def get_psu_alternatives(db: Session, min_wattage: int, tiers: tuple[str, ...], exclude_id: int) -> list[PSU]:
    return (
        db.query(PSU)
        .filter(PSU.price > 0, PSU.wattage >= min_wattage, PSU.tier.in_(tiers), PSU.id != exclude_id)
        .order_by(PSU.price, PSU.id).limit(2).all()
    )
