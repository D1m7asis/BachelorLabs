def is_subset(set1, set2):
    return set1.issubset(set2)


def main():
    input_str1 = input("Введите элементы первого множества через запятую: ") #1, 2, 3, 4, 5, 6, 7
    input_str2 = input("Введите элементы второго множества через запятую: ") #10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0

    set1 = set(input_str1.split(', '))
    set2 = set(input_str2.split(', '))

    result = is_subset(set1, set2)

    print(result)


if __name__ == "__main__":
    main()
