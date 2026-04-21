from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import create_db_and_tables, engine
from app.models.cpu import CPU
from app.routers import build, cpu, gpu

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    with Session(engine) as session:
        has_cpus = session.scalar(select(CPU.id).limit(1)) is not None

    if not has_cpus:
        from app.dataload.load_cpu_data import load_cpu_data
        from app.dataload.load_gpu_data import load_gpu_data
        from app.dataload.load_ram_data import load_ram_data
        from app.dataload.load_storage_data import load_storage_data
        from app.dataload.load_motherboard_data import load_motherboard_data
        from app.dataload.load_psu_data import load_psu_data
        from app.dataload.load_psu_tier_data import assign_tiers

        load_cpu_data()
        load_gpu_data()
        load_ram_data()
        load_storage_data()
        load_motherboard_data()
        load_psu_data()
        assign_tiers()
        print("seeded")

app.include_router(cpu.router, prefix="/api/v1/cpu", tags=["CPU"])
app.include_router(gpu.router, prefix="/api/v1/gpu", tags=["GPU"])
app.include_router(build.router, prefix="/api/v1/build", tags=["Build"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "PC Builder API is online."}
