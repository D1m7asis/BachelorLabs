import numpy as np


if __name__ == '__main__':
    arr = np.arange(16).reshape(4, 4)
    print(arr)
    arr[[1, 3]] = arr[[3, 1]]
    print(arr)
