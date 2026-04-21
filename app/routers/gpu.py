from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.gpu import GPU
from app.dto.gpu import GPURead

router = APIRouter()


@router.get("/", response_model=List[GPURead])
def get_all_gpus(session: Session = Depends(get_db)):
    return session.scalars(select(GPU)).all()
