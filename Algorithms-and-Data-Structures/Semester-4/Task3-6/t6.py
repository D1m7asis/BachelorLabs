def get_substring_rk(text: str, pattern: str) -> list:
    """
    Реализует алгоритм Рабина-Карпа для поиска всех вхождений шаблона в текст.
    Алгоритм использует хэширование с последующим пересчетом хэша за O(1).

    Аргументы:
      text: Строка, в которой производится поиск.
      pattern: Шаблон для поиска.

    Возвращает:
      Список позиций начала вхождений шаблона в тексте.
    """
    result = []

    # База для хэширования (обычно равна количеству символов в алфавите)
    alphabet_size = 256
    # Простое число для вычисления модуля (для уменьшения коллизий)
    mod = 9973

    n = len(text)
    m = len(pattern)

    if m > n:
        return result

    pattern_hash = 0
    text_hash = 0
    first_index_hash = 1  # Значение (alphabet_size^(m-1)) % mod для удаления старшего символа

    # Вычисляем значение first_index_hash
    for i in range(m - 1):
        first_index_hash = (first_index_hash * alphabet_size) % mod

    # Вычисляем начальный хэш для шаблона и первого окна текста
    for i in range(m):
        pattern_hash = (pattern_hash * alphabet_size + ord(pattern[i])) % mod
        text_hash = (text_hash * alphabet_size + ord(text[i])) % mod

    # Проходим по всем возможным окнам текста
    for i in range(n - m + 1):
        # Если хэши совпадают, выполняем посимвольное сравнение для проверки
        if pattern_hash == text_hash and compare_text(text, i, pattern):
            result.append(i)

        # Если окно не последнее, пересчитываем хэш для следующего окна
        if i < n - m:
            text_hash = (alphabet_size * (text_hash - ord(text[i]) * first_index_hash) + ord(text[i + m])) % mod
            # Обеспечиваем, чтобы хэш был неотрицательным
            if text_hash < 0:
                text_hash += mod

    return result


def compare_text(text: str, index: int, pattern: str) -> bool:
    """
    Посимвольно сравнивает подстроку текста, начиная с index, с шаблоном.
    Возвращает True, если они совпадают, иначе False.
    """
    for i in range(len(pattern)):
        if text[index + i] != pattern[i]:
            return False
    return True


if __name__ == '__main__':
    text = "abracadabra"
    pattern = "abr"

    # Поиск подстроки с использованием алгоритма Рабина-Карпа
    matches = get_substring_rk(text, pattern)

    # Вывод найденных позиций и совпадающих подстрок
    print("Найденные совпадения:")
    for match in matches:
        print(f"Позиция {match}: {text[match:match + len(pattern)]}")
