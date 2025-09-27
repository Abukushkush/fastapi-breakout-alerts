from pydantic import BaseModel

class ScanResult(BaseModel):
    ticker: str
    price: float
    volume: int
    reason: str
