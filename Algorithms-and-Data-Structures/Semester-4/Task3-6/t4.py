def find_borders(pattern: str) -> list:
    borders = [0] * len(pattern)  # Список границ (prefix function)
    current_index = 0  # Индекс текущей позиции в шаблоне

    # Проходим по всем символам шаблона, начиная с первого символа после начала
    for i in range(1, len(pattern)):
        # Пока текущий индекс больше нуля и символы не совпадают,
        # обновляем текущий индекс на значение из предыдущей границы
        while current_index > 0 and pattern[current_index] != pattern[i]:
            current_index = borders[current_index - 1]

        # Если символы совпадают, увеличиваем текущий индекс
        if pattern[current_index] == pattern[i]:
            current_index += 1

        # Записываем текущий индекс в список границ
        borders[i] = current_index

    return borders


def get_substring_kmp(text: str, pattern: str) -> list:
    # Вычисляем границы для шаблона
    borders = find_borders(pattern)

    result = []  # Список для хранения найденных позиций
    compare_index = 0  # Индекс текущего символа в шаблоне

    # Проходим по каждому символу текста
    for i in range(len(text)):
        # Пока текущий индекс больше нуля и символы не совпадают,
        # обновляем текущий индекс на значение из предыдущей границы
        while compare_index > 0 and text[i] != pattern[compare_index]:
            compare_index = borders[compare_index - 1]

        # Если символы совпадают, увеличиваем текущий индекс
        if text[i] == pattern[compare_index]:
            compare_index += 1

        # Если достигли конца шаблона, значит нашли вхождение
        if compare_index == len(pattern):
            # Добавляем позицию начала вхождения в результат
            result.append(i - compare_index + 1)

            # Обновляем текущий индекс для продолжения поиска
            compare_index = borders[compare_index - 1] if compare_index > 0 else 0

    return result


if __name__ == '__main__':
    text = "abracadabra"
    pattern = "abra"

    # Выполняем поиск подстроки с использованием алгоритма Кнута-Морриса-Пратта (KMP)
    matches = get_substring_kmp(text, pattern)

    # Выводим найденные позиции
    print("Найденные совпадения:")
    for match in matches:
        print(f"Позиция {match}: {text[match:match + len(pattern)]}")
