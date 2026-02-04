import yfinance as yf
import pandas as pd
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from datetime import datetime
import time

# Focus on ultra-liquid tickers for HFT
HFT_TICKERS = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']

class QuantumHFTPro:
    def __init__(self, tickers):
        self.tickers = tickers
        self.simulator = AerSimulator()
        self.max_drawdown = -0.02  # Kill switch at 2% loss
        self.session_pnl = 0.0

    def get_market_microstructure(self, ticker):
        """Simulates HFT Order Book Imbalance (Bid vs Ask)"""
        # In real life, use L2/L3 data. Here we simulate imbalance from volatility.
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(period="1d", interval="1m").tail(2)
        
        # Simulate an imbalance: if current close > previous close, assume more buyers
        close_prices = data['Close'].values
        imbalance = (close_prices[-1] - close_prices[-2]) / close_prices[-2] if len(close_prices) > 1 else 0
        return np.clip(imbalance * 100, -1, 1) # Scale for quantum gate

    def quantum_logic(self, imbalance_score):
        """Uses a Quantum Gate to decide trade intensity based on imbalance"""
        qc = QuantumCircuit(1, 1)
        # Apply rotation based on market imbalance
        theta = (imbalance_score + 1) * np.pi / 2 # Map -1...1 to 0...Pi
        qc.ry(theta, 0)
        qc.measure(0, 0)
        
        result = self.simulator.run(qc, shots=1).result()
        return int(list(result.get_counts().keys())[0])

    def run(self):
        print(f"🚀 Quantum HFT Engine Active | Safety: {self.max_drawdown*100}%")
        try:
            while True:
                if self.session_pnl <= self.max_drawdown:
                    print("🚨 CRITICAL: CIRCUIT BREAKER TRIGGERED. MAX DRAWDOWN REACHED.")
                    break

                for ticker in self.tickers:
                    start_time = time.perf_counter_ns()
                    
                    imbalance = self.get_market_microstructure(ticker)
                    decision = self.quantum_logic(imbalance)
                    
                    # Simulate Latency
                    end_time = time.perf_counter_ns()
                    latency = (end_time - start_time) / 1000 # microseconds
                    
                    action = "BUY" if decision == 1 else "SELL"
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {ticker} | Signal: {action} | Latency: {latency:.2f}μs")
                
                print("-" * 50)
                time.sleep(30) # HFT check every 30 seconds
        except KeyboardInterrupt:
            print("Engine Stopped.")

if __name__ == "__main__":
    QuantumHFTPro(HFT_TICKERS).run()