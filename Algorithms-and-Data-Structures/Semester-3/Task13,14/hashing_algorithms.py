import hashlib


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().split()


def hash_function(word, table_size):
    hash_object = hashlib.sha256(word.encode())
    hash_value = int(hash_object.hexdigest(), 16)
    return hash_value % table_size


# Лаба №13: Разрешение коллизий с наложением (открытая адресация, линейное пробирование)
def create_hash_table_open_addressing(words, table_size):
    table = [None] * table_size
    for word in words:
        index = hash_function(word, table_size)
        original_index = index
        while table[index] is not None:
            index = (index + 1) % table_size
            if index == original_index:
                raise Exception("Хеш-таблица переполнена")
        table[index] = word
    return table


# Лаба №14: Разрешение коллизий со списками (цепочки)
def create_hash_table_chaining(words, table_size):
    table = [[] for _ in range(table_size)]
    for word in words:
        index = hash_function(word, table_size)
        table[index].append(word)
    return table


def write_hash_table_to_file(filename, table):
    with open(filename, 'w', encoding='utf-8') as file:
        for i, entry in enumerate(table):
            file.write(f"{i}: {entry}\n")


def main():
    input_file = 'input.txt'

    output_file_open_addressing = 'output_open_addressing.txt'
    output_file_chaining = 'output_chaining.txt'

    table_size = 30  # Размер хеш-таблицы

    words = read_file(input_file)

    # Лаба №13: Хеш-таблица с наложением (открытая адресация)
    hash_table_open_addressing = create_hash_table_open_addressing(words, table_size)
    write_hash_table_to_file(output_file_open_addressing, hash_table_open_addressing)

    # Лаба №14: Хеш-таблица со списками (цепочки)
    hash_table_chaining = create_hash_table_chaining(words, table_size)
    write_hash_table_to_file(output_file_chaining, hash_table_chaining)


if __name__ == '__main__':
    main()
