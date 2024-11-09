import numpy as np

class GBMSimulator:

    def __init__(self):
        pass
        '''
        Initialises Instance of GBMSimulator class
        '''

    def simulate(self, mu,n,T, M, y0, sigma):


        """
        Simulate geometric Brownian motion for given parameters.

        :param mu: Drift coefficient.
        :type mu: int
        :param n: Number of time steps.
        :type n: int
        :param T: Total time in years.
        :type T: int
        :param M: Number of simulation paths.
        :type M: int
        :param y0: Initial value.
        :type y0: int
        :param sigma: Volatility of the process.
        :type sigma: int
        :return: Simulated paths, with shape (n + 1, M).
        :rtype: numpy.ndarray

        :Example:

        >>> simulator = GBMSimulator()
        >>> paths = simulator.simulate(mu=0.1, n=1000, T=1, M=10, y0=100, sigma=0.2)
        >>> paths.shape
        (1001, 10)
        """



        # calculate each time step
        dt = T/n        

        # simulate using numpy array
        st = np.exp(    
            (mu - sigma**2 / 2) * dt
                                    + sigma*np.random.normal(0, np.sqrt(dt), size=(M,n)).T
                                )

        # include array of 1's
        st = np.vstack([np.ones(M), st])

        st = y0 * st.cumprod(axis=0)

        return st

