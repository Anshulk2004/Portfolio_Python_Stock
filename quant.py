import yfinance as yf
import asyncio
import json
import time
from datetime import datetime
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class QuantumEngine:
    def __init__(self):
        # 10 Nifty 50 Tickers
        self.tickers = [
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
            'HINDUNILVR.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'ITC.NS', 'KOTAKBANK.NS'
        ]
        self.pnl = 0.0

    async def get_data_packet(self):
        # Rotate through tickers every 2 seconds
        ticker = self.tickers[int(time.time() / 2) % len(self.tickers)]
        
        # Real Data Fetch (using tail(1) for latest minute)
        data = yf.Ticker(ticker).history(period="1d", interval="1m").tail(1)
        current_price = data['Close'].iloc[0] if not data.empty else 0
        
        start = time.perf_counter_ns()
        # Simulated Quantum Logic
        signal = "BUY" if (time.time() % 2 > 1) else "SELL"
        latency = (time.perf_counter_ns() - start) / 1000 
        
        self.pnl += round((time.time() % 0.1) - 0.045, 3)

        return {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "ticker": ticker,
            "price": round(current_price, 2),
            "signal": signal,
            "latency_us": round(latency, 2),
            "pnl": f"{round(self.pnl, 2)}%"
        }

engine = QuantumEngine()

@app.websocket("/ws/quantum")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            packet = await engine.get_data_packet()
            await websocket.send_json(packet)
            await asyncio.sleep(2) 
    except Exception:
        pass
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)