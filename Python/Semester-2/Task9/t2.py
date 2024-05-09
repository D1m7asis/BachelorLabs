import numpy as np


def run_len_coding(arr):
    frequencies = []
    occurrences = 1
    numbers = []
    num = arr[0]

    for i in range(1, len(arr)):
        if arr[i] == num:
            occurrences += 1
        else:
            numbers.append(num)
            frequencies.append(occurrences)
            num = arr[i]
            occurrences = 1

    numbers.append(num)
    frequencies.append(occurrences)
    return np.array(numbers), np.array(frequencies)


if __name__ == '__main__':
    matrix = np.array([0, 0, 0, 1, 1, 1, 2, 2, 9, 9, 9, 9, 9])
    result = run_len_coding(matrix)
    print(result)
