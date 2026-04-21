from typing import List, Optional
from pydantic import BaseModel

class BuildRequest(BaseModel):
    budget: int
    use_case: str  

class ComponentSpecs(BaseModel):
    vram_gb: Optional[int] = None
    benchmark_score: Optional[int] = None
    cores: Optional[int] = None
    single_core_score: Optional[int] = None
    multi_core_score: Optional[int] = None
    capacity_gb: Optional[int] = None
    type: Optional[str] = None
    speed_mhz: Optional[int] = None
    socket: Optional[str] = None
    form_factor: Optional[str] = None
    interface: Optional[str] = None
    wattage: Optional[int] = None
    efficiency_rating: Optional[str] = None

class AlternativeSummary(BaseModel):
    brand: str        
    name: str         
    price: float
    specs: ComponentSpecs

class ComponentSummary(BaseModel):
    type: str 
    name: str
    price: float
    specs: ComponentSpecs
    tier: Optional[str] = None 
    alternatives: Optional[List[AlternativeSummary]] = None 

class BuildResponse(BaseModel):
    components: List[ComponentSummary]
    total_price: float
    remaining_budget: float
    use_case: str
