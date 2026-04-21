from sqlalchemy import Column, Boolean, Float, Integer, String

from app.database import Base


class CPU(Base):
    __tablename__ = "cpu"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    brand = Column(String, nullable=False)
    cores = Column(Integer, nullable=False)
    single_core_score = Column(Integer, nullable=True)
    multi_core_score = Column(Integer, nullable=True)
    tdp = Column(Integer, nullable=False)
    socket = Column(String, index=True, nullable=False)
    integrated_gpu = Column(Boolean, nullable=False)
    price = Column(Float, nullable=True)

