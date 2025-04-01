import math
from collections import Counter

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


def rle_encode_optimized(word, verbose=True):
    """Оптимизированное RLE-кодирование без нулевых маркеров"""
    if verbose:
        print_step("НАЧАЛО RLE КОДИРОВАНИЯ",
                   f"Исходная строка: {GREEN}'{word}'{RESET} (длина: {len(word)})\n"
                   f"Правила кодирования:\n"
                   f"- Последовательности из 2+ одинаковых символов → [count][char]\n"
                   f"- Одиночные символы → остаются как есть")

    if not word:
        if verbose:
            print_info("Пустая строка - возвращаем пустой результат")
        return "", 1, 1

    res = []
    count = 1

    if verbose:
        print_info("Пошаговая обработка символов:")

    for i in range(1, len(word) + 1):
        if i < len(word) and word[i] == word[i - 1]:
            count += 1
        else:
            # Формируем закодированный блок
            if count >= 2:  # Кодируем только повторяющиеся символы
                encoded = f"{count}{word[i - 1]}"
                if verbose:
                    print_info(f"Группа: {YELLOW}{word[i - count:i]}{RESET} → {GREEN}{encoded}{RESET}")
                res.append(encoded)
            else:
                if verbose:
                    print_info(f"Символ: {YELLOW}{word[i - 1]}{RESET} → остается как есть")
                res.append(word[i - 1])
            count = 1

    encoded_str = ''.join(res)

    # Расчет параметров сжатия
    original_size = len(word)
    compressed_size = len(encoded_str)
    compression_rate = compressed_size / original_size if original_size != 0 else 1
    compression_ratio = original_size / compressed_size if compressed_size != 0 else 1

    if verbose:
        print_step("РЕЗУЛЬТАТ КОДИРОВАНИЯ",
                   f"Закодированная строка: {GREEN}'{encoded_str}'{RESET}\n"
                   f"Длина: {compressed_size} (было {original_size})\n"
                   f"Коэффициент сжатия: {GREEN}{compression_ratio:.1f}x{RESET}\n"
                   f"Степень сжатия: {compression_rate:.3f}",
                   GREEN)

    return encoded_str, compression_rate, compression_ratio


def print_encoding_comparison(word, encoded_str):
    """Выводит сравнение методов кодирования"""
    # 1. Равномерное кодирование (8 бит на символ)
    uniform_size = len(word) * 8

    # 2. Теоретическое кодирование Хаффмана
    freq = Counter(word)
    prob = {char: count / len(word) for char, count in freq.items()}
    entropy = -sum(p * math.log2(p) for p in prob.values())
    huffman_size = entropy * len(word)

    # 3. RLE кодирование
    rle_size = len(encoded_str) * 8

    print_step("СРАВНЕНИЕ МЕТОДОВ КОДИРОВАНИЯ",
               f"{'Метод':<25} {'Размер (бит)':<15} {'Коэф. сжатия':<15}\n"
               f"{'-' * 55}\n"
               f"{'1. Равномерное':<25} {uniform_size:<15.2f} {'1.000':<15}\n"
               f"{'2. Теория Хаффмана':<25} {huffman_size:<15.2f} {uniform_size / huffman_size:<15.3f}\n"
               f"{'3. RLE (оптимизир.)':<25} {rle_size:<15.2f} {uniform_size / rle_size:<15.3f}",
               MAGENTA)


if __name__ == "__main__":
    # Тестовые примеры
    test_strings = [
        'aaaaadggggggggggggggghtiyklooooop',
    ]

    for word in test_strings:
        print(f"\n{YELLOW}{' ТЕСТОВЫЙ ПРИМЕР ':=^70}{RESET}")
        print(f"Исходная строка: {CYAN}'{word}'{RESET} (длина: {len(word)})")

        # RLE кодирование
        encoded, rate, ratio = rle_encode_optimized(word)

        # Сравнение методов кодирования
        print_encoding_comparison(word, encoded)

        print(f"\n{GREEN}{' КОНЕЦ ТЕСТА ':=^70}{RESET}\n")