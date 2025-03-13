from sympy import symbols, Eq, solve
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


# ----- Классы для работы с геометрическими объектами -----

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Triangle:
    def __init__(self, vertices):
        self.vertices = vertices


class LineSegment:
    def __init__(self, endPoint1, endPoint2):
        self.endPoint1 = endPoint1
        self.endPoint2 = endPoint2


# Для окружности будем использовать кортеж (h, k, r), где (h,k) – центр, r – радиус.

# ----- Алгоритмы пересечения -----

def intersection_two_lines(line1, line2):
    """
    Нахождение пересечения двух прямых, заданных уравнениями:
      line: (a, b, c) соответствует уравнению a*x + b*y = c
    """
    x, y = symbols('x y')
    eq1 = Eq(line1[0] * x + line1[1] * y, line1[2])
    eq2 = Eq(line2[0] * x + line2[1] * y, line2[2])
    solution = solve((eq1, eq2), (x, y))
    if solution:
        return solution[x], solution[y]
    else:
        return None  # Прямые параллельны или совпадают


def point_on_segment(point, segment):
    """
    Проверка, лежит ли точка (x, y) на отрезке, заданном двумя точками.
    segment – кортеж из двух объектов Point.
    """
    x, y = point
    x1, y1 = segment[0].x, segment[0].y
    x2, y2 = segment[1].x, segment[1].y
    return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)


def intersection_line_segment(line, segment):
    """
    Нахождение пересечения прямой и отрезка.
    Прямая задается кортежем (a, b, c), отрезок – объект LineSegment.
    """
    # Представляем отрезок в виде прямой, перпендикулярной ему:
    seg_line = (segment.endPoint2.y - segment.endPoint1.y,
                segment.endPoint1.x - segment.endPoint2.x,
                segment.endPoint1.x * segment.endPoint2.y - segment.endPoint2.x * segment.endPoint1.y)
    intersection_point = intersection_two_lines(line, seg_line)
    if intersection_point and point_on_segment(intersection_point, (segment.endPoint1, segment.endPoint2)):
        return intersection_point
    else:
        return None


def intersection_two_segments(segment1, segment2):
    """
    Нахождение пересечения двух отрезков.
    Каждый отрезок задается объектом LineSegment.
    Если найдено пересечение, возвращает точку (x, y),
    иначе – None.
    """

    # Представляем каждую пару точек отрезка в виде уравнения прямой:
    # Для отрезка (P1, P2) можно получить уравнение в виде:
    # A*x + B*y = C, где A = (y2 - y1), B = (x1 - x2), C = A*x1 + B*y1.
    def line_from_segment(seg):
        A = seg.endPoint2.y - seg.endPoint1.y
        B = seg.endPoint1.x - seg.endPoint2.x
        C = A * seg.endPoint1.x + B * seg.endPoint1.y
        return (A, B, C)

    line1 = line_from_segment(segment1)
    line2 = line_from_segment(segment2)
    ip = intersection_two_lines(line1, line2)
    if ip:
        if point_on_segment(ip, (segment1.endPoint1, segment1.endPoint2)) and point_on_segment(ip, (
        segment2.endPoint1, segment2.endPoint2)):
            return ip
    return None


def intersection_line_circle(line, circle):
    """
    Нахождение точек пересечения прямой и окружности.
    Прямая задается кортежем (a, b, c): a*x + b*y = c.
    Окружность задается кортежем (h, k, r): центр (h,k), радиус r.
    Возвращает список точек пересечения (возможно, пустой, из одной или двух точек).
    """
    a, b, c = line
    h, k, r = circle
    # Переносим уравнение: a*x + b*y = c  =>  a*(x - h) + b*(y - k) = c - a*h - b*k
    # Определим расстояние от центра окружности до прямой:
    D = abs(a * h + b * k - c) / math.sqrt(a ** 2 + b ** 2)
    if D > r:
        return []  # нет пересечений
    # Найдём точку проекции центра на прямую:
    t = (a * h + b * k - c) / (a ** 2 + b ** 2)
    x0 = h - a * t
    y0 = k - b * t
    if math.isclose(D, r):
        return [(x0, y0)]  # касание
    else:
        # Расстояние от точки проекции до точек пересечения
        d = math.sqrt(r ** 2 - D ** 2)
        # Направляющий вектор вдоль прямой: (-b, a) (перпендикулярный нормали (a, b))
        factor = d / math.sqrt(a ** 2 + b ** 2)
        offset_x = -b * factor
        offset_y = a * factor
        p1 = (x0 + offset_x, y0 + offset_y)
        p2 = (x0 - offset_x, y0 - offset_y)
        return [p1, p2]


