from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.scanner import run_scan
from app.core.config import settings

def start_scheduler(scheduler: AsyncIOScheduler):
    scheduler.add_job(run_scan, "interval", minutes=settings.scan_interval_minutes, id="scan")
    scheduler.start()

def stop_scheduler(scheduler: AsyncIOScheduler):
    scheduler.shutdown()
