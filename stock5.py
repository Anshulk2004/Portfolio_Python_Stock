import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz
import time

TICKERS = [ 'ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS',
    'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS',
    'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS',
    'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
    'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ITC.NS',
    'INDUSINDBK.NS', 'INFY.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LTIM.NS',
    'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NTPC.NS', 'NESTLEIND.NS', 'ONGC.NS',
    'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SUNPHARMA.NS',
    'TCS.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TECHM.NS',
    'TITAN.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'WIPRO.NS' ] 

TZ = pytz.timezone("Asia/Kolkata")

PERIODS = {    
    "12mo": 360
}

def cumulative_metrics(df, dividends):
    return {
        "High": df["High"].max(),
        "Low": df["Low"].min(),
        "Volume": df["Volume"].sum(),
        "Dividends": dividends
    }

def fetch_portfolio_data():
    now = datetime.now(TZ)
    records = []

    for symbol in TICKERS:
        try:
            print(f"Fetching {symbol}")
            ticker = yf.Ticker(symbol)

            hist = ticker.history(period="12mo", actions=True)
            if hist.empty:
                continue

            info = ticker.info
            meta = {
                "Symbol": symbol,
                "Company": info.get("longName", symbol),
                "Sector": info.get("sector", "N/A"),
                "MarketCap": info.get("marketCap", 0),
                "PE": info.get("trailingPE", 0),
                "LastUpdated": now.isoformat()
            }

            for _, days in PERIODS.items():
                if days == 0:
                    df = hist.tail(1)
                else:
                    start = now - timedelta(days=days)
                    df = hist[hist.index >= start]

                if df.empty:
                    continue

                dividends = df["Dividends"].sum() if "Dividends" in df else 0
                metrics = cumulative_metrics(df, dividends)

                records.append({**meta, **metrics})

            time.sleep(0.2)

        except Exception as e:
            print(f"{symbol} failed: {e}")

    if records:
        pd.DataFrame(records).to_csv("Structured_Portfolio_Data.csv", index=False)
        print("Saved Structured_Portfolio_Data.csv")
    else:
        print("No data collected")

if __name__ == "__main__":
    fetch_portfolio_data()
