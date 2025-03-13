from itertools import permutations


def tsp_bruteforce(adj_matrix):
    """
    Решает задачу коммивояжёра (TSP) полным перебором всех маршрутов.

    Аргументы:
      adj_matrix: Квадратная матрица n x n, где adj_matrix[i][j] — стоимость перехода из города i в город j.

    Возвращает:
      Минимальную стоимость обхода всех городов и возврата в начальный.
    """
    n = len(adj_matrix)
    cities = list(range(1, n))  # Все города, кроме начального (0)
    min_cost = float('inf')

    # Перебираем все возможные перестановки маршрутов (кроме 0, т.к. он фиксирован)
    for perm in permutations(cities):
        cost = 0
        current_city = 0

        # Считаем стоимость маршрута
        for next_city in perm:
            cost += adj_matrix[current_city][next_city]
            current_city = next_city

        # Возвращаемся в начальный город
        cost += adj_matrix[current_city][0]

        # Обновляем минимум
        min_cost = min(min_cost, cost)

    return min_cost


if __name__ == '__main__':
    # Пример матрицы связности для 4 городов
    adj_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    result = tsp_bruteforce(adj_matrix)
    print("Минимальная стоимость маршрута:", result)
