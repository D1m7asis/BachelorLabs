import numpy as np


if __name__ == '__main__':
    x = np.array([6, 2, 0, 3, 0, 0, 5, 7, 0])

    zeroes = np.where(x == 0)[0]
    zeroes = zeroes[:-1]
    max_after_zero = np.max(x[zeroes + 1])

    print(max_after_zero)
