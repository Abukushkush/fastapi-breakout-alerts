from pydantic import BaseModel, Field
from typing import List

class ConfigOut(BaseModel):
    tickers: List[str]
    scan_interval_minutes: int
    sms_recipients: List[str]
    email_recipients: List[str]
    @staticmethod
    def from_settings(s):
        return ConfigOut(
            tickers=s.tickers,
            scan_interval_minutes=s.scan_interval_minutes,
            sms_recipients=s.sms_recipients,
            email_recipients=s.email_recipients,
        )

class ConfigIn(BaseModel):
    tickers: List[str] = None
    scan_interval_minutes: int = None
    sms_recipients: List[str] = None
    email_recipients: List[str] = None
