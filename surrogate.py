import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel as C

class GPSurrogate:
    def __init__(self):
        kernel = C(1.0, (1e-3, 1e3)) * Matern(length_scale=1.0, nu=2.5)
        self.model = GaussianProcessRegressor(kernel=kernel, normalize_y=True, n_restarts_optimizer=2)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.model.fit(X, y)

    def predict(self, X: np.ndarray):
        m, s = self.model.predict(X, return_std=True)
        return m, s**2
