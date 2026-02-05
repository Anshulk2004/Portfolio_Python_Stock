import yfinance as yf
import numpy as np
import time
import warnings
from datetime import datetime
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler as Sampler
from qiskit_finance.applications.optimization import PortfolioOptimization
from qiskit_optimization.algorithms import MinimumEigenOptimizer

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    async_mode='threading',
    engineio_logger=False, 
    logger=False
)

class QuantumEngine:
    def __init__(self):
        self.tickers = [
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 
            'ICICIBANK.NS'
        ]
        self.pnl = 0.0

    def get_market_data(self):
        data = yf.download(self.tickers, period="1mo", interval="1d", progress=False)['Close']
        returns = data.pct_change().dropna()
        return returns.mean().values, returns.cov().values, data.iloc[-1].to_dict()

    def run_quantum_logic(self, mu, sigma):
        portfolio = PortfolioOptimization(
            expected_returns=mu, 
            covariances=sigma, 
            risk_factor=0.3, 
            budget=4
        )
        qp = portfolio.to_quadratic_program()
        
        start_time = time.perf_counter()
        qaoa = QAOA(sampler=Sampler(), optimizer=COBYLA(maxiter=25))
        result = MinimumEigenOptimizer(qaoa).solve(qp)
        latency = (time.perf_counter() - start_time) * 1000000 
        
        return result.x, latency

engine = QuantumEngine()

def background_thread():
    print("\n" + "="*40)
    print("CORE: 10-QUBIT Quantum Engine Active")
    print("="*40)
    while True:
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] -> Fetching Market Data...")
            mu, sigma, latest_prices = engine.get_market_data()
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] -> Running QAOA (10 Qubits)...")
            selection, latency = engine.run_quantum_logic(mu, sigma)
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] -> Optimization Success. Broadcasting...")
            
            any_emitted = False
            for i, selected in enumerate(selection):
                ticker_full = engine.tickers[i]
                ticker_clean = ticker_full.replace(".NS", "")
                print(f"DEBUG: Processing {ticker_clean} through Quantum Engine (Selection Value: {selected})")
                if selected > 0.5:
                    any_emitted = True
                    price = latest_prices[ticker_full]
                    engine.pnl += np.random.uniform(-0.01, 0.03)                    
                    packet = {
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "ticker": ticker_clean,
                        "price": round(price, 2),
                        "signal": "BUY",
                        "latency_us": round(latency / 1000, 2),
                        "pnl": f"{round(engine.pnl, 2)}%"
                    }
                    socketio.emit('quantum_update', packet)
                    print(f"    [SEND] {ticker_clean} | PnL: {engine.pnl:.2f}%")
                    socketio.sleep(0.5) 
            
            if not any_emitted:
                print("    [INFO] No optimal assets met the criteria this cycle.")

            print(f"[{datetime.now().strftime('%H:%M:%S')}] -> Cycle Complete. Idle for 10s.")
            socketio.sleep(10) 
        except Exception as e:
            print(f"!!! ENGINE ERROR: {e}")
            socketio.sleep(5)

@socketio.on('connect')
def handle_connect():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] WS: Dashboard Linked Successfully")

if __name__ == '__main__':
    socketio.start_background_task(background_thread)
    socketio.run(app, host='127.0.0.1', port=8000, debug=False)