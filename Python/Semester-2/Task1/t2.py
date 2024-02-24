def print_ladder(i):
    for j in range(i, 0, -1):
        s = ''
        for k in range(1, j + 1):
            s += str(k)
        print(s)


def print_pyramid(i):
    for j in range(i, 0, -1):
        s = ''
        s += ' ' * (i - j)
        for k in range(j, 1, -1):
            s += str(k)
        for k in range(1, j + 1):
            s += str(k)

        print(s)


def print_inverted_pyramid(n):
    max_width = 2 * n - 1
    for i in range(n, 0, -1):
        numbers = ''.join(str(j) for j in range(i, 0, -1)) + ''.join(str(j) for j in range(2, i + 1))
        print(numbers.center(max_width*2 - 1))


if __name__ == '__main__':
    print_ladder(5)  # 2.1
    print('')
    print_pyramid(3)  # 2.2
    print('')
    print_inverted_pyramid(22)  # 2.3
