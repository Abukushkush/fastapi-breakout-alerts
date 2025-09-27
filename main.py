from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.routers import scan, config
from app.core.config import settings
from app.core.scheduler import start_scheduler, stop_scheduler

app = FastAPI(title="Breakout Alerts", version="1.0.0")
scheduler = AsyncIOScheduler()

app.include_router(scan.router, prefix="/scan", tags=["scan"])
app.include_router(config.router, prefix="/config", tags=["config"])

@app.on_event("startup")
async def startup():
    start_scheduler(scheduler)

@app.on_event("shutdown")
async def shutdown():
    stop_scheduler(scheduler)

@app.get("/")
def health():
    return {"status": "ok"}
