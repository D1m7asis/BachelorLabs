import sys
import numpy as np
import matplotlib.pyplot as plt


def right_turn(p1, p2, p3):
    """
    Определяет, является ли поворот от точки p1 к p2 и затем к p3 правым.

    Параметры:
    p1, p2, p3 -- кортежи координат точек (x, y).

    Возвращает:
    True, если поворот правый (против часовой стрелки), иначе False.
    """
    # Используем формулу определения направления поворота
    return (p3[1] - p1[1]) * (p2[0] - p1[0]) < (p2[1] - p1[1]) * (p3[0] - p1[0])


def graham_scan(points):
    """
    Основной алгоритм Грэхема.

    Вычисляет выпуклую оболочку множества точек с использованием алгоритма Грэхема.

    Параметры:
    points -- список кортежей координат точек (x, y).

    Возвращает:
    Массив точек, составляющих выпуклую оболочку.
    """
    # Сортируем точки по их x-координатам (и y-координатам при равенстве x)
    points.sort()

    # Инициализируем верхнюю часть выпуклой оболочки
    upper_hull = [points[0], points[1]]

    # Вычисляем верхнюю часть выпуклой оболочки
    for i in range(2, len(points)):
        upper_hull.append(points[i])
        while len(upper_hull) > 2 and not right_turn(upper_hull[-3], upper_hull[-2], upper_hull[-1]):
            del upper_hull[-2]

    # Инициализируем нижнюю часть выпуклой оболочки
    lower_hull = [points[-1], points[-2]]

    # Вычисляем нижнюю часть выпуклой оболочки
    for i in range(len(points) - 3, -1, -1):
        lower_hull.append(points[i])
        while len(lower_hull) > 2 and not right_turn(lower_hull[-3], lower_hull[-2], lower_hull[-1]):
            del lower_hull[-2]

    # Удаляем первую и последнюю точки из нижней части, так как они совпадают с верхней частью
    del lower_hull[0]
    del lower_hull[-1]

    # Объединяем верхнюю и нижнюю части для получения полной выпуклой оболочки
    convex_hull = upper_hull + lower_hull

    return np.array(convex_hull)


def main():
    try:
        N = int(sys.argv[1])
    except:
        N = int(input("Введите количество точек N: "))

    # Генерируем случайное множество точек в диапазоне [0, 300) x [0, 300)
    if N < 3:
        print("Для построения выпуклой оболочки необходимо минимум 3 точки.")
        return

    points = [(np.random.randint(0, 300), np.random.randint(0, 300)) for _ in range(N)]

    # Вычисляем выпуклую оболочку
    convex_hull = graham_scan(points)

    # Преобразуем список точек в массив NumPy для удобства работы с графиками
    points = np.array(points)

    # Построение выпуклой оболочки и исходных точек
    plt.figure()
    plt.plot(convex_hull[:, 0], convex_hull[:, 1], 'b-', picker=5)  # Линии выпуклой оболочки
    plt.plot([convex_hull[-1, 0], convex_hull[0, 0]], [convex_hull[-1, 1], convex_hull[0, 1]], 'b-',
             picker=5)  # Замыкающая линия
    plt.plot(points[:, 0], points[:, 1], ".r")  # Исходные точки
    plt.axis('off')  # Отключение осей
    plt.title("Выпуклая оболочка множества точек")
    plt.show()


if __name__ == '__main__':
    main()
