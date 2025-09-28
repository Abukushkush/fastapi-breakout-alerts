import yfinance as yf, requests, re
from app.core.config import settings
from app.services.alerts import send_alerts

FINVIZ_URL = "https://finviz.com/screener.ashx?v=111&f=sh_curvol_o200,sh_price_o0.5&o=volume&c=1"

def get_candidates() -> list[str]:
    """Return tickers that meet volume > 200k, price > $0.5, sorted by volume."""
    resp = requests.get(FINVIZ_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.raise_for_status()
    tickers = re.findall(r'"?(\w+)"?\s+</a></td>', resp.text)
    return list(dict.fromkeys(tickers))[:400]   # de-dup + cap at 400

def run_scan():
    candidates = get_candidates()
    results = []
    for ticker in candidates:
        df = yf.download(ticker, period="1d", interval="15m", progress=False)
        if df.empty: continue
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
    if results: send_alerts(results)
    return results

def check_breakout(df):
    df["Typ"] = (df["High"]+df["Low"]+df["Close"])/3
    df["VWAP"] = (df["Typ"]*df["Volume"]).cumsum() / df["Volume"].cumsum()
    if len(df)>1 and df["Close"].iloc[-2]<df["VWAP"].iloc[-2] and df["Close"].iloc[-1]>df["VWAP"].iloc[-1]:
        return "VWAP reclaim"
    avg_vol = df["Volume"].rolling(20).mean().iloc[-1]
    if df["Volume"].iloc[-1] > 2*avg_vol:
        return "Volume spike"
    return ""
