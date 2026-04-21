from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class RAM(Base):
    __tablename__ = "ram"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    model = Column(String, nullable=True)
    capacity_gb = Column(Integer, nullable=False)
    speed_mhz = Column(Integer, nullable=False)
    type = Column(String, index=True, nullable=False)
    modules = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    price = Column(Float, nullable=True)

