import numpy as np

class pygbm:

    def __init__(self, y0, mu, sigma, T, N, seed=2):
        self.y0 = y0
        self.mu = mu
        self.sigma = sigma
        self.T = T
        self.N = N
        self.seed = seed
    
    def simulate(self):
        np.random.seed(self.seed)
        dt = self.T / self.N
        dW = np.random.normal(0, np.sqrt(dt), self.N)
        W = np.cumsum(dW)
        t = np.linspace(0, self.T, self.N)
        y = self.y0 * np.exp((self.mu - 0.5 * self.sigma ** 2) * t + self.sigma * W)
        return y
    
    def plot(self):
        import matplotlib.pyplot as plt

        plt.plot(self.simulate())
        plt.title('Geometric Brownian Motion')
        plt.xlabel('steps')
        plt.ylabel('Value')
        plt.show()