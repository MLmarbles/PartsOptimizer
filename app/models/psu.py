from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class PSU(Base):
    __tablename__ = "psu"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    wattage = Column(Integer, nullable=False)
    efficiency_rating = Column(String, nullable=False)
    tier = Column(String, nullable=False)
    form_factor = Column(String, nullable=False)
    price = Column(Float, nullable=True)

