import yfinance as yf
import numpy as np
import time
import warnings
from datetime import datetime

# 1. Silence Scipy's "SparseEfficiencyWarning" and others
from scipy.sparse import SparseEfficiencyWarning
warnings.simplefilter('ignore', SparseEfficiencyWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler as Sampler
from qiskit_finance.applications.optimization import PortfolioOptimization
from qiskit_optimization.algorithms import MinimumEigenOptimizer

class QuantumPortfolioEngine:
    def __init__(self):
        # Full 10 Nifty 50 Tickers
        self.tickers = [
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS'
        ]

    def fetch_market_data(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching data for {len(self.tickers)} assets...")
        data = yf.download(self.tickers, period="3mo", interval="1d", progress=False)['Close']
        returns = data.pct_change().dropna()
        return returns.mean().values, returns.cov().values

    def solve_quantum_allocation(self, avg_returns, cov_matrix):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Mapping problem to 10 qubits...")
        
        # risk_factor: balance (0.5), budget: selection size (3)
        portfolio = PortfolioOptimization(
            expected_returns=avg_returns, 
            covariances=cov_matrix, 
            risk_factor=0.5, 
            budget=3 
        )
        qp = portfolio.to_quadratic_program()
        
        # This callback function triggers every time the "Quantum" circuit is measured
        def callback(eval_count, parameters, mean, std):
            # Print every iteration so you know it's alive
            print(f"  > Iteration {eval_count:03}: Energy Mean = {mean:.6f}")

        sampler = Sampler()
        # COBYLA is the classical optimizer tuning the quantum angles
        optimizer = COBYLA(maxiter=150) 
        qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=1, callback=callback)
        
        quantum_solver = MinimumEigenOptimizer(qaoa)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting QAOA loop. Please wait...")
        start_time = time.perf_counter()
        result = quantum_solver.solve(qp)
        end_time = time.perf_counter()
        
        return result, (end_time - start_time) * 1000

    def run(self):
        try:
            mu, sigma = self.fetch_market_data()
            result, latency = self.solve_quantum_allocation(mu, sigma)
            
            # Binary selection: result.x contains 1.0 for chosen stocks
            chosen = [self.tickers[i] for i, val in enumerate(result.x) if val > 0.5]
            
            print("\n" + "="*50)
            print(f"🚀 QUANTUM OPTIMIZATION COMPLETE")
            print("="*50)
            print(f"Time Taken:     {latency/1000:.2f} seconds")
            print(f"Optimal Assets: {chosen}")
            print(f"Solution Value: {result.fval:.6f}")
            print("="*50)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    QuantumPortfolioEngine().run()