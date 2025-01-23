def bad_character_heuristic(pattern: str) -> dict:
    # Инициализация словаря для хранения индексов символов в шаблоне
    symbol_indexes = {}

    # Проходим по каждому символу шаблона
    for i in range(len(pattern)):
        # Записываем последний индекс каждого символа в словарь
        symbol_indexes[pattern[i]] = i

    return symbol_indexes


def get_substring_bmbc(text: str, pattern: str) -> list:
    # Вычисляем худший символ (Bad Character Heuristic) для шаблона
    symbol_indexes = bad_character_heuristic(pattern)

    result = []  # Список для хранения найденных позиций
    shift = 0  # Текущий сдвиг по тексту

    # Пока текущий сдвиг позволяет разместить шаблон в тексте
    while shift <= (len(text) - len(pattern)):
        current_index = len(pattern) - 1  # Начинаем сравнение с конца шаблона

        # Сравниваем символы с конца шаблона к началу
        while current_index >= 0 and pattern[current_index] == text[shift + current_index]:
            current_index -= 1

        # Если все символы совпали (current_index стал -1), нашли вхождение
        if current_index == -1:
            # Добавляем позицию начала вхождения в результат
            result.append(shift)

            # Определяем сдвиг для следующего сравнения
            if shift + len(pattern) < len(text):
                # Используем Bad Character Heuristic для определения сдвига
                indent = len(pattern) - symbol_indexes.get(text[shift + len(pattern)], 0)
            else:
                indent = 1

            # Увеличиваем сдвиг на вычисленное значение
            shift += indent
        else:
            # Если символы не совпадают, используем Bad Character Heuristic для сдвига
            # Определяем сдвиг на основе худшего символа
            indent = symbol_indexes.get(text[shift + current_index], -1)

            # Увеличиваем сдвиг на максимальное значение из 1 и (текущий индекс - индекс символа)
            shift += max(1, current_index - indent)

    return result


if __name__ == '__main__':
    text = "abracadabra"
    pattern = "abra"

    # Выполняем поиск подстроки с использованием алгоритма Бойера-Мура с использованием худшего символа (BMBC)
    matches = get_substring_bmbc(text, pattern)

    # Выводим найденные позиции
    print("Найденные совпадения:")
    for match in matches:
        print(f"Позиция {match}: {text[match:match + len(pattern)]}")
