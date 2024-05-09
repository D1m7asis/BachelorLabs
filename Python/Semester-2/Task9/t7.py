import numpy as np


if __name__ == '__main__':
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    iris = np.genfromtxt(url, delimiter=',', dtype='object')

    species_column = iris[:, -1]
    unique, count = np.unique(species_column, return_counts=True)
    print(unique, count)
