from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class Motherboard(Base):
    __tablename__ = "motherboard"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    model = Column(String, nullable=True)
    socket = Column(String, index=True, nullable=False)
    form_factor = Column(String, nullable=False)
    color = Column(String, nullable=False)
    memory_slots = Column(Integer, nullable=False)
    max_memory_gb = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)

