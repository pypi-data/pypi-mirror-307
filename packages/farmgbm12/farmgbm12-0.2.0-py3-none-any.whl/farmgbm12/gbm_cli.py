import argparse
from farmgbm12.GeometricBrownian import pygbm
import matplotlib.pyplot as plt

def main():
    # Step 1: Parse command-line arguments
    parser = argparse.ArgumentParser(description="Simulate Geometric Brownian Motion (GBM) paths")
    parser.add_argument("--y0", type=float, required=True, help="Initial value of Y0")
    parser.add_argument("--mu", type=float, required=True, help="Drift coefficient (mu)")
    parser.add_argument("--sigma", type=float, required=True, help="Diffusion coefficient (sigma)")
    parser.add_argument("--T", type=float, required=True, help="Time horizon (T)")
    parser.add_argument("--N", type=int, required=True, help="Number of Timesteps (N)")

    args = parser.parse_args()

    simulator = pygbm(args.y0, args.mu, args.sigma, args.T, args.N)
    simulator.simulate()
    simulator.plot()


if __name__ == "__main__":
    main()




