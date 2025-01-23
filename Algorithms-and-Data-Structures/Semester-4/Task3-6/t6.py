def get_substring_rk(text: str, pattern: str) -> list:
    # Инициализация результата
    result = []

    # Константы для хэширования
    alphabet_size = 256
    mod = 9973

    # Если длина шаблона больше длины текста, возвращаем пустой результат
    if len(pattern) > len(text):
        return result

    # Вычисляем начальные значения хэша для шаблона и текста
    pattern_hash = ord(pattern[0]) % mod
    text_hash = ord(text[0]) % mod
    first_index_hash = 1

    # Вычисляем хэш для шаблона и начальной части текста
    for i in range(1, len(pattern)):
        pattern_hash = (pattern_hash * alphabet_size + ord(pattern[i])) % mod
        text_hash = (text_hash * alphabet_size + ord(text[i])) % mod
        first_index_hash = (first_index_hash * alphabet_size) % mod

    # Проверяем совпадения в тексте
    for i in range(len(text) - len(pattern) + 1):
        # Если хэши совпадают и строки также совпадают, добавляем индекс в результат
        if pattern_hash == text_hash and compare_text(text, i, pattern):
            result.append(i)

        # Обновляем хэш для следующего окна
        if i < len(text) - len(pattern):
            text_hash = (alphabet_size * (text_hash - ord(text[i]) * first_index_hash) + ord(
                text[i + len(pattern)])) % mod

            # Если хэш стал отрицательным, корректируем его
            if text_hash < 0:
                text_hash += mod

    return result


def compare_text(text: str, index: int, pattern: str) -> bool:
    # Сравниваем подстроку текста с шаблоном посимвольно
    for i in range(len(pattern)):
        if pattern[i] != text[index + i]:
            return False
    return True


if __name__ == '__main__':
    text = "abracadabra"
    pattern = "abr"

    # Выполняем поиск подстроки с использованием алгоритма Рабина-Карпа
    matches = get_substring_rk(text, pattern)

    # Выводим найденные позиции
    print("Найденные совпадения:")
    for match in matches:
        print(f"Позиция {match}: {text[match:match + len(pattern)]}")
