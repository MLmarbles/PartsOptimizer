from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dto.build import BuildRequest, BuildResponse
from app.dto.fps import FpsEstimateRequest, FpsEstimateResponse, StandaloneFpsRequest
from app.service.recommendation.generator import generate_build
from app.service.fps_estimator import estimate_fps, estimate_fps_standalone

router = APIRouter()


@router.post("/generate", response_model=BuildResponse)
def generate_recommendation(*, session: Session = Depends(get_db), request: BuildRequest):
    return generate_build(session, request.budget, request.use_case)

@router.post("/estimate-fps", response_model=FpsEstimateResponse)
def estimate_build_fps(*, request: FpsEstimateRequest):
    result = estimate_fps(request.components)
    return FpsEstimateResponse(**result)

@router.post("/estimate-fps-standalone", response_model=FpsEstimateResponse)
def estimate_fps_standalone_endpoint(*, request: StandaloneFpsRequest):
    result = estimate_fps_standalone(request.cpu_name, request.gpu_name, request.game)
    return FpsEstimateResponse(**result)
