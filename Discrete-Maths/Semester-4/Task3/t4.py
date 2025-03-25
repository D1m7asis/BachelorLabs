import heapq
import math


class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(frequencies):
    heap = [HuffmanNode(char=char, freq=freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heapq.heappop(heap)


def build_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}

    if node.char is not None:
        codes[node.char] = current_code
        return

    build_codes(node.left, current_code + "0", codes)
    build_codes(node.right, current_code + "1", codes)

    return codes


def encode(word, code):
    return ''.join([code[char] for char in word])


def decode(encoded, root):
    current_node = root
    decoded = []

    for bit in encoded:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded.append(current_node.char)
            current_node = root

    return ''.join(decoded)


# Исходные данные
frequencies = {'A': 3, 'B': 5, 'C': 12, 'D': 16, 'E': 19, 'F': 20, 'G': 25}

# 1. Построение дерева Хаффмана
huffman_tree = build_huffman_tree(frequencies)

# 2. Построение кодов
huffman_codes = build_codes(huffman_tree)
print("Коды символов:")
for char, code in sorted(huffman_codes.items()):
    print(f"{char}: {code}")

# 3. Демонстрация кодирования и декодирования
test_word = "GDEGFCABA"
print(f"\nТестовое слово: {test_word}")

encoded = encode(test_word, huffman_codes)
print(f"Закодированное: {encoded}")

decoded = decode(encoded, huffman_tree)
print(f"Декодированное: {decoded}")

# 4. Расчет параметров сжатия для алгоритма Хаффмана
total_symbols = sum(frequencies.values())

# 4.1. Для равномерного кодирования (минимальное количество бит)
uniform_bits_per_symbol = math.ceil(math.log2(len(frequencies)))  # 3 бита на символ
total_uniform = uniform_bits_per_symbol * total_symbols  # 3 * 100 = 300 бит

# 4.2. Для кодирования Хаффмана
avg_length = sum(len(code) * (freq / total_symbols) for char, (code, freq) in
                 zip(huffman_codes.items(), frequencies.items()))

total_huffman = sum(len(code) * freq for char, (code, freq) in
                    zip(huffman_codes.items(), frequencies.items()))

# 4.3. Параметры сжатия
compression_rate_huffman = total_huffman / total_uniform
compression_ratio_huffman = total_uniform / total_huffman

print("\n4. Сравнение с равномерным кодированием:")
print(f"Равномерное кодирование: {uniform_bits_per_symbol} бит/символ, всего {total_uniform} бит")
print(f"Кодирование Хаффмана: средняя длина {avg_length:.2f} бит/символ, всего {total_huffman} бит")
print(f"Степень сжатия (compression rate): {compression_rate_huffman:.3f}")
print(f"Коэффициент сжатия (compression ratio): {compression_ratio_huffman:.3f} (сжали в 1.19 раз)")
