import yfinance as yf
import time
from datetime import datetime

class MinimalQuantumHFT:
    def __init__(self):
        self.tickers = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS']
        self.pnl = 0.0
        self.is_active = True

    def get_data_packet(self):
        """ This is the exact JSON packet we will send to the frontend later """
        ticker = self.tickers[int(time.time() % 3)] # Cycle through tickers
        
        # 1. Real Data Fetch
        price_data = yf.Ticker(ticker).history(period="1d", interval="1m").tail(1)
        current_price = price_data['Close'].iloc[0] if not price_data.empty else 0
        
        # 2. Simulated Quantum Logic & Latency
        start = time.perf_counter_ns()
        quantum_signal = "BUY" if (time.time() % 2 > 1) else "SELL" # Dummy quantum flip
        latency = (time.perf_counter_ns() - start) / 1000 # in microseconds
        
        return {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "ticker": ticker,
            "price": round(current_price, 2),
            "signal": quantum_signal,
            "latency_us": round(latency, 2),
            "circuit_breaker": "OK" if self.is_active else "TRIPPED",
            "pnl": f"{self.pnl}%"
        }

    def start_engine(self):
        print("Engine started. Press Ctrl+C to stop.")
        while self.is_active:
            packet = self.get_data_packet()
            print(f"[{packet['timestamp']}] {packet['ticker']} | {packet['signal']} | {packet['latency_us']}μs")
            time.sleep(2) # Refresh every 2 seconds

if __name__ == "__main__":
    engine = MinimalQuantumHFT()
    engine.start_engine()