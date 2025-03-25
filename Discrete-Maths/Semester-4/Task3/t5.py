import math


def arithmetic_encode(word, probabilities):
    low = 0.0
    high = 1.0

    for char in word:
        range_size = high - low
        current_low = low
        for symbol, prob in probabilities.items():
            if symbol == char:
                high = current_low + range_size * prob
                break
            current_low += range_size * prob
        low = current_low

    return (low + high) / 2


def float_to_binary(number, precision=20):
    binary = []
    for _ in range(precision):
        number *= 2
        bit = int(number)
        binary.append(str(bit))
        if number >= 1:
            number -= bit
    return ''.join(binary)


def calculate_compression(original_size, encoded_size, uniform_bits):
    compression_rate = encoded_size / (original_size * uniform_bits)
    compression_ratio = (original_size * uniform_bits) / encoded_size
    return compression_rate, compression_ratio


# Исходные данные
probabilities = {
    'a': 0.05,
    'b': 0.10,
    'c': 0.05,
    'd': 0.55,
    'e': 0.15,
    'f': 0.10
}
word = "eacdbf"

# 1. Выполняем арифметическое кодирование
encoded_value = arithmetic_encode(word, probabilities)
binary_code = float_to_binary(encoded_value)

# 2. Рассчитываем параметры сжатия
original_size = len(word)
encoded_size = len(binary_code)
uniform_bits = math.ceil(math.log2(len(probabilities)))  # 3 бита на символ для 6 символов

compression_rate, compression_ratio = calculate_compression(
    original_size, encoded_size, uniform_bits)

# 3. Выводим результаты
print(f"5. Арифметическое кодирование для строки '{word}':")
print(f"Закодированное значение: {encoded_value:.10f}")
print(f"Двоичное представление: {binary_code}")
print(f"Длина двоичного кода: {encoded_size} бит")

print("\nПараметры сжатия:")
print(f"Размер при равномерном кодировании: {original_size * uniform_bits} бит")
print(f"Степень сжатия (compression rate): {compression_rate:.3f}")
print(f"Коэффициент сжатия (compression ratio): {compression_ratio:.3f}")

# 4. Теоретическая энтропия
entropy = -sum(p * math.log2(p) for p in probabilities.values())
print(f"\nТеоретическая энтропия: {entropy:.3f} бит/символ")
print(f"Теоретический минимальный размер: {entropy * original_size:.3f} бит")