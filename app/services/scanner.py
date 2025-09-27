import yfinance as yf
from datetime import datetime, timedelta
from app.core.config import settings
from app.services.alerts import send_alerts
import pandas as pd

def run_scan():
    results = []
    for ticker in settings.tickers:
        df = yf.download(ticker, period="1d", interval="15m", progress=False)
        if df.empty:
            continue
        df.reset_index(inplace=True)
        reason = check_breakout(df)
        if reason:
            row = df.iloc[-1]
            results.append({
                "ticker": ticker,
                "price": float(row["Close"]),
                "volume": int(row["Volume"]),
                "reason": reason
            })
    if results:
        send_alerts(results)
    return results

def check_breakout(df):
    # VWAP reclaim
    df["Typ"] = (df["High"]+df["Low"]+df["Close"])/3
    df["VWAP"] = (df["Typ"]*df["Volume"]).cumsum() / df["Volume"].cumsum()
    if len(df)>1 and df["Close"].iloc[-2]<df["VWAP"].iloc[-2] and df["Close"].iloc[-1]>df["VWAP"].iloc[-1]:
        return "VWAP reclaim"
    # Volume spike
    avg_vol = df["Volume"].rolling(20).mean().iloc[-1]
    if df["Volume"].iloc[-1] > 2*avg_vol:
        return "Volume spike"
    return ""
