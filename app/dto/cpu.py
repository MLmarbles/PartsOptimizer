from typing import Optional
from pydantic import BaseModel, ConfigDict


class CPUBase(BaseModel):
    name: str
    brand: str
    cores: int
    single_core_score: Optional[int] = None
    multi_core_score: Optional[int] = None
    tdp: int
    socket: str
    integrated_gpu: bool
    price: Optional[float] = None


class CPURead(CPUBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
