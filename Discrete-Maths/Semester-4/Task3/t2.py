import itertools


def hamming_distance(a, b):
    """Вычисляет расстояние Хемминга между двумя строками битов."""
    return sum(bit1 != bit2 for bit1, bit2 in zip(a, b))


def generate_codes(min_distance, num_codes, max_length=6):
    """
    Генерирует набор двоичных кодов с заданным минимальным расстоянием Хемминга.

    Args:
        min_distance: минимальное требуемое расстояние Хемминга
        num_codes: необходимое количество кодов
        max_length: максимальная длина кода для поиска

    Returns:
        Список кодов или None, если не удалось найти достаточно кодов
    """
    for code_length in range(3, max_length + 1):
        codes = [''.join(bits) for bits in itertools.product('01', repeat=code_length)]
        valid_codes = []

        # Используем жадный алгоритм для выбора кодов
        while codes and len(valid_codes) < num_codes:
            # Выбираем первый код из оставшихся
            current_code = codes.pop(0)
            valid = True

            # Проверяем расстояние до всех уже выбранных кодов
            for existing in valid_codes:
                if hamming_distance(current_code, existing) < min_distance:
                    valid = False
                    break

            if valid:
                valid_codes.append(current_code)

        if len(valid_codes) >= num_codes:
            return valid_codes[:num_codes]

    return None


def validate_code_set(code_dict, min_distance):
    """Проверяет, что все коды удовлетворяют условию минимального расстояния."""
    chars = list(code_dict.keys())
    for i in range(len(chars)):
        for j in range(i + 1, len(chars)):
            dist = hamming_distance(code_dict[chars[i]], code_dict[chars[j]])
            if dist < min_distance:
                print(f"Ошибка: '{chars[i]}' и '{chars[j]}' имеют расстояние {dist}")
                return False
    print(f"Все коды удовлетворяют минимальному расстоянию {min_distance}")
    return True


def detect_error(code, code_dict):
    """Обнаруживает наличие ошибки в коде."""
    return code not in code_dict.values()


def correct_error(error_code, code_dict):
    """Исправляет ошибку в коде (если возможно)."""
    min_dist = float('inf')
    corrections = []

    for char, code in code_dict.items():
        dist = hamming_distance(error_code, code)
        if dist < min_dist:
            min_dist = dist
            corrections = [char]
        elif dist == min_dist:
            corrections.append(char)

    return corrections[0] if len(corrections) == 1 else None


def main():
    letters = ['с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш']

    # Часть 1: Коды с расстоянием ≥ 2 (обнаружение ошибок)
    print("\n" + "=" * 50)
    print("Часть 1: Коды с расстоянием Хемминга ≥ 2 (обнаружение ошибок)")
    print("=" * 50)

    codes_distance_2 = generate_codes(2, len(letters), max_length=5)
    if not codes_distance_2:
        print("Не удалось сгенерировать коды с расстоянием ≥ 2")
        return

    code_dict_2 = dict(zip(letters, codes_distance_2))

    print("\nСгенерированные коды:")
    for char, code in code_dict_2.items():
        print(f"'{char}': {code}")

    validate_code_set(code_dict_2, 2)

    # Демонстрация обнаружения ошибки
    correct_code = next(iter(code_dict_2.values()))
    error_code = correct_code[:-1] + ('1' if correct_code[-1] == '0' else '0')

    print("\nДемонстрация обнаружения ошибки:")
    print(f"Правильный код: {correct_code}")
    print(f"Ошибочный код:  {error_code}")
    print("Обнаружена ошибка:", detect_error(error_code, code_dict_2))

    # Часть 2: Коды с расстоянием ≥ 3 (исправление ошибок)
    print("\n" + "=" * 50)
    print("Часть 2: Коды с расстоянием Хемминга ≥ 3 (исправление ошибок)")
    print("=" * 50)

    codes_distance_3 = generate_codes(3, len(letters), max_length=6)
    if not codes_distance_3:
        print("Не удалось сгенерировать коды с расстоянием ≥ 3")
        return

    code_dict_3 = dict(zip(letters, codes_distance_3))

    print("\nСгенерированные коды:")
    for char, code in code_dict_3.items():
        print(f"'{char}': {code}")

    validate_code_set(code_dict_3, 3)

    # Демонстрация исправления ошибки
    correct_char, correct_code = next(iter(code_dict_3.items()))
    error_code = correct_code[:-1] + ('1' if correct_code[-1] == '0' else '0')

    print("\nДемонстрация исправления ошибки:")
    print(f"Правильный код: {correct_code} (символ '{correct_char}')")
    print(f"Ошибочный код:  {error_code}")

    corrected_char = correct_error(error_code, code_dict_3)
    if corrected_char:
        print(f"Исправленный символ: '{corrected_char}' (код: {code_dict_3[corrected_char]})")
    else:
        print("Ошибка не может быть однозначно исправлена")


if __name__ == "__main__":
    main()