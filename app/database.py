import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit = False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as db:
        yield db

def create_db_and_tables():
    from app.models.cpu import CPU
    from app.models.gpu import GPU
    from app.models.motherboard import Motherboard
    from app.models.price import Price
    from app.models.psu import PSU
    from app.models.ram import RAM
    from app.models.storage import Storage

    Base.metadata.create_all(engine)
