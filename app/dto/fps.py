from typing import List

from pydantic import BaseModel

from app.dto.build import ComponentSummary


class FpsRange(BaseModel):
    min: int
    max: int

class ResolutionFps(BaseModel):
    resolution: str
    low: FpsRange
    medium: FpsRange
    high: FpsRange
    ultra: FpsRange

class GameFpsEstimate(BaseModel):
    game: str
    resolutions: List[ResolutionFps]

class FpsEstimateRequest(BaseModel):
    components: List[ComponentSummary]

class FpsEstimateResponse(BaseModel):
    estimates: List[GameFpsEstimate]
    disclaimer: str

class StandaloneFpsRequest(BaseModel):
    cpu_name: str
    gpu_name: str
    game: str

