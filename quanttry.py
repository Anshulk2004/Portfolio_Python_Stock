import yfinance as yf
import numpy as np
import time
import warnings
from datetime import datetime

# Silence noisy scipy warnings
from scipy.sparse import SparseEfficiencyWarning
warnings.simplefilter('ignore', SparseEfficiencyWarning)

from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler as Sampler
from qiskit_finance.applications.optimization import PortfolioOptimization
from qiskit_optimization.algorithms import MinimumEigenOptimizer

class QuantumPortfolioEngine:
    def __init__(self):
        # Reduced to 4 tickers for a fast first test (Change back to 10 once verified)
        self.tickers = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS']

    def fetch_market_data(self):
        print(f"--- Fetching data for {len(self.tickers)} assets ---")
        data = yf.download(self.tickers, period="3mo", interval="1d", progress=False)['Close']
        returns = data.pct_change().dropna()
        return returns.mean().values, returns.cov().values

    def solve_quantum_allocation(self, avg_returns, cov_matrix):
        print("--- Starting Quantum Optimization (Check your CPU usage!) ---")
        
        portfolio = PortfolioOptimization(
            expected_returns=avg_returns, 
            covariances=cov_matrix, 
            risk_factor=0.5, 
            budget=2 # Selecting 2 best out of 4
        )
        qp = portfolio.to_quadratic_program()
        
        # Callback to see progress
        def callback(eval_count, parameters, mean, std):
            if eval_count % 5 == 0:
                print(f"  Iteration {eval_count}: Energy Mean = {mean:.4f}")

        sampler = Sampler()
        optimizer = COBYLA(maxiter=100) # Limit iterations for speed
        qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=1, callback=callback)
        
        quantum_solver = MinimumEigenOptimizer(qaoa)
        
        start_time = time.perf_counter()
        result = quantum_solver.solve(qp)
        end_time = time.perf_counter()
        
        return result, (end_time - start_time) * 1000

    def run(self):
        try:
            mu, sigma = self.fetch_market_data()
            result, latency = self.solve_quantum_allocation(mu, sigma)
            
            chosen = [self.tickers[i] for i, val in enumerate(result.x) if val > 0.5]
            
            print("\n" + "="*40)
            print(f"🚀 SUCCESS AT {datetime.now().strftime('%H:%M:%S')}")
            print(f"Selected Assets: {chosen}")
            print(f"Total Time: {latency/1000:.2f} seconds")
            print("="*40)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    QuantumPortfolioEngine().run()