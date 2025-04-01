import ctypes
import itertools
import math

# 🔵 Цвета для вывода
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def super_explained_arithmetic_encode(word, probabilities):
    """
    📚 Арифметическое кодирование - упаковка строки в число между 0 и 1
    Каждый символ сужает диапазон как в игре "горячо-холодно" 🔍
    """
    print(f"\n{GREEN}🔹 Кодируем слово: '{word}' с вероятностями:{RESET}")
    for char, prob in probabilities.items():
        print(f"   '{char}': {prob:.2f} ({prob * 100:.0f}% вероятности)")

    # 1. Начальный диапазон [0, 1]
    low, high = 0.0, 1.0
    print(f"\n{GREEN}🔹 Начальный диапазон: [{low}, {high}]{RESET}")

    for step, char in enumerate(word, 1):
        print(f"\n{YELLOW}🔹 Шаг {step}: кодируем '{char}'{RESET}")

        # 2. Вычисляем длину текущего диапазона
        range_size = high - low
        print(f"   Текущий диапазон: [{low:.8f}, {high:.8f}]")
        print(f"   Длина диапазона: {range_size:.8f}")

        # 3. Ищем поддиапазон для символа
        current_low = low
        print(f"\n   Поддиапазоны символов:")
        for symbol, prob in probabilities.items():
            symbol_high = current_low + range_size * prob
            marker = " ← " + RED + "НАШ!" + RESET if symbol == char else ""
            print(f"   '{symbol}': [{current_low:.8f}, {symbol_high:.8f}]{marker}")
            if symbol == char:
                high = symbol_high
                break
            current_low = symbol_high

        low = current_low
        print(f"\n   {GREEN}Новый диапазон:{RESET}")
        print(f"   [{low:.8f}, {high:.8f}]")
        print(f"   Новая длина: {high - low:.8f}")

    # 4. Выбираем среднюю точку
    encoded_value = (low + high) / 2
    print(f"\n{GREEN}🔹 Итоговое закодированное число:{RESET}")
    print(f"   ({low:.10f} + {high:.10f}) / 2 = {encoded_value:.10f}")

    return encoded_value


def explain_binary_conversion(number):
    """🧮 Преобразование числа в двоичный вид с пояснениями"""
    print(f"\n{GREEN}🔹 Преобразуем {number:.10f} в двоичный код:{RESET}")
    binary = []
    working_num = number

    for i in range(1, 21):  # 20 итераций
        working_num *= 2
        bit = int(working_num)
        binary.append(str(bit))

        action = ""
        if bit == 1:
            working_num -= 1
            action = f" ({RED}вычитаем 1{RESET}, остаток: {working_num:.5f})"

        print(f"   Шаг {i:2d}: {working_num / 2:.5f} × 2 → {working_num:.5f} → бит {bit}{action}")

    binary_str = ''.join(binary)
    print(f"\n   {GREEN}Итоговый код:{RESET} {binary_str}")
    print(f"   (Первые 20 битов числа {number:.10f})")
    return binary_str


def compare_compression_methods(word, probabilities):
    """Сравнение методов сжатия для заданного слова"""

    # 1. Размер без сжатия (равномерный код)
    uniform_bits = len(word) * math.ceil(math.log2(len(probabilities)))

    # 2. Теоретический минимум (энтропия Шеннона)
    entropy = -sum(p * math.log2(p) for p in probabilities.values())
    shannon_bits = entropy * len(word)

    # 3. Арифметическое кодирование (из предыдущей реализации)
    binary_code = bin(ctypes.c_uint32.from_buffer(ctypes.c_float(encoded_num)).value)
    arithmetic_bits = len(binary_code)

    # 4. RLE-кодирование (для сравнения)
    rle_code = "".join(f"{len(list(g))}{k}" for k, g in itertools.groupby(word))
    rle_bits = len(rle_code) * 8  # Примерная оценка

    # Результаты сравнения
    print(f"\n{GREEN}🔹 Сравнение методов сжатия:{RESET}")
    print(f"{'Метод':<25} | {'Размер (бит)':<10} | {'Эффективность':<10}")
    print("-" * 50)
    print(f"{'1. Без сжатия':<25} | {uniform_bits:<10} | {'1.00x':<10}")
    print(f"{'2. Теория Шеннона':<25} | {shannon_bits:<10.1f} | {uniform_bits / shannon_bits:<10.1f}x")
    print(f"{'3. Арифметическое':<25} | {arithmetic_bits:<10} | {uniform_bits / arithmetic_bits:<10.1f}x")
    print(f"{'4. RLE':<25} | {rle_bits:<10} | {uniform_bits / rle_bits:<10.1f}x")


# Основные параметры
probabilities = {
    'a': 0.05,  # 5%
    'b': 0.10,  # 10%
    'c': 0.05,  # 5%
    'd': 0.55,  # 55% (самый частый)
    'e': 0.15,  # 15%
    'f': 0.10  # 10%
}
word = "eacdbf"

print(f"\n{BLUE}=== АРИФМЕТИЧЕСКОЕ КОДИРОВАНИЕ ===")
print("Каждый символ сужает числовой диапазон! ==={RESET}")

# 1. Кодирование
encoded_num = super_explained_arithmetic_encode(word, probabilities)

# 2. Двоичное преобразование
binary_code = explain_binary_conversion(encoded_num)

# 3. Анализ эффективности
original_bits = len(word) * 3  # 3 бита/символ (log2(6) ≈ 2.58 → 3)
compressed_bits = len(binary_code)
ratio = original_bits / compressed_bits

print(f"\n{GREEN}🔹 Эффективность сжатия:{RESET}")
print(f"   Исходно: {len(word)} симв. × 3 бита = {original_bits} бит")
print(f"   После кодирования: {compressed_bits} бит")
print(f"   Коэффициент сжатия: {ratio:.2f}x")

# 4. Теоретическая основа
entropy = -sum(p * math.log2(p) for p in probabilities.values())
print(f"\n{GREEN}🔹 Теория информации:{RESET}")
print(f"   Энтропия: -Σ p·log2(p) = {entropy:.3f} бит/символ")
print(f"   Минимальный размер: {entropy * len(word):.1f} бит")
print(f"{BLUE}=== КОНЕЦ ==={RESET}")
# После выполнения arithmetic_encode и explain_binary
print(f"\n{BLUE}=== СРАВНЕНИЕ ==={RESET}")

compare_compression_methods(word, probabilities)
