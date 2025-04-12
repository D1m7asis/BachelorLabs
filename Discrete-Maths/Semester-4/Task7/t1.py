import numpy as np
import networkx as nx
from itertools import combinations
import time
import matplotlib.pyplot as plt


def generate_connected_sparse_graph(n):
    """Генерация связного разреженного графа с подграфами K7 и K4,5."""
    assert n >= 16, "Граф должен содержать минимум 16 вершин!"

    G = nx.Graph()
    G.add_nodes_from(range(n))

    # 1. Подграф K7 (0-6) - полный граф
    for u, v in combinations(range(7), 2):
        G.add_edge(u, v, weight=np.random.uniform(0.1, 1.0))

    # 2. Подграф K4,5 (7-10 и 11-15)
    for u in range(7, 11):
        for v in range(11, 16):
            G.add_edge(u, v, weight=np.random.uniform(0.1, 1.0))

    # 3. Остовное дерево для связности (16...n-1)
    if n > 16:
        for v in range(16, n):
            G.add_edge(v - 1, v, weight=np.random.uniform(0.1, 1.0))

    # 4. Дополнительные случайные рёбра для разреженности
    target_edges = int(2.5 * n)
    while G.number_of_edges() < target_edges:
        u, v = np.random.randint(0, n), np.random.randint(0, n)
        if u != v and not G.has_edge(u, v):
            G.add_edge(u, v, weight=np.random.uniform(0.1, 1.0))

    # Проверка условий
    assert nx.is_connected(G), "Граф не связный!"
    assert any(len(c) >= 7 for c in nx.find_cliques(G)), "Нет подграфа K7!"
    assert nx.is_bipartite(G.subgraph(range(7, 16))), "Нет подграфа K4,5!"

    return G


def floyd_warshall(G):
    """Алгоритм Флойда-Уоршелла для всех пар вершин."""
    n = G.number_of_nodes()
    dist = np.full((n, n), np.inf)
    np.fill_diagonal(dist, 0)

    for u, v, data in G.edges(data=True):
        dist[u][v] = data['weight']
        dist[v][u] = data['weight']

    for k in range(n):
        dist = np.minimum(dist, dist[:, k, np.newaxis] + dist[k, np.newaxis, :])

    return dist


def ford_bellman(G, start):
    """Алгоритм Форда-Беллмана для одной вершины."""
    n = G.number_of_nodes()
    dist = np.full(n, np.inf)
    dist[start] = 0

    edges = list(G.edges(data=True)) + [(v, u, d) for u, v, d in G.edges(data=True)]

    for _ in range(n - 1):
        updated = False
        for u, v, data in edges:
            if dist[u] + data['weight'] < dist[v]:
                dist[v] = dist[u] + data['weight']
                updated = True
        if not updated:
            break

    return dist


def analyze_graph(n):
    """Анализ графа с вычислением расстояний."""
    print(f"\nАнализ графа с {n} вершинами")
    G = generate_connected_sparse_graph(n)

    # Проверка свойств
    print(f"Рёбер: {G.number_of_edges()}")
    print(f"Связность: {nx.is_connected(G)}")

    # Флойд-Уоршелл
    start_time = time.time()
    fw_dist = floyd_warshall(G)
    print(f"\nФлойд-Уоршелл: {time.time() - start_time:.2f} сек")
    print("Пример расстояний (первые 5x5):")
    print(fw_dist[:5, :5])

    # Форд-Беллман
    start_time = time.time()
    fb_dist = ford_bellman(G, 0)
    print(f"\nФорд-Беллман: {time.time() - start_time:.2f} сек")
    print(f"Расстояния от вершины 0: {fb_dist[:10]}...")

    # Сравнение результатов
    assert np.allclose(fb_dist, fw_dist[0]), "Результаты не совпадают!"
    print("\nПроверка: расстояния от 0 совпадают в обоих алгоритмах")


# Запуск для разных размеров графа
for n in [50, 100, 200]:
    analyze_graph(n)