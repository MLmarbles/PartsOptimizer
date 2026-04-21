from typing import Optional
from pydantic import BaseModel, ConfigDict


class GPUBase(BaseModel):
    name: str
    brand: str
    model: Optional[str] = None
    vram_gb: int
    benchmark_score: Optional[int] = None
    tdp: int
    price: Optional[float] = None


class GPURead(GPUBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
