import math

# ANSI-коды для цветного вывода
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"


def insert(word: str, index: int, value: str):
    return word[:index] + value + word[index:]


def replace(word: str, index: int, value: str):
    return word[:index] + value + word[index + 1:]


def invert_bit(word: str, index: int):
    return replace(word, index, '1' if word[index] == '0' else '0')


def checkBit(pos, startBitPos):
    bit_controlling_true = startBitPos + 1
    bit_controlling = bit_controlling_true * 2
    if pos > startBitPos:
        return ((pos - startBitPos) % bit_controlling) < bit_controlling_true


def encode(word, block_bits):
    binary = ''.join(f'{ord(c):08b}' for c in word)

    blocks = [binary[i * block_bits:(i + 1) * block_bits] for i in range(math.ceil(len(binary) / block_bits))]

    blocks_result = []
    for block in blocks:
        control_bits_count = int(math.log(len(block), 2)) + 1
        control_bits = {2 ** i - 1: 0 for i in range(control_bits_count)}

        for pos in control_bits:
            block = insert(block, pos, '0')

        for i in range(len(block)):
            for pos in control_bits:
                if checkBit(i, pos):
                    control_bits[pos] += int(block[i])

        for pos in control_bits:
            block = replace(block, pos, str(control_bits[pos] % 2))

        blocks_result.append(block)

    return ''.join(blocks_result)


def highlight_errors(binary_str, error_positions):
    highlighted = []
    for i, bit in enumerate(binary_str):
        if i in error_positions:
            highlighted.append(f"{RED}{bit}{RESET}")
        else:
            highlighted.append(bit)
    return ''.join(highlighted)


def decode(binary, block_bits):
    control_bits_count = int(math.log(block_bits, 2)) + 1
    block_size = block_bits + control_bits_count
    blocks = [binary[i * block_size:(i + 1) * block_size] for i in range(math.ceil(len(binary) / block_size))]

    result = []
    for block in blocks:
        control_bits = {2 ** i - 1: 0 for i in range(control_bits_count)}

        for i in range(len(block)):
            for pos in control_bits:
                if checkBit(i, pos):
                    control_bits[pos] += int(block[i])

        error_pos = 0
        for pos in control_bits:
            if pos < len(block) and block[pos] != str(control_bits[pos] % 2):
                error_pos += pos + 1

        if error_pos > 0:
            block = invert_bit(block, error_pos - 1)

        clean_block = ''.join(block[i] for i in range(len(block)) if i not in control_bits)

        text = ''.join(chr(int(clean_block[i * 8:(i + 1) * 8], 2)) for i in range(len(clean_block) // 8))
        result.append(text)

    return ''.join(result)


# Основная программа
WORD = "kantiana"
BLOCK_BITS = 32

# Кодируем сообщение
encoded = encode(WORD, BLOCK_BITS)
print(f"Исходное закодированное сообщение:\n{encoded}")

# Имитируем ошибки (7-й бит первого блока и 17-й бит второго блока)
control_bits_count = int(math.log(BLOCK_BITS, 2)) + 1
block_size = BLOCK_BITS + control_bits_count

error_positions = [6, block_size + 16]  # Индексы сломанных битов (начиная с 0)

# Инвертируем биты (имитируем ошибки)
for pos in error_positions:
    encoded = invert_bit(encoded, pos)

# Выводим с подсветкой ошибок
highlighted_encoded = highlight_errors(encoded, error_positions)
print(f"Сообщение с ошибками (красные биты):\n{highlighted_encoded}")

# Декодируем и исправляем ошибки
decoded = decode(encoded, BLOCK_BITS)
print(f"Декодированное сообщение: {GREEN}{decoded}{RESET}")