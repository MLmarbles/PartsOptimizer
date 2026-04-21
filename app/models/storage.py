from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class Storage(Base):
    __tablename__ = "storage"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    capacity_gb = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    interface = Column(String, nullable=False)
    price = Column(Float, nullable=True)

