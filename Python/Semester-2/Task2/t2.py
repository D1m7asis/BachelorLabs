def printSierpinski(n):
    n = 2 ** n
    y = (n - 1)

    while y >= 0:
        i = 0

        while i < y:
            print(" ", end="")
            i += 1

        x = 0

        while x + y < n:
            if (x & y) != 0:
                print(" ", end=" ")
            else:
                print("* ", end="")
            x += 1

        print()
        y -= 1


if __name__ == '__main__':
    n = int(input("Введите ранг треугольника Серпинского: "))
    printSierpinski(n)
