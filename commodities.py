import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# Tickers for Gold, Silver, Crude Oil, etc.
COMMODITIES = {
    "GC=F": "Gold",
    "SI=F": "Silver",
    "CL=F": "Crude Oil",
    "HG=F": "Copper"
}

TZ = pytz.timezone("Asia/Kolkata")

def fetch_commodity_data():
    records = []
    print("Fetching Commodity Prices...")

    for ticker_symbol, name in COMMODITIES.items():
        try:
            ticker = yf.Ticker(ticker_symbol)
            # Getting 5 days of data to ensure we have a valid previous close for change calculation
            hist = ticker.history(period="5d")
            
            if hist.empty:
                print(f"No data for {name}")
                continue
            
            current_price = hist["Close"].iloc[-1]
            prev_close = hist["Close"].iloc[-2]
            
            records.append({
                "Asset": name,
                "Ticker": ticker_symbol,
                "Current Price (USD)": round(current_price, 2),
                "Day Change %": round(((current_price - prev_close) / prev_close) * 100, 2),
                "Day High": round(hist["High"].iloc[-1], 2),
                "Day Low": round(hist["Low"].iloc[-1], 2),
                "Last Updated": datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"Success: {name}")

        except Exception as e:
            print(f"Error fetching {name}: {e}")

    if records:
        df = pd.DataFrame(records)
        df.to_csv("Live_Commodity_Data.csv", index=False)
        print("\nSaved: Live_Commodity_Data.csv")

if __name__ == "__main__":
    fetch_commodity_data()