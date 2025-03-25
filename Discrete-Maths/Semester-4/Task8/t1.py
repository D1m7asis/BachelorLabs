import networkx as nx
import random

def create_graph():
    G = nx.DiGraph()
    edges = {
        ('S', 'p'): 7, ('S', 'd'): 5, ('S', 'a'): 3,
        ('p', 'k'): 2, ('p', 'b'): 3,
        ('d', 'k'): 2, ('d', 'c'): 6,
        ('a', 'd'): 2, ('a', 'k'): 1, ('a', 'b'): 6,
        ('c', 'T'): 4, ('c', 'b'): 1,
        ('b', 'T'): 5,
        ('k', 'T'): 6
    }
    for (u, v), capacity in edges.items():
        G.add_edge(u, v, capacity=capacity)
    return G

def max_flow_min_cut(G, source, sink):
    """
    Возвращает:
    - flow_value: значение максимального потока
    - cut_value: суммарная пропускная способность минимального разреза
    - (reachable, non_reachable): кортеж из двух множеств вершин, лежащих по разные стороны разреза
    - cut_edges: список рёбер, которые пересекают разрез
    """
    # Максимальный поток
    flow_value, flow_dict = nx.maximum_flow(G, source, sink)

    # Минимальный разрез
    cut_value, (reachable, non_reachable) = nx.minimum_cut(G, source, sink)

    # Список рёбер, пересекающих разрез
    cut_edges = []
    for u in reachable:
        for v in G[u]:
            if v in non_reachable:
                cut_edges.append((u, v))

    return flow_value, cut_value, (reachable, non_reachable), cut_edges

def randomize_capacities(G):
    """Заменяет пропускные способности всех рёбер на случайные из диапазона [100, 1000]."""
    for u, v in G.edges:
        G[u][v]['capacity'] = random.randint(100, 1000)

def main():
    G = create_graph()
    source, sink = 'S', 'T'

    print("### Оригинальная сеть ###")
    max_flow, cut_value, (reachable, non_reachable), cut_edges = max_flow_min_cut(G, source, sink)
    print(f"Максимальный поток: {max_flow}")
    print(f"Минимальный разрез (ёмкость): {cut_value}")
    print(f"Рёбра, пересекающие разрез: {cut_edges}")
    print(f"Достижимые из S вершины: {reachable}")
    print(f"Недостижимые из S вершины: {non_reachable}")

    # Рандомизируем пропускные способности
    randomize_capacities(G)

    print("\n### Случайные пропускные способности ###")
    max_flow, cut_value, (reachable, non_reachable), cut_edges = max_flow_min_cut(G, source, sink)
    print(f"Максимальный поток: {max_flow}")
    print(f"Минимальный разрез (ёмкость): {cut_value}")
    print(f"Рёбра, пересекающие разрез: {cut_edges}")
    print(f"Достижимые из S вершины: {reachable}")
    print(f"Недостижимые из S вершины: {non_reachable}")

if __name__ == "__main__":
    main()
