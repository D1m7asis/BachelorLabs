import math

# ANSI-коды для цветного вывода
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def print_step(title, details, color=BLUE):
    """Выводит шаг процесса с заголовком и деталями"""
    print(f"\n{color}=== {title} ==={RESET}")
    print(details)


def insert(word: str, index: int, value: str):
    """Вставляет символ в строку по указанному индексу"""
    return word[:index] + value + word[index:]


def replace(word: str, index: int, value: str):
    """Заменяет символ в строке по указанному индексу"""
    return word[:index] + value + word[index + 1:]


def invert_bit(word: str, index: int):
    """Инвертирует бит по указанному индексу"""
    return replace(word, index, '1' if word[index] == '0' else '0')


def checkBit(pos, startBitPos):
    """Проверяет, контролируется ли позиция данным контрольным битом"""
    bit_controlling_true = startBitPos + 1
    bit_controlling = bit_controlling_true * 2
    if pos > startBitPos:
        return ((pos - startBitPos) % bit_controlling) < bit_controlling_true


def encode(word, block_bits):
    """Кодирует строку в бинарный формат с добавлением контрольных битов Хэмминга"""
    print_step("НАЧАЛО КОДИРОВАНИЯ", f"Исходное слово: '{word}', бит в блоке: {block_bits}")

    # Преобразуем каждый символ в 8-битный бинарный код
    binary = ''.join(f'{ord(c):08b}' for c in word)
    print_step("Бинарное представление", f"'{word}' -> {binary}")

    # Разбиваем на блоки указанного размера
    blocks = [binary[i * block_bits:(i + 1) * block_bits] for i in range(math.ceil(len(binary) / block_bits))]
    print_step("Разбиение на блоки", f"Блоки по {block_bits} бит: {blocks}")

    blocks_result = []
    for block_idx, block in enumerate(blocks):
        print_step(f"Обработка блока {block_idx + 1}", f"Исходный блок: {block}")

        # Вычисляем необходимое количество контрольных битов
        control_bits_count = int(math.log(len(block), 2)) + 1
        print_step(f"Вычисление контрольных битов",
                   f"Для блока длиной {len(block)} бит нужно {control_bits_count} контрольных битов")

        # Позиции для контрольных битов (степени двойки минус 1: 0, 1, 3, 7, 15...)
        control_bits = {2 ** i - 1: 0 for i in range(control_bits_count)}
        print_step("Позиции контрольных битов",
                   f"Контрольные биты будут на позициях: {sorted(control_bits.keys())}")

        # Вставляем нули на позиции контрольных битов
        for pos in sorted(control_bits.keys()):
            block = insert(block, pos, '0')
        print_step("Вставка нулевых контрольных битов", f"Блок после вставки: {block}")

        # Вычисляем значения контрольных битов
        for i in range(len(block)):
            for pos in control_bits:
                if checkBit(i, pos):
                    control_bits[pos] += int(block[i])

        print_step("Вычисление значений контрольных битов",
                   f"Суммы для контрольных битов: {control_bits}")

        # Заменяем нули на вычисленные значения контрольных битов
        for pos in control_bits:
            block = replace(block, pos, str(control_bits[pos] % 2))

        print_step("Финальный блок с контрольными битами",
                   f"Блок после вычисления: {block}\n" +
                   f"Контрольные биты: { {pos: block[pos] for pos in control_bits} }")

        blocks_result.append(block)

    encoded_result = ''.join(blocks_result)
    print_step("РЕЗУЛЬТАТ КОДИРОВАНИЯ",
               f"Итоговое закодированное сообщение:\n{encoded_result}", GREEN)
    return encoded_result


def highlight_errors(binary_str, error_positions):
    """Подсвечивает биты с ошибками в строке"""
    highlighted = []
    for i, bit in enumerate(binary_str):
        if i in error_positions:
            highlighted.append(f"{RED}{bit}{RESET}")
        else:
            highlighted.append(bit)
    return ''.join(highlighted)


