def rle_encode(word):
    """Кодирование методом RLE с расчетом параметров сжатия"""
    if not word:
        return "", 1, 1

    res = []
    count = 1

    for i in range(1, len(word)):
        if word[i] == word[i - 1]:
            count += 1
        else:
            if count > 1:
                res.append(chr(count) + word[i - 1])
            else:
                # Группа неповторяющихся символов
                start = i - count
                res.append(chr(0) + chr(count) + word[start:i])
            count = 1

    # Обработка последней последовательности
    if count > 1:
        res.append(chr(count) + word[-1])
    else:
        res.append(chr(0) + chr(count) + word[-count:])

    encoded = ''.join(res)

    # Расчет параметров сжатия
    original_size = len(word)
    compressed_size = len(encoded)
    compression_ratio = original_size / compressed_size if compressed_size != 0 else 1
    compression_rate = compressed_size / original_size

    return encoded, compression_rate, compression_ratio


# 3. RLE кодирование
word = 'aaaaadggggggggggggggghtiyklooooop'
encoded, rate, ratio = rle_encode(word)

print("3. RLE кодирование:")
print(f"Исходная строка: {word} (длина: {len(word)})")
print(f"Закодированная строка: {encoded} (длина: {len(encoded)})")
print("Байты закодированной строки:", [ord(c) for c in encoded])
print(f"Степень сжатия (compression rate): {rate:.3f}")
print(f"Коэффициент сжатия (compression ratio): {ratio:.3f}\n")

# 4. Пример для равномерного кодирования (8 бит на символ)
uniform_size = len(word) * 8  # бит
print("4. Равномерное кодирование (8 бит/символ):")
print(f"Размер в битах: {uniform_size}")
print(f"Коэффициент сжатия по сравнению с RLE: {uniform_size / (len(encoded) * 8):.3f}\n")

# 5. Пример для кодирования Хаффмана (теоретический расчет)
from collections import Counter


def theoretical_huffman(word):
    freq = Counter(word)
    avg_length = sum(freq[c] * (1 / len(word)) * len(bin(ord(c))[2:]) for c in freq)
    return avg_length


huffman_size = theoretical_huffman(word) * len(word)
print("5. Теоретическое кодирование Хаффмана:")
print(f"Теоретический размер: {huffman_size:.2f} бит")
print(f"Коэффициент сжатия по сравнению с RLE: {(huffman_size) / (len(encoded) * 8):.3f}")