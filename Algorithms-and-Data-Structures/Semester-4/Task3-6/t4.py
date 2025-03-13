def find_borders(pattern: str) -> list:
    """
    Вычисляет префикс-функцию (границы) для шаблона.

    Префикс-функция для каждой позиции i показывает длину наибольшего собственного префикса,
    который одновременно является суффиксом подстроки pattern[0:i+1].

    Аргументы:
      pattern: Строка, для которой вычисляется префикс-функция.

    Возвращает:
      Список значений префикс-функции для каждого индекса в pattern.
    """
    borders = [0] * len(pattern)
    current_index = 0  # Длина текущего совпадающего префикса

    # Проходим по шаблону, начиная с 1-го символа (0-й элемент всегда 0)
    for i in range(1, len(pattern)):
        # Если символы не совпадают, возвращаемся к предыдущей границе
        while current_index > 0 and pattern[current_index] != pattern[i]:
            current_index = borders[current_index - 1]

        # Если символы совпадают, увеличиваем текущий индекс
        if pattern[current_index] == pattern[i]:
            current_index += 1

        borders[i] = current_index

    return borders


def get_substring_kmp(text: str, pattern: str) -> list:
    """
    Реализует поиск всех вхождений подстроки (pattern) в тексте (text) с использованием алгоритма KMP.

    Аргументы:
      text: Строка, в которой производится поиск.
      pattern: Шаблон для поиска.

    Возвращает:
      Список позиций начала вхождений шаблона в тексте.
    """
    if not pattern:
        return []  # Если шаблон пустой, можно вернуть пустой список или обработать как специальный случай

    # Вычисляем префикс-функцию для шаблона
    borders = find_borders(pattern)

    result = []  # Список для хранения индексов начала совпадений
    compare_index = 0  # Текущий индекс в шаблоне, с которым сравниваем символ текста

    # Проходим по каждому символу текста
    for i in range(len(text)):
        # Если символы не совпадают, возвращаемся к предыдущей границе
        while compare_index > 0 and text[i] != pattern[compare_index]:
            compare_index = borders[compare_index - 1]

        # Если символы совпадают, переходим к следующему символу шаблона
        if text[i] == pattern[compare_index]:
            compare_index += 1

        # Если весь шаблон совпал, сохраняем позицию начала вхождения
        if compare_index == len(pattern):
            result.append(i - compare_index + 1)
            # Обновляем индекс шаблона для продолжения поиска
            compare_index = borders[compare_index - 1] if compare_index > 0 else 0

    return result


if __name__ == '__main__':
    text = "abracadabra"
    pattern = "abra"

    # Поиск подстроки с использованием алгоритма Кнута-Морриса-Пратта (KMP)
    matches = get_substring_kmp(text, pattern)

    # Вывод результатов поиска
    print("Найденные совпадения:")
    for match in matches:
        print(f"Позиция {match}: {text[match:match + len(pattern)]}")
