from farmgbm12.GeometricBrownian import pygbm

y0 =1.0
mu = 0.05
sigma = 0.2
T = 1.0
N = 100


simulator = pygbm(y0, mu, sigma, T, N)

simulator.simulate()
simulator.plot()
