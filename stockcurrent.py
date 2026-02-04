import yfinance as yf
import pandas as pd
from datetime import datetime
import tabulate # Optional: pip install tabulate (for pretty printing)

TICKERS = [
    'ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS',
    'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS',
    'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS',
    'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
    'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ITC.NS',
    'INDUSINDBK.NS', 'INFY.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LTIM.NS',
    'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NTPC.NS', 'NESTLEIND.NS', 'ONGC.NS',
    'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SUNPHARMA.NS',
    'TCS.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TECHM.NS',
    'TITAN.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'WIPRO.NS'
]

def run_test():
    print(f"--- Starting Test Fetch at {datetime.now().strftime('%H:%M:%S')} ---")
    
    # 1. Bulk Price/Volume Fetch
    print("Fetching live prices...")
    market_data = yf.download(TICKERS, period="1d", interval="1m", group_by='ticker', progress=False)
    
    # 2. Fundamental Fetch
    print("Fetching company details (Sector, PE, Market Cap)...")
    tickers_obj = yf.Tickers(" ".join(TICKERS))
    
    results = []
    for symbol in TICKERS:
        try:
            # Extract most recent price
            ticker_subset = market_data[symbol].dropna()
            price = ticker_subset['Close'].iloc[-1] if not ticker_subset.empty else "N/A"
            volume = ticker_subset['Volume'].iloc[-1] if not ticker_subset.empty else "N/A"
            
            # Extract info
            info = tickers_obj.tickers[symbol].info
            
            results.append({
                "Symbol": symbol,
                "Price": f"₹{price:.2f}" if isinstance(price, float) else price,
                "Sector": info.get('sector', 'N/A'),
                "P/E": round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else "N/A",
                "Market Cap": f"{info.get('marketCap', 0):,}",
                "Volume": f"{int(volume):,}" if isinstance(volume, (int, float)) else volume
            })
        except Exception as e:
            print(f"Skipping {symbol}: {e}")

    # Display as a Table
    df = pd.DataFrame(results)
    print("\n" + df.to_string(index=False))
    print(f"\n--- Test Complete. Total Stocks Fetched: {len(results)} ---")

if __name__ == "__main__":
    run_test()