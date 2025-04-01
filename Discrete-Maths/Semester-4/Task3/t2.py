import itertools

# ANSI-коды для цветного вывода
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


def print_step(title, details, color=BLUE):
    """Выводит шаг процесса с заголовком и деталями"""
    print(f"\n{color}=== {title} ==={RESET}")
    print(details)


def print_info(message, color=CYAN):
    """Выводит информационное сообщение"""
    print(f"{color}[INFO]{RESET} {message}")


def print_success(message):
    """Выводит сообщение об успехе"""
    print(f"{GREEN}[SUCCESS]{RESET} {message}")


def print_warning(message):
    """Выводит предупреждение"""
    print(f"{YELLOW}[WARNING]{RESET} {message}")


def print_error(message):
    """Выводит сообщение об ошибке"""
    print(f"{RED}[ERROR]{RESET} {message}")


def hamming_distance(a, b):
    """Вычисляет расстояние Хемминга между двумя строками битов."""
    distance = sum(bit1 != bit2 for bit1, bit2 in zip(a, b))
    print_info(f"Расстояние Хемминга между '{a}' и '{b}': {distance}")
    return distance


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
    print_step("ГЕНЕРАЦИЯ КОДОВ",
               f"Параметры генерации:\n"
               f"- Минимальное расстояние: {min_distance}\n"
               f"- Количество кодов: {num_codes}\n"
               f"- Максимальная длина кода: {max_length}")

    for code_length in range(3, max_length + 1):
        print_info(f"Попытка с длиной кода {code_length}...")

        # Генерируем все возможные коды данной длины
        codes = [''.join(bits) for bits in itertools.product('01', repeat=code_length)]
        print_info(f"Сгенерировано {len(codes)} возможных кодов длины {code_length}")

        valid_codes = []
        attempts = 0

        # Используем жадный алгоритм для выбора кодов
        while codes and len(valid_codes) < num_codes:
            attempts += 1
            current_code = codes.pop(0)
            valid = True

            # Проверяем расстояние до всех уже выбранных кодов
            for existing in valid_codes:
                if hamming_distance(current_code, existing) < min_distance:
                    valid = False
                    break

            if valid:
                valid_codes.append(current_code)
                print_info(f"Добавлен код {current_code} (длина {code_length})")

        print_info(f"Проверено {attempts} кодов, найдено {len(valid_codes)} подходящих")

        if len(valid_codes) >= num_codes:
            print_success(f"Найдены коды длины {code_length} с расстоянием ≥ {min_distance}")
            return valid_codes[:num_codes]
        else:
            print_warning(f"Не удалось найти достаточно кодов длины {code_length}")

    print_error("Не удалось сгенерировать коды с заданными параметрами")
    return None


def validate_code_set(code_dict, min_distance):
    """Проверяет, что все коды удовлетворяют условию минимального расстояния."""
    print_step("ПРОВЕРКА КОДОВ",
               f"Проверяем набор из {len(code_dict)} кодов на минимальное расстояние {min_distance}")

    chars = list(code_dict.keys())
    all_valid = True

    for i in range(len(chars)):
        for j in range(i + 1, len(chars)):
            char1, char2 = chars[i], chars[j]
            code1, code2 = code_dict[char1], code_dict[char2]
            dist = hamming_distance(code1, code2)

            if dist < min_distance:
                print_error(f"'{char1}' ({code1}) и '{char2}' ({code2}) имеют расстояние {dist}")
                all_valid = False
            else:
                print_info(f"'{char1}' и '{char2}': расстояние {dist} (OK)")

    if all_valid:
        print_success(f"Все коды удовлетворяют минимальному расстоянию {min_distance}")
    else:
        print_error("Найдены коды, не удовлетворяющие условию")

    return all_valid


def detect_error(code, code_dict):
    """Обнаруживает наличие ошибки в коде."""
    print_step("ОБНАРУЖЕНИЕ ОШИБКИ", f"Проверяем код: {code}")

    is_valid = code in code_dict.values()

    if is_valid:
        print_success("Код корректен, ошибок не обнаружено")
    else:
        print_error(f"Обнаружена ошибка: код {code} не соответствует ни одному допустимому")

    return not is_valid


