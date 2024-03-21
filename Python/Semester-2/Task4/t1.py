def count_unique_numbers(numbers):
    unique_numbers = set(numbers)
    return len(unique_numbers)


def main():
    input_str = input("Введите список чисел через запятую: ")
    numbers = [int(x.strip()) for x in input_str.split(',')]
    unique_count = count_unique_numbers(numbers)
    print("Количество различных чисел в списке:", unique_count)


if __name__ == "__main__":
    main()
