from sympy import symbols, Eq, solve
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


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


def intersection_two_lines(line1, line2):
    # Нахождение пересечения двух прямых
    x, y = symbols('x y')
    eq1 = Eq(line1[0] * x + line1[1] * y, line1[2])
    eq2 = Eq(line2[0] * x + line2[1] * y, line2[2])
    solution = solve((eq1, eq2), (x, y))
    if solution:
        return solution[x], solution[y]
    else:
        return None  # Прямые параллельны или совпадают


def point_on_segment(point, segment):
    # Проверка, лежит ли точка на отрезке
    x, y = point
    x1, y1 = segment[0].x, segment[0].y
    x2, y2 = segment[1].x, segment[1].y
    return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)


def intersection_line_segment(line, segment):
    # Нахождение пересечения прямой и отрезка
    intersection_point = intersection_two_lines(line,
                                                (segment.endPoint2.y - segment.endPoint1.y,
                                                 segment.endPoint1.x - segment.endPoint2.x,
                                                 segment.endPoint1.x * segment.endPoint2.y - segment.endPoint2.x * segment.endPoint1.y))
    if intersection_point and point_on_segment(intersection_point, (segment.endPoint1, segment.endPoint2)):
        return intersection_point
    else:
        return None


def eval_line(line, p):
    # Оценка положения точки относительно прямой
    x1, y1 = line.endPoint1.x, line.endPoint1.y
    x2, y2 = line.endPoint2.x, line.endPoint2.y
    x, y = p.x, p.y
    return (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)


def are_on_same_side_of(p1, p2, line):
    # Проверка, находятся ли две точки по одну сторону от прямой
    val1 = eval_line(line, p1)
    val2 = eval_line(line, p2)
    if val1 == 0 or val2 == 0:
        return False
    return (val1 > 0 and val2 > 0) or (val1 < 0 and val2 < 0)


def is_within(p, t):
    # Проверка, находится ли точка внутри треугольника
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
    # Проверка, содержится ли один треугольник внутри другого
    for vertex in inner.vertices:
        if not is_within(vertex, outer):
            return False
    return True


def check_for_nesting(t1, t2):
    # Проверка наличия вложенных треугольников
    if contains(t1, t2) or contains(t2, t1):
        print("These triangles nest.")
    else:
        print("These triangles do not nest.")


def read_triangle():
    # Чтение треугольника из стандартного ввода
    vertices = []
    for _ in range(3):
        x, y = map(float, input().split())
        vertices.append(Point(x, y))
    return Triangle(vertices)


def find_nested_triangles(points):
    # Поиск всех возможных треугольников и проверка их на вложенность
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
    # Визуализация точек и вложенных треугольников
    fig, ax = plt.subplots()
    # Рисуем все точки
    for point in points:
        ax.plot(point.x, point.y, 'bo')  # Синие точки для исходных точек
        ax.text(point.x, point.y, f'({point.x},{point.y})', fontsize=8, ha='right')
    # Рисуем все треугольники
    for triangle in nested_triangles:
        t1_vertices = [(v.x, v.y) for v in triangle[0].vertices]
        t2_vertices = [(v.x, v.y) for v in triangle[1].vertices]
        polygon1 = Polygon(t1_vertices, closed=True, edgecolor='r', fill=None, linewidth=2, label='Nested Triangle 1')
        polygon2 = Polygon(t2_vertices, closed=True, edgecolor='g', fill=None, linewidth=2, label='Nested Triangle 2')
        ax.add_patch(polygon1)
        ax.add_patch(polygon2)
    # Настройка осей и вывод графика
    ax.set_aspect('equal', 'box')
    ax.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Points and Nested Triangles')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Пример координат точек
    points = [
        Point(0, 0), Point(1, 0), Point(0, 1),
        Point(0.25, 0.25), Point(0.5, 0.25), Point(0.25, 0.5),
        Point(0.05, 0.03)
    ]
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
