import numpy as np


if __name__ == '__main__':
    data = np.random.randn(10, 4)

    _min = np.min(data)
    _max = np.max(data)
    _mean = np.mean(data)
    _std = np.std(data)

    first_five_rows = data[:5, :]

    print(_min, _max, _mean, _std, first_five_rows)
