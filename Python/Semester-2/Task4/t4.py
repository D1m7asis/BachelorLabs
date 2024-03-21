def count_previous_occurrences(text):
    words = text.split()
    occurrences = {}
    result = []
    for word in words:
        if word not in occurrences:
            occurrences[word] = 0
        result.append(occurrences[word])
        occurrences[word] += 1
    return result


def main():
    input_string = input("Введите строку текста: ")
    counts = count_previous_occurrences(input_string)
    print("Результат:", ' '.join(map(str, counts)))


if __name__ == "__main__":
    main()
