from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class GPU(Base):
    __tablename__ = "gpu"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, index=True, unique=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=True)
    vram_gb = Column(Integer, nullable=False)
    benchmark_score = Column(Integer, nullable=True)
    tdp = Column(Integer, nullable=False)
    price = Column(Float, nullable=True)

