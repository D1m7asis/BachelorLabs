def draw_sierpinski_triangle(n, x_offset, y_offset, size, canvas):
    if n == 0:
        for i in range(size):
            for j in range(i + 1):
                canvas[y_offset + i][x_offset + j] = '*'
    else:
        draw_sierpinski_triangle(n - 1, x_offset, y_offset, size // 2, canvas)  # верхний треугольник
        draw_sierpinski_triangle(n - 1, x_offset + size // 2, y_offset, size // 2, canvas)  # правый треугольник
        draw_sierpinski_triangle(n - 1, x_offset + size // 4, y_offset + size // 2, size // 2, canvas)  # нижний треугольник

def print_canvas(canvas):
    for row in canvas:
        print(' '.join(row))

# Инициализация пустого холста
size = 32  # Размер холста
canvas = [[' ' for _ in range(size)] for _ in range(size)]

# Рисуем треугольник Серпинского на холсте
draw_sierpinski_triangle(3, 0, 0, size, canvas)

# Выводим холст на экран
print_canvas(canvas)
