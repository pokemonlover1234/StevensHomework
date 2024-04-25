import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from tqdm import trange

colors = ['red', 'green', 'blue', 'orange', 'yellow', 'purple']

class EM():
    # initialize. Set unknown params to empty arrays to
    # be initialized later.
    def __init__(self, X, k, nIter):
        self.n = X.shape[0]
        self.f = X.shape[1]
        self.k = k
        self.X = X
        self.w = np.matrix(np.empty((self.n, self.k)))
        self.pi = np.empty((1, self.k))
        self.mu = np.matrix(np.empty((self.k, self.f)))
        self.sigma = np.array(np.empty((self.f, self.f, self.k)))
        self.random = np.random.default_rng(13514890984)
        self.nIter = nIter
        self.init_vars()

    def init_vars(self):
        # Initialize variables with values pulled
        # from base dataset
        # Initialized with idea of starting with an E-step,
        # So init pi, mu, sigma.
        # Pi initialized randomly, mu, sigma from dataset
        # Sum of pi is 1
        self.pi = self.random.dirichlet(np.ones(self.k), size=1)
        # mu initialized by choosing k random points as means
        self.mu = self.random.permutation(self.X, axis=0)[:self.k]
        # sigma initialized as whole data covariance matrix for each
        for k in range(self.k):
            self.sigma[:,:,k] = np.cov(self.X, rowvar=False)

    # Helper function to get gaussian density of kth 
    # mixture component
    def mixture_density(self, x, k):
        x_minus_mean = np.matrix(x - self.mu[k, :])
        den = math.pow(2 * math.pi, self.f / 2) * math.sqrt(np.linalg.det(self.sigma[:, :, k]))
        num = math.exp(-1/2 * (np.matmul(np.matmul(x_minus_mean, np.linalg.inv(self.sigma[:, :, k])), x_minus_mean.T)))
        return num / den
    
    # Get total membership weights. 
    # Optimizes getting weights so the denominator
    # doesn't have to be calculated for each x every time,
    # when the denominator is the same for all x when in 
    # each class
    def total_memb_weight(self, x):
        weight = 0
        for k in range(self.k):
            weight += self.mixture_density(x, k) * self.pi[0, k]
        return weight

    # Get the membership weight of x in component k
    # used for expectation step
    def membership_weight(self, x, k, totweight):
        num = self.mixture_density(x, k) * self.pi[0, k]
        return num / totweight

    # Perform an E-step
    # Confirmed via testing that all weight
    # rows sum to 1, so I believe the implementations
    # of functions that this depends on are correct.
    # (barring floating point rounding errors)
    def expectation_step(self):
        for i in range(self.n):
            totweight = self.total_memb_weight(self.X[i, :])
            for k in range(self.k):
                self.w[i, k] = self.membership_weight(self.X[i, :], k, totweight)
    
    # Gets N_k, the effective number of data points assigned to component k
    def N_k(self, k):
        return np.sum(self.w[:, k])

    # Mean likelihood maximization step of M step
    def maximize_means(self):
        for k in range(self.k):
            self.mu[k] = 1 / self.N_k(k) * np.sum(np.multiply(np.repeat(self.w[:, k], 2, axis=1), self.X), axis=0)

    # Maximizes likelihood of covariances
    # By time this is run, means are already
    # updated.
    def maximize_cov(self):
        for k in range(self.k):
            new_sigma = np.zeros((self.f, self.f))
            for i in range(self.n):
                x_minus_mean = np.matrix(self.X[i, :] - self.mu[k, :])
                new_sigma += self.w[i, k] * np.matmul(x_minus_mean.T, x_minus_mean)
            self.sigma[:, :, k] = 1 / self.N_k(k) * new_sigma
    
    # Maximizes likelihood of mixture weights
    def maximize_weights(self):
        for k in range(self.k):
            self.pi[0, k] = self.N_k(k) / self.n

    # Perform an M-step
    def maximization_step(self):
        self.maximize_means()
        self.maximize_cov()
        self.maximize_weights()

    # Determines log-likelihood
    def log_likelihood(self):
        likelihood = 0
        for i in range(self.n):
            partial_sum = 0
            for k in range(self.k):
                partial_sum += self.pi[0, k] * self.mixture_density(self.X[i, :], k)
            likelihood += math.log(partial_sum)
        return likelihood
    
    # Run an iteration
    def run_iteration(self):
        self.expectation_step()
        self.maximization_step()

    # Run all iterations
    def run_to_completion(self):
        for i in trange(self.nIter):
            self.run_iteration()

    # Get point assignment, as k value
    # of assigned component.
    def get_assignment(self, x):
        return np.argmax([
            self.mixture_density(x, k) for k in range(self.k)
        ])

    def get_colors(self):
        return [colors[self.get_assignment(x)] for x in self.X]
    
    # Display a graph of the model
    # Assumes each xi has two components
    def show_plot(self):
        def draw_ellipse(pos, cov, ax, **kwargs):
            U, s, Vt = np.linalg.svd(cov)
            angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
            width, height = 2 * np.sqrt(s)
            for nsig in range(1, 4):
                ax.add_patch(Ellipse(pos, nsig * width, nsig * height, angle, **kwargs))
        c = self.get_colors()
        ax = plt.gca()
        ax.scatter(self.X[:, 0], self.X[:, 1], s=40, zorder=2, c=c, cmap='viridis')
        ax.axis('equal')
        w_factor = 0.2 / self.pi.max()
        for k in range(self.k):
            draw_ellipse(self.mu[k, :], self.sigma[:, :, k], ax, alpha=self.pi[0, k] * w_factor)
        plt.show()