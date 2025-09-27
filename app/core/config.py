from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    twilio_account_sid: str = Field(..., env="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(..., env="TWILIO_AUTH_TOKEN")
    twilio_from: str = Field(..., env="TWILIO_FROM")
    sms_recipients: List[str] = Field(default_factory=list, env="SMS_RECIPIENTS")
    smtp_host: str = Field("smtp.gmail.com", env="SMTP_HOST")
    smtp_port: int = Field(587, env="SMTP_PORT")
    smtp_user: str = Field(..., env="SMTP_USER")
    smtp_pass: str = Field(..., env="SMTP_PASS")
    email_recipients: List[str] = Field(default_factory=list, env="EMAIL_RECIPIENTS")
    scan_interval_minutes: int = Field(15, env="SCAN_INTERVAL_MINUTES")
    tickers: List[str] = Field(default=["AAPL","MSFT","NVDA","AMD","TSLA"], env="TICKERS")
    class Config:
        env_file = ".env"

settings = Settings()
