from itertools import permutations

word = "АБРАКАДАБРА"
length = 5

# Получаем все возможные перестановки длины 5 (учитывая порядок)
all_perms = permutations(word, length)

# Убираем дубликаты (так как в слове есть повторяющиеся буквы)
unique_perms = set(all_perms)

print(f"Количество уникальных перестановок из {length} букв: {len(unique_perms)}")