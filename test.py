import yfinance as yf
import pandas as pd
import time
from flask import Flask, jsonify

app = Flask(__name__)

def get_all_indian_stocks(limit=50):
    tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", 
               "BHARTIARTL.NS", "SBI.NS", "LICI.NS", "ITC.NS", "HINDUNILVR.NS"]     
    all_data = []

    for symbol in tickers[:limit]: 
        try:
            ticker = yf.Ticker(symbol)            
            hist = ticker.history(period="1mo")            
            if not hist.empty:
                hist['Ticker'] = symbol
                hist['Company Name'] = ticker.info.get('longName', symbol)
                all_data.append(hist)
            time.sleep(0.5)             
        except Exception as e:
            print(f"Skipping {symbol}: {e}")
    
    if all_data:
        final_df = pd.concat(all_data)
        final_df = final_df.reset_index()
        return final_df[['Date', 'Company Name', 'Ticker', 'Close']].to_dict(orient='records')
    else:
        return []

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    data = get_all_indian_stocks(limit=20)  
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5000)  
