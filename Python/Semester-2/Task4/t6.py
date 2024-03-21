def count_words(text):
    words = text.split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count


def print_sorted_words(word_count):
    sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_words:
        print(word)


def main():
    input_text = input("Введите текст: ")
    word_count = count_words(input_text)
    print_sorted_words(word_count)


if __name__ == "__main__":
    main()