def intersection_segment_circle(segment, circle):
    """
    Нахождение точек пересечения отрезка и окружности.
    Отрезок задается объектом LineSegment.
    Окружность – кортежем (h, k, r).
    Возвращает список точек пересечения, которые лежат на отрезке.
    """
    # Получаем уравнение прямой, в которой лежит отрезок:
    x1, y1 = segment.endPoint1.x, segment.endPoint1.y
    x2, y2 = segment.endPoint2.x, segment.endPoint2.y
    A = y2 - y1
    B = x1 - x2
    C = A * x1 + B * y1
    line = (A, B, C)
    pts = intersection_line_circle(line, circle)
    # Фильтруем только те точки, которые лежат на отрезке
    return [pt for pt in pts if point_on_segment(pt, (segment.endPoint1, segment.endPoint2))]


def intersection_two_circles(circle1, circle2):
    """
    Нахождение точек пересечения двух окружностей.
    Каждая окружность задается кортежем (h, k, r): центр (h, k) и радиус r.
    Возвращает список точек пересечения (может быть пустым, содержать одну или две точки).
    """
    h1, k1, r1 = circle1
    h2, k2, r2 = circle2
    # Расстояние между центрами:
    d = math.hypot(h2 - h1, k2 - k1)
    # Проверка на отсутствие пересечения
    if d > r1 + r2 or d < abs(r1 - r2):
        return []
    # Если окружности совпадают
    if math.isclose(d, 0) and math.isclose(r1, r2):
        return None  # Бесконечно много точек пересечения
    # Находим точку, лежащую на прямой, соединяющей центры:
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h0 = h1 + (h2 - h1) * a / d
    k0 = k1 + (k2 - k1) * a / d
    # Расстояние от этой точки до точек пересечения
    h = math.sqrt(max(r1 ** 2 - a ** 2, 0))
    # Если h == 0, то окружности касаются
    if math.isclose(h, 0):
        return [(h0, k0)]
    else:
        # Перпендикулярный вектор к направлению между центрами
        rx = -(k2 - k1) * (h / d)
        ry = (h2 - h1) * (h / d)
        p1 = (h0 + rx, k0 + ry)
        p2 = (h0 - rx, k0 - ry)
        return [p1, p2]


# ----- Функции для проверки вложенности треугольников -----

def eval_line(line, p):
    """
    Оценка положения точки p относительно прямой, заданной отрезком line (с двумя точками).
    Вычисляется ориентированная площадь треугольника.
    """
    x1, y1 = line.endPoint1.x, line.endPoint1.y
    x2, y2 = line.endPoint2.x, line.endPoint2.y
    x, y = p.x, p.y
    return (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)


def are_on_same_side_of(p1, p2, line):
    """
    Проверка, находятся ли точки p1 и p2 по одну сторону от прямой, заданной отрезком.
    """
    val1 = eval_line(line, p1)
    val2 = eval_line(line, p2)
    if math.isclose(val1, 0) or math.isclose(val2, 0):
        return False
    return (val1 > 0 and val2 > 0) or (val1 < 0 and val2 < 0)


def is_within(p, t):
    """
    Проверка, находится ли точка p (объект Point) внутри треугольника t.
    Для этого используется метод, сравнивающий положение относительно сторон треугольника.
    """
    # Находим центр треугольника (центроид)
    centroid = Point(0.0, 0.0)
    for vertex in t.vertices:
        centroid.x += vertex.x
        centroid.y += vertex.y
    centroid.x /= 3.0
    centroid.y /= 3.0
    for i in range(3):
        side = LineSegment(t.vertices[i], t.vertices[(i + 1) % 3])
        if not are_on_same_side_of(p, centroid, side):
            return False
    return True


def contains(outer, inner):
    """
    Проверка, содержится ли треугольник inner внутри треугольника outer.
    """
    for vertex in inner.vertices:
        if not is_within(vertex, outer):
            return False
    return True


