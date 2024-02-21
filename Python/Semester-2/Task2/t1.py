def generate_pascal_triangle(n):
    triangle = []
    for i in range(n):
        row = [1]  # начинаем каждую строку с 1
        if i > 0:
            prev_row = triangle[i - 1]
            for j in range(1, i):  # вычисляем значения внутренних элементов строки
                row.append(prev_row[j - 1] + prev_row[j])
            row.append(1)  # заканчиваем строку единицей
        triangle.append(row)
    return triangle


def print_pascal_triangle(triangle):
    max_width = len(' '.join(map(str, triangle[-1])))  # вычисляем максимальную ширину строки
    for row in triangle:
        row_str = ' '.join(map(str, row))
        print(row_str.center(max_width))


# Пример использования:
n = int(input("Введите количество строк треугольника Паскаля: "))
pascal_triangle = generate_pascal_triangle(n)
print_pascal_triangle(pascal_triangle)