def correct_error(error_code, code_dict):
    """Исправляет ошибку в коде (если возможно)."""
    print_step("ИСПРАВЛЕНИЕ ОШИБКИ", f"Пытаемся исправить ошибочный код: {error_code}")

    min_dist = float('inf')
    corrections = []
    distances = {}

    # Вычисляем расстояния до всех допустимых кодов
    for char, code in code_dict.items():
        dist = hamming_distance(error_code, code)
        distances[char] = dist

        if dist < min_dist:
            min_dist = dist
            corrections = [char]
        elif dist == min_dist:
            corrections.append(char)

    print_info("Расстояния до допустимых кодов:")
    for char, dist in distances.items():
        print(f"  '{char}': {dist} (код: {code_dict[char]})")

    if len(corrections) == 1:
        corrected_char = corrections[0]
        print_success(f"Ошибка исправлена: '{corrected_char}' (расстояние {min_dist})")
        return corrected_char
    else:
        print_error(f"Ошибка не может быть однозначно исправлена: несколько вариантов ({', '.join(corrections)})")
        return None


def main():
    letters = ['с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш']

    print(f"\n{MAGENTA}{'=' * 70}")
    print(f"{' ДЕМОНСТРАЦИЯ КОДОВ ХЕММИНГА ':^70}")
    print(f"{'=' * 70}{RESET}")

    # Часть 1: Коды с расстоянием ≥ 2 (обнаружение ошибок)
    print(f"\n{YELLOW}{' Часть 1: Коды с расстоянием Хемминга ≥ 2 (обнаружение ошибок) ':-^70}{RESET}")

    codes_distance_2 = generate_codes(2, len(letters), max_length=5)
    if not codes_distance_2:
        return

    code_dict_2 = dict(zip(letters, codes_distance_2))

    print("\nСгенерированные коды:")
    for char, code in code_dict_2.items():
        print(f"  '{char}': {code}")

    validate_code_set(code_dict_2, 2)

    # Демонстрация обнаружения ошибки
    correct_char, correct_code = next(iter(code_dict_2.items()))
    error_code = correct_code[:-1] + ('1' if correct_code[-1] == '0' else '0')

    print(f"\n{YELLOW}Демонстрация обнаружения ошибки:{RESET}")
    print(f"Правильный код: {GREEN}{correct_code}{RESET} (символ '{correct_char}')")
    print(f"Ошибочный код:  {RED}{error_code}{RESET}")
    detect_error(error_code, code_dict_2)

    # Часть 2: Коды с расстоянием ≥ 3 (исправление ошибок)
    print(f"\n{YELLOW}{' Часть 2: Коды с расстоянием Хемминга ≥ 3 (исправление ошибок) ':-^70}{RESET}")

    codes_distance_3 = generate_codes(3, len(letters), max_length=6)
    if not codes_distance_3:
        return

    code_dict_3 = dict(zip(letters, codes_distance_3))

    print("\nСгенерированные коды:")
    for char, code in code_dict_3.items():
        print(f"  '{char}': {code}")

    validate_code_set(code_dict_3, 3)

    # Демонстрация исправления ошибки
    correct_char, correct_code = next(iter(code_dict_3.items()))
    error_code = correct_code[:-1] + ('1' if correct_code[-1] == '0' else '0')

    print(f"\n{YELLOW}Демонстрация исправления ошибки:{RESET}")
    print(f"Правильный код: {GREEN}{correct_code}{RESET} (символ '{correct_char}')")
    print(f"Ошибочный код:  {RED}{error_code}{RESET}")
    corrected_char = correct_error(error_code, code_dict_3)

    if corrected_char:
        print(f"Исправленный символ: '{GREEN}{corrected_char}{RESET}' (код: {code_dict_3[corrected_char]})")
    else:
        print_error("Ошибка не может быть однозначно исправлена")


if __name__ == "__main__":
    main()