def check_for_nesting(t1, t2):
    """
    Проверка наличия вложенности двух треугольников.
    """
    if contains(t1, t2) or contains(t2, t1):
        print("These triangles nest.")
    else:
        print("These triangles do not nest.")


def read_triangle():
    """
    Чтение треугольника из стандартного ввода.
    """
    vertices = []
    for _ in range(3):
        x, y = map(float, input().split())
        vertices.append(Point(x, y))
    return Triangle(vertices)


def find_nested_triangles(points):
    """
    Поиск всех треугольников, построенных на основе заданных точек,
    и проверка их на вложенность.
    """
    triangles = []
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                triangles.append(Triangle([points[i], points[j], points[k]]))
    nested_pairs = []
    m = len(triangles)
    for i in range(m):
        for j in range(i + 1, m):
            if contains(triangles[i], triangles[j]) or contains(triangles[j], triangles[i]):
                nested_pairs.append((triangles[i], triangles[j]))
    return nested_pairs


def plot_points_and_triangles(points, nested_triangles):
    """
    Визуализация точек и вложенных треугольников.
    """
    fig, ax = plt.subplots()
    # Рисуем исходные точки
    for point in points:
        ax.plot(point.x, point.y, 'bo')
        ax.text(point.x, point.y, f'({point.x},{point.y})', fontsize=8, ha='right')
    # Рисуем вложенные треугольники
    for triangle in nested_triangles:
        t1_vertices = [(v.x, v.y) for v in triangle[0].vertices]
        t2_vertices = [(v.x, v.y) for v in triangle[1].vertices]
        polygon1 = Polygon(t1_vertices, closed=True, edgecolor='r', fill=None, linewidth=2, label='Nested Triangle 1')
        polygon2 = Polygon(t2_vertices, closed=True, edgecolor='g', fill=None, linewidth=2, label='Nested Triangle 2')
        ax.add_patch(polygon1)
        ax.add_patch(polygon2)
    ax.set_aspect('equal', 'box')
    ax.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Points and Nested Triangles')
    plt.grid(True)
    plt.show()


# ----- Пример использования -----

if __name__ == "__main__":
    # Пример: зададим набор точек
    points = [
        Point(0, 0), Point(1, 0), Point(0, 1),
        Point(0.25, 0.25), Point(0.5, 0.25), Point(0.25, 0.5),
        Point(0.05, 0.03)
    ]

    # Поиск вложенных треугольников
    nested_triangles = find_nested_triangles(points)
    if nested_triangles:
        print("Found nested triangles:")
        for t1, t2 in nested_triangles:
            print(f"Triangle 1: {[(v.x, v.y) for v in t1.vertices]}")
            print(f"Triangle 2: {[(v.x, v.y) for v in t2.vertices]}")
        # Визуализация
        plot_points_and_triangles(points, nested_triangles)
    else:
        print("No nested triangles found.")

    # --- Примеры использования алгоритмов пересечения ---
    # Пересечение двух прямых
    line1 = (1, -1, 0)  # уравнение: x - y = 0
    line2 = (0, 1, 1)  # уравнение: y = 1
    pt = intersection_two_lines(line1, line2)
    print("\nIntersection of two lines:", pt)

    # Пересечение двух отрезков
    seg1 = LineSegment(Point(0, 0), Point(2, 2))
    seg2 = LineSegment(Point(0, 2), Point(2, 0))
    ip_seg = intersection_two_segments(seg1, seg2)
    print("Intersection of two segments:", ip_seg)

    # Пересечение прямой и окружности
    # Прямая: x = 1  =>  уравнение: 1*x + 0*y = 1
    # Окружность: центр (0,0) и радиус 2
    line = (1, 0, 1)
    circle = (0, 0, 2)
    pts_lc = intersection_line_circle(line, circle)
    print("Intersection of line and circle:", pts_lc)

    # Пересечение отрезка и окружности
    seg = LineSegment(Point(-3, 0), Point(3, 0))
    pts_sc = intersection_segment_circle(seg, circle)
    print("Intersection of segment and circle:", pts_sc)

    # Пересечение двух окружностей
    circle1 = (0, 0, 2)
    circle2 = (3, 0, 2)
    pts_cc = intersection_two_circles(circle1, circle2)
    print("Intersection of two circles:", pts_cc)
