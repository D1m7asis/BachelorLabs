import sys
import numpy as np
import matplotlib.pyplot as plt


def right_turn(p1, p2, p3):
    """
    Определяет, является ли поворот от вектора (p1 -> p2) к вектору (p2 -> p3) поворотом по часовой стрелке.

    Параметры:
    p1, p2, p3 -- кортежи координат точек (x, y).

    Возвращает:
    True, если поворот по часовой стрелке, иначе False.
    """
    return (p3[1] - p1[1]) * (p2[0] - p1[0]) < (p2[1] - p1[1]) * (p3[0] - p1[0])


def graham_scan(points):
    """
    Вычисляет выпуклую оболочку множества точек с использованием алгоритма Грэхема.

    Параметры:
    points -- список кортежей координат точек (x, y).

    Возвращает:
    Массив точек, составляющих выпуклую оболочку.
    """
    points.sort()  # Сортировка по x, при равенстве по y

    # Строим верхнюю цепочку оболочки
    upper_hull = [points[0], points[1]]
    for p in points[2:]:
        upper_hull.append(p)
        while len(upper_hull) > 2 and not right_turn(upper_hull[-3], upper_hull[-2], upper_hull[-1]):
            del upper_hull[-2]

    # Строим нижнюю цепочку оболочки
    lower_hull = [points[-1], points[-2]]
    for p in reversed(points[:-2]):
        lower_hull.append(p)
        while len(lower_hull) > 2 and not right_turn(lower_hull[-3], lower_hull[-2], lower_hull[-1]):
            del lower_hull[-2]

    # Убираем повторяющиеся точки (первая и последняя из нижней цепочки)
    del lower_hull[0]
    del lower_hull[-1]

    convex_hull = upper_hull + lower_hull
    return np.array(convex_hull)


def input_points(N):
    """
    Функция для ручного ввода точек.
    """
    points = []
    print("Введите координаты точек (формат: x y):")
    for i in range(N):
        while True:
            try:
                coords = input(f"Точка {i + 1}: ").split()
                if len(coords) != 2:
                    raise ValueError("Нужно ввести ровно 2 числа.")
                x, y = map(float, coords)
                points.append((x, y))
                break
            except ValueError as ve:
                print("Ошибка ввода:", ve)
    return points


def generate_points(N):
    """
    Функция для генерации случайного набора точек.
    """
    points = [(np.random.randint(0, 300), np.random.randint(0, 300)) for _ in range(N)]
    print("Сгенерированные точки:")
    for i, point in enumerate(points, start=1):
        print(f"Точка {i}: {point}")
    return points


def main():
    try:
        N = int(sys.argv[1])
    except:
        N = int(input("Введите количество точек N (минимум 3): "))

    if N < 3:
        print("Для построения выпуклой оболочки необходимо минимум 3 точки.")
        return

    print("Выберите способ задания точек:")
    print("1 - Ручной ввод")
    print("2 - Генерация случайных точек")
    choice = input("Ваш выбор (1 или 2): ").strip()

    if choice == '1':
        points = input_points(N)
    else:
        points = generate_points(N)

    # Вычисляем выпуклую оболочку
    convex_hull = graham_scan(points)

    # Вывод координат вершин выпуклой оболочки
    print("\nКоординаты вершин выпуклой оболочки (в порядке обхода):")
    for point in convex_hull:
        print(f"({point[0]}, {point[1]})")

    # Преобразуем список точек в массив NumPy для построения графика
    points_np = np.array(points)

    # Построение графика
    plt.figure()
    # Рисуем линии выпуклой оболочки
    plt.plot(convex_hull[:, 0], convex_hull[:, 1], 'b-', label="Выпуклая оболочка")
    # Замыкающая линия
    plt.plot([convex_hull[-1, 0], convex_hull[0, 0]], [convex_hull[-1, 1], convex_hull[0, 1]], 'b-')
    # Рисуем исходные точки
    plt.plot(points_np[:, 0], points_np[:, 1], ".r", label="Исходные точки")
    plt.title("Выпуклая оболочка множества точек")
    plt.legend()
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    main()
