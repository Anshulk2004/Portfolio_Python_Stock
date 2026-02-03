import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta
import pytz 

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

def fetch_portfolio_data():
    daily_records = []
    monthly_averages = []
    tz = pytz.timezone('Asia/Kolkata')
    today = datetime.now(tz)
    three_months_ago = today - timedelta(days=90)
    six_months_ago = today - timedelta(days=180)

    for symbol in TICKERS:
        try:
            print(f"Syncing: {symbol}...")
            ticker = yf.Ticker(symbol)
            full_hist = ticker.history(start=six_months_ago, end=today)
            
            if full_hist.empty:
                print(f"No data for {symbol}")
                continue

            info = ticker.info
            sector = info.get('sector', 'N/A')
            market_cap = info.get('marketCap', 0)
            pe_ratio = info.get('trailingPE', 0)
            comp_name = info.get('longName', symbol)
            daily_df = full_hist[full_hist.index >= three_months_ago].copy()
            if not daily_df.empty:
                daily_df['Ticker'] = symbol
                daily_df['Company Name'] = comp_name
                daily_df['Sector'] = sector
                daily_df['Market Cap'] = market_cap
                daily_df['PE Ratio'] = pe_ratio
                daily_records.append(daily_df)
            older_df = full_hist[full_hist.index < three_months_ago].copy()
            if not older_df.empty:
                monthly_resampled = older_df.resample('ME').mean()
                monthly_resampled['Ticker'] = symbol
                monthly_resampled['Company Name'] = comp_name
                monthly_resampled['Type'] = 'Monthly_Average'
                monthly_averages.append(monthly_resampled)

            time.sleep(0.2) 
        except Exception as e:
            print(f"Error {symbol}: {e}")
    if daily_records:
        pd.concat(daily_records).to_csv("Daily_3Mo_Data.csv")
        print("Saved Daily_3Mo_Data.csv")
    
    if monthly_averages:
        pd.concat(monthly_averages).to_csv("Monthly_Avg_Data.csv")
        print("Saved Monthly_Avg_Data.csv")

    if not daily_records and not monthly_averages:
        print("Critical Error: No data was collected for any ticker.")

if __name__ == "__main__":
    fetch_portfolio_data()