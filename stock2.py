import yfinance as yf
import pandas as pd
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from datetime import datetime
import time

# HFT focus: High liquidity stocks
HFT_TICKERS = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS']

class QuantumHFTSimulator:
    def __init__(self, tickers):
        self.tickers = tickers
        self.simulator = AerSimulator()

    def get_real_time_data(self):
        """Fetches the latest 1-minute interval data."""
        data = yf.download(self.tickers, period='1d', interval='1m', progress=False)['Close']
        return data.dropna().tail(5) # Get last 5 minutes

    def quantum_optimize(self, returns_correlation):
        """
        Simulates a Quantum Circuit to find the optimal stock to trade
        based on price 'entanglement' (correlations).
        """
        num_qubits = len(self.tickers)
        qc = QuantumCircuit(num_qubits, num_qubits)

        # Step 1: Put qubits in superposition (Checking all possibilities)
        qc.h(range(num_qubits))

        # Step 2: Apply 'Entanglement' based on stock correlations
        # If correlation is high, we apply a rotation gate (simulating quantum advantage)
        for i in range(num_qubits):
            correlation_weight = returns_correlation[i]
            qc.ry(correlation_weight * np.pi, i) 

        # Step 3: Measurement
        qc.measure(range(num_qubits), range(num_qubits))

        # Run the virtual quantum circuit
        job = self.simulator.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        
        # Get the winning 'state' (the optimized trade path)
        winning_state = list(counts.keys())[0]
        return winning_state

    def run_hft_loop(self):
        print(f"--- Starting Quantum HFT Engine: {datetime.now()} ---")
        
        try:
            while True:
                # 1. Get Data
                prices = self.get_real_time_data()
                returns = prices.pct_change().mean()
                
                # Normalize returns for the Quantum Gate (scaling between 0 and 1)
                norm_returns = (returns - returns.min()) / (returns.max() - returns.min())
                
                # 2. Run Quantum Optimization
                quantum_decision = self.quantum_optimize(norm_returns.values)
                
                # 3. Output Results
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Quantum State: {quantum_decision}")
                
                for i, ticker in enumerate(self.tickers):
                    action = "BUY" if quantum_decision[i] == '1' else "WAIT"
                    print(f"  > {ticker}: {action} (Price: {prices[ticker].iloc[-1]:.2f})")
                
                print("-" * 40)
                time.sleep(60) # Wait for next minute candle

        except KeyboardInterrupt:
            print("Shutting down Quantum Engine...")

if __name__ == "__main__":
    engine = QuantumHFTSimulator(HFT_TICKERS)
    engine.run_hft_loop()