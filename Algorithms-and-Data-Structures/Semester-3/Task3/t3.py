def find_numbers(num):
    result = set()

    K = 0
    while (3 ** K) <= num:
        L = 0
        while (3 ** K) * (5 ** L) <= num:
            M = 0
            while (3 ** K) * (5 ** L) * (7 ** M) <= num:
                result.add((3 ** K) * (5 ** L) * (7 ** M))
                M += 1
            L += 1
        K += 1

    result = sorted(result)
    for num in result:
        print(num)


if __name__ == '__main__':
    x = int(input("Введите число x: "))
    find_numbers(x)
