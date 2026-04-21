from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cpu import CPU
from app.dto.cpu import CPURead

router = APIRouter()


@router.get("/", response_model=List[CPURead])
def get_all_cpus(session: Session = Depends(get_db)):
    return session.scalars(select(CPU)).all()
