def amax(a, b, c):
    return a if ((a >= b) & (a >= c)) else b if ((b >= a) & (b >= c)) else c


def amin(a, b, c):
    return a if ((a <= b) & (a <= c)) else b if ((b <= a) & (b <= c)) else c


if __name__ == '__main__':
    print('Введите 3 числа для сравнения: ')
    a = int(input(' '))
    b = int(input(' '))
    c = int(input(' '))

    print('Максимальное и минимальное из них: ' + str(amax(a, b, c)) + ' и ' + str(amin(a, b, c)))


