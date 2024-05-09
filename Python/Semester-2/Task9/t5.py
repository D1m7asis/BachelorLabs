import numpy as np
from scipy.linalg import cholesky, solve_triangular
from scipy.stats import multivariate_normal
import time


def log_pdf_multivariate_normal(matrix, math_wait, covar_matrix):
    N, D = matrix.shape
    diff = matrix - math_wait

    # Вычисление обратной матрицы ковариации
    L = cholesky(covar_matrix, lower=True)
    Linv = solve_triangular(L, np.eye(D), lower=True)
    C_inv = Linv.T @ Linv
    # Вычисление логарифма определителя ковариационной матрицы
    log_det = -2 * np.sum(np.log(np.diag(L)))
    # Вычисление логарифма плотности вероятности
    log_density = -0.5 * (np.sum(diff @ C_inv * diff, axis=1) + log_det + D * np.log(2 * np.pi))
    return log_density


if __name__ == '__main__':
    m = np.array([0, 0])
    C = np.array([[1, 0.5], [0.5, 2]])
    X = np.random.randn(1000, 2)

    start_time = time.time()
    log_density_custom = log_pdf_multivariate_normal(X, m, C)
    custom_duration = time.time() - start_time

    start_time = time.time()
    log_density_scipy = multivariate_normal(m, C).logpdf(X)
    scipy_duration = time.time() - start_time

    print("Максимальная абсолютная разница между логарифмами плотностей вероятности:",
          np.max(np.abs(log_density_custom - log_density_scipy)))

    print("Время выполнения нашей функции:", custom_duration)
    print("Время выполнения scipy.stats.multivariate_normal.logpdf():", scipy_duration)
