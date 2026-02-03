import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz
import time

TICKERS = ['ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS',
    'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS',
    'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS',
    'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
    'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ITC.NS',
    'INDUSINDBK.NS', 'INFY.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LTIM.NS',
    'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NTPC.NS', 'NESTLEIND.NS', 'ONGC.NS',
    'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SUNPHARMA.NS',
    'TCS.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TECHM.NS',
    'TITAN.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'WIPRO.NS',
    'ABB.NS', 'ACC.NS', 'AWL.NS', 'AMBUJACEM.NS', 'ASTRAL.NS', 
    'AUSMALL.NS', 'DMART.NS', 'BAJAJHLDNG.NS', 'BALKRISIND.NS', 'BANDHANBNK.NS',
    'BANKBARODA.NS', 'BANKINDIA.NS', 'BERGEPAINT.NS', 'BEL.NS', 'BHARATFORG.NS',
    'BHEL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'CANBK.NS', 'CGPOWER.NS',
    'CHOLAFIN.NS', 'CONCOR.NS', 'CUMMINSIND.NS', 'DLF.NS', 'DABUR.NS',
    'DALBHARAT.NS', 'DEEPAKNTR.NS', 'ESCORTS.NS', 'FSNRENEW.NS', 'FEDERALBNK.NS',
    'FORTIS.NS', 'GAIL.NS', 'GLAND.NS', 'GODREJCP.NS', 'GODREJPROP.NS',
    'GUJGASLTD.NS', 'HAL.NS', 'HAVELLS.NS', 'HDFCAMC.NS', 'ICICIGI.NS',
    'ICICIPRULI.NS', 'IDFCFIRSTB.NS', 'IRCTC.NS', 'IRFC.NS', 'IGL.NS',
    'INDUSTOWER.NS', 'IOC.NS', 'JOBY.NS', 'JINDALSTEL.NS', 'JUBLFOOD.NS',
    'KAYNES.NS', 'KEI.NS', 'KOTAKGOLD.NS', 'KPITTECH.NS', 'L&TFH.NS',
    'LICI.NS', 'LUPIN.NS', 'MRF.NS', 'MAHABANK.NS', 'MAXHEALTH.NS',
    'MAZDOCK.NS', 'METROBRAND.NS', 'MPHASIS.NS', 'MUTHOOTFIN.NS', 'NHPC.NS',
    'NMDC.NS', 'NAUKRI.NS', 'OBEROIRLTY.NS', 'OFSS.NS', 'PAYTM.NS',
    'PIIND.NS', 'PFC.NS', 'PAGEIND.NS', 'PATANJALI.NS', 'PNB.NS',
    'POLYCAB.NS', 'POONAWALLA.NS', 'PRESTIGE.NS', 'RECLTD.NS', 'RVNL.NS',
    'SAIL.NS', 'SRF.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS',
    'SONACOMS.NS', 'SOLARINDS.NS', 'STL.NS', 'SYNGENE.NS', 'TATACOMM.NS',
    'TATAELXSI.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TRENT.NS', 'TIINDIA.NS',
    'TVSMOTOR.NS', 'UNOMINDA.NS', 'UNITDSPR.NS', 'VBL.NS', 'VEDL.NS',
    'VOLTAS.NS', 'YESBANK.NS', 'ZOMATO.NS', 'ZYDUSLIFE.NS'
]

TZ = pytz.timezone("Asia/Kolkata")

PERIODS = {
    "today": 0,
    "yesterday": 1,
    "7d": 7,
    "1mo": 30,
    "3mo": 90,
    "6mo": 180
}

def cumulative_metrics(df):
    return {
        "Open": df["Open"].iloc[0],
        "High": df["High"].max(),
        "Low": df["Low"].min(),
        "Close": df["Close"].iloc[-1],
        "Volume": df["Volume"].sum()
    }

def fetch_portfolio_data():
    now = datetime.now(TZ)
    records = []

    for symbol in TICKERS:
        try:
            print(f"Fetching {symbol}")
            ticker = yf.Ticker(symbol)

            hist = ticker.history(period="6mo", actions=False)
            if hist.empty:
                continue

            info = ticker.info
            meta = {
                "Ticker": symbol,
                "Company": info.get("longName", symbol),
                "Sector": info.get("sector", "N/A"),
                "MarketCap": info.get("marketCap", 0),
                "PE": info.get("trailingPE", 0),
                "LastUpdated": now.isoformat()
            }

            for label, days in PERIODS.items():
                if days == 0:  # today
                    df = hist.tail(1)
                else:
                    start = now - timedelta(days=days)
                    df = hist[hist.index >= start]

                if df.empty:
                    continue

                metrics = cumulative_metrics(df)
                records.append({
                    **meta,
                    "Period": label,
                    **metrics
                })

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
