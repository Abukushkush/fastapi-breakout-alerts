from fastapi import APIRouter
from app.core.config import settings
from app.schemas.config import ConfigOut, ConfigIn

router = APIRouter()

@router.get("", response_model=ConfigOut)
def get_config():
    return ConfigOut.from_settings(settings)

@router.post("", response_model=ConfigOut)
def update_config(cfg: ConfigIn):
    for k, v in cfg.dict(exclude_unset=True).items():
        setattr(settings, k, v)
    return ConfigOut.from_settings(settings)
