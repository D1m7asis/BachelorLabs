import numpy as np


if __name__ == '__main__':
    arr = np.array([0, 1, 2, 0, 0, 4, 0, 6, 9])
    res = np.nonzero(arr)[0]
    print(res)
