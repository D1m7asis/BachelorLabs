def tsp_dp(adj_matrix):
    """
    Решает задачу коммивояжёра (TSP) с помощью динамического программирования по подмножествам (Held-Karp Algorithm).

    Аргументы:
      adj_matrix: Квадратная матрица n x n, где adj_matrix[i][j] — стоимость перехода из города i в город j.

    Возвращает:
      Минимальную стоимость обхода всех городов и возврата в начальный.
    """
    n = len(adj_matrix)
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Базовый случай: стартуем из города 0

    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue  # Город u не посещён в этом подмножестве

            for v in range(n):
                if mask & (1 << v) or u == v:
                    continue  # Город v уже посещён или совпадает с u

                next_mask = mask | (1 << v)
                dp[next_mask][v] = min(dp[next_mask][v],
                                       dp[mask][u] + adj_matrix[u][v])

    # Финальный шаг — возвращение в начальный город (0)
    min_cost = float('inf')
    full_mask = (1 << n) - 1
    for u in range(1, n):
        min_cost = min(min_cost, dp[full_mask][u] + adj_matrix[u][0])

    return min_cost


if __name__ == '__main__':
    adj_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    result = tsp_dp(adj_matrix)
    print("Минимальная стоимость маршрута:", result)