def decode(binary, block_bits):
    """Декодирует сообщение, исправляя ошибки с помощью кода Хэмминга"""
    print_step("НАЧАЛО ДЕКОДИРОВАНИЯ", f"Закодированное сообщение: {binary}\nБит в блоке: {block_bits}")

    # Вычисляем количество контрольных битов и размер блока
    control_bits_count = int(math.log(block_bits, 2)) + 1
    block_size = block_bits + control_bits_count
    print_step("Параметры декодирования",
               f"Контрольных битов на блок: {control_bits_count}\n" +
               f"Размер блока: {block_size} бит")

    # Разбиваем на блоки
    blocks = [binary[i * block_size:(i + 1) * block_size] for i in range(math.ceil(len(binary) / block_size))]
    print_step("Разбиение на блоки", f"Полученные блоки: {blocks}")

    result = []
    for block_idx, block in enumerate(blocks):
        print_step(f"Обработка блока {block_idx + 1}", f"Исходный блок: {block}")

        # Позиции контрольных битов
        control_bits = {2 ** i - 1: 0 for i in range(control_bits_count)}
        print_step("Проверка контрольных битов",
                   f"Проверяем контрольные биты на позициях: {sorted(control_bits.keys())}")

        # Вычисляем суммы для каждого контрольного бита
        for i in range(len(block)):
            for pos in control_bits:
                if checkBit(i, pos):
                    control_bits[pos] += int(block[i])

        print_step("Вычисленные суммы", f"Суммы для контрольных битов: {control_bits}")

        # Определяем позицию ошибки
        error_pos = 0
        error_bits = []
        for pos in control_bits:
            if pos < len(block) and block[pos] != str(control_bits[pos] % 2):
                error_bits.append(pos)
                error_pos += pos + 1

        if error_pos > 0:
            print_step("Обнаружена ошибка",
                       f"Несовпадения в контрольных битах: {error_bits}\n" +
                       f"Вычисленная позиция ошибки: {error_pos} (бит №{error_pos - 1})", RED)

            # Исправляем ошибку
            block = invert_bit(block, error_pos - 1)
            print_step("Исправление ошибки",
                       f"Исправленный блок: {block}\n" +
                       f"Инвертирован бит на позиции {error_pos - 1}", GREEN)
        else:
            print_step("Ошибок не обнаружено", "Все контрольные биты совпадают", GREEN)

        # Удаляем контрольные биты
        clean_block = ''.join(block[i] for i in range(len(block)) if i not in control_bits)
        print_step("Удаление контрольных битов",
                   f"Очищенный блок: {clean_block}")

        # Преобразуем бинарную строку в текст
        text = ''.join(chr(int(clean_block[i * 8:(i + 1) * 8], 2)) for i in range(len(clean_block) // 8))
        print_step("Преобразование в текст",
                   f"Декодированный текст: '{text}'")

        result.append(text)

    final_result = ''.join(result)
    print_step("РЕЗУЛЬТАТ ДЕКОДИРОВАНИЯ",
               f"Итоговое декодированное сообщение: {GREEN}{final_result}{RESET}", GREEN)
    return final_result


# Основная программа
if __name__ == "__main__":
    WORD = "kantiana"
    BLOCK_BITS = 32

    print(f"\n{YELLOW}====== НАЧАЛО ПРОГРАММЫ ======{RESET}")
    print(f"Исходное слово: {CYAN}{WORD}{RESET}")
    print(f"Размер блока данных: {BLOCK_BITS} бит")

    # Кодируем сообщение
    encoded = encode(WORD, BLOCK_BITS)

    # Имитируем ошибки (7-й бит первого блока и 17-й бит второго блока)
    control_bits_count = int(math.log(BLOCK_BITS, 2)) + 1
    block_size = BLOCK_BITS + control_bits_count

    error_positions = [6, block_size + 16]  # Индексы сломанных битов (начиная с 0)
    print_step("ИМИТАЦИЯ ОШИБОК",
               f"Инвертируем биты на позициях: {error_positions}\n" +
               f"(Бит 7 в первом блоке и бит 17 во втором блоке)", RED)

    # Инвертируем биты (имитируем ошибки)
    for pos in error_positions:
        encoded = invert_bit(encoded, pos)

    # Выводим с подсветкой ошибок
    highlighted_encoded = highlight_errors(encoded, error_positions)
    print_step("Сообщение с ошибками",
               f"Биты с ошибками выделены {RED}красным{RESET}:\n{highlighted_encoded}", RED)

    # Декодируем и исправляем ошибки
    decoded = decode(encoded, BLOCK_BITS)

    print(f"\n{YELLOW}====== ИТОГОВЫЙ РЕЗУЛЬТАТ ======{RESET}")
    print(f"Исходное слово:  {CYAN}{WORD}{RESET}")
    print(f"Декодированное:  {GREEN}{decoded}{RESET}")
    print(f"Совпадение:      {'✓' if WORD == decoded else '✗'}")