import numpy as np
import matplotlib.pyplot as plt

class Stochastic_Processes:
    """
    Creates an object that undergoes a 1D stochastic process (Brownian motion).

    Args:
         y0 (float): starting point of the object at t=0.
    """
    def __init__ (self, y0):

        self.y0 = y0
    

    def brownian_motion (self, T, N):
        """
        Calculates the Brownian motion random walk over.

        Args:
            T (float): Time scale of the Brownian motion.
            N (int): Number of time steps.

        Returns:
            t (np.array): Timesteps in array format.
            B_t (np.array): Brownian motion displacement in arrary format for corresponding timesteps.
        """

        dt = T/N 
        t = np.linspace (0, T, N+1)
        dB = np.random.normal(0, np.sqrt(dt), N)
        B_t = np.concatenate(([0], np.cumsum(dB)))

        return t, B_t 
    
    def plot (self, t, Y_t):
        """
        Plots a graph of the Brownian motion displacement (y-axis) with the corresponding time-steps.
        Saves plot in folder.

        Args:
            t (np.array): Timesteps in array format.
            Y_t (np.array): Brownian motion displacement in arrary format for corresponding timesteps.
        """

        plt.plot (t, Y_t)
        plt.xlabel ('Time, t')
        plt.ylabel ('Displacement, Y_t')
        plt.savefig('fig.png')
        print('Figure saved in current folder.')

class GBMSimulator (Stochastic_Processes):
    """
    Produces an object undergoing geometric Brownian motion.

    Args:
        y0 (float): Starting point of the object at t=0.
        mu (float): Mean of GBM.
        sigma (float): Standard deviation of GBM.
    """
    def __init__ (self, y0, mu, sigma):

        super().__init__(y0)
        self.mu = mu
        self.sigma = sigma 

    def simulate_path (self, T, N):
        """
        Simulates 1D GBM and plots a graph. Saves plot in folder.

        Args:
            T (float): Time scale of the Brownian motion.
            N (int): Number of time steps

        Returns:
            t (np.array): Timesteps in array format.
            Y_t (np.array): Brownian motion displacement in arrary format for corresponding timesteps.
        """
        t, B_t = self.brownian_motion (T, N)
        Y_t = self.y0 * np.exp((self.mu-0.5*(self.sigma**2))*t + self.sigma * B_t)
        self.plot(t, Y_t)
        return t, Y_t
    

