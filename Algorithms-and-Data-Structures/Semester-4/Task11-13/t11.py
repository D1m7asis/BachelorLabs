import numpy as np

n = 40
graph = np.zeros((n, n), dtype=int)


def createGraph():
    global graph
    graph = np.random.randint(0, 2, size=(n, n))

    # Делаем граф симметричным
    for i in range(n):
        for j in range(i, n):
            if i == j:
                graph[i][j] = 0
            else:
                graph[j][i] = graph[i][j]


def doColoring():
    """Алгоритм жадной раскраски графа"""
    colorAssignment = [-1] * n  # -1 означает, что вершина пока не окрашена
    availableColors = [True] * n  # Какие цвета доступны для текущей вершины

    for vertex in range(n):
        # Помечаем занятые цвета (уже используемые соседями)
        for neighbor in range(n):
            if graph[vertex][neighbor] == 1 and colorAssignment[neighbor] != -1:
                availableColors[colorAssignment[neighbor]] = False

        # Находим минимальный доступный цвет
        for color in range(n):
            if availableColors[color]:
                colorAssignment[vertex] = color
                break

        # Сбрасываем доступные цвета для следующей вершины
        availableColors = [True] * n

    return colorAssignment


def printGraph():
    for row in graph:
        for item in row:
            print(item, end=" ")
        print()


if __name__ == '__main__':
    createGraph()
    printGraph()
    colors = doColoring()
    print(f"Использовано {max(colors) + 1} цветов")
