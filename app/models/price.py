from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, nullable=False)

    component_type = Column(String, index=True, nullable=False)
    component_id = Column(Integer, index=True, nullable=False)

    retailer = Column(String, nullable=False)
    country = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    url = Column(String, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
