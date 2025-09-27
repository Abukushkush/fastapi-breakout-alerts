from fastapi import APIRouter, BackgroundTasks
from app.services.scanner import run_scan
from app.schemas.scan import ScanResult

router = APIRouter()

@router.post("/manual", response_model=list[ScanResult])
def manual_scan(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_scan)
    return run_scan()
