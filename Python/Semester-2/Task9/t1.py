import numpy as np


def work():
    total_sum = np.sum(matrix)
    max_element = np.max(matrix)
    min_element = np.min(matrix)
    print(total_sum)
    print(max_element)
    print(min_element)


if __name__ == '__main__':
    matrix = np.loadtxt('t1_data.txt', delimiter=',')

    work()
