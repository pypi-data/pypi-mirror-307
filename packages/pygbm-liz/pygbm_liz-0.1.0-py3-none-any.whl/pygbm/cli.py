# pygbm/cli.py

import argparse
from .gbm_simulator import GBMSimulator

def main():
    parser = argparse.ArgumentParser(description="Simulate Geometric Brownian Motion")
    parser.add_argument("--y0", type=float, default=1.0, help="Initial value Y(0)")
    parser.add_argument("--mu", type=float, default=0.05, help="Drift coefficient")
    parser.add_argument("--sigma", type=float, default=0.2, help="Diffusion coefficient")
    parser.add_argument("--T", type=float, default=1.0, help="Total time")
    parser.add_argument("--N", type=int, default=100, help="Number of steps")

    args = parser.parse_args()

    # Run the GBM simulator
    simulator = GBMSimulator(args.y0, args.mu, args.sigma)
    t_values, y_values = simulator.simulate_path(args.T, args.N)

    # Optionally, you could save or plot the results here
    print("Simulation complete. First few values:")
    print(t_values[:5], y_values[:5])

if __name__ == "__main__":
    main()
