import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Заданные ребра
edges = [(0, 1), (0, 4), (6, 0), (7, 0), (1, 2), (2, 3), (3, 7), (3, 5), (3, 4), (6, 3), (4, 5), (7, 5), (5, 6), (6, 7)]

# Создание графа
G = nx.Graph()
G.add_edges_from(edges)

# 1. Чертеж графа
plt.figure(figsize=(10, 8))
nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold')
plt.suptitle("Чертеж графа")
plt.show()

# 2. Список смежности
print("Список смежности:")
adj_list = {node: list(G.neighbors(node)) for node in G.nodes()}
for node, neighbors in adj_list.items():
    print(f"{node}: {neighbors}")

# 3. Матрица смежности
print("\nМатрица смежности:")
adj_matrix = nx.adjacency_matrix(G).todense()
print(adj_matrix)

# 4. Матрица инцидентности
print("\nМатрица инцидентности:")
inc_matrix = nx.incidence_matrix(G).todense().T
print(inc_matrix)

# 5. Вектор степеней вершин
print("\nСтепени вершин:")
degrees = dict(G.degree())
print(degrees)

# 6. Максимальный полный подграф (клика)
max_clique = max(nx.find_cliques(G), key=len)
print(f"\nМаксимальный полный подграф (клика): {max_clique}")

# 7. Дополнение графа
complement = nx.complement(G)
complement_edges = list(complement.edges())
print(f"\nДополнение графа (список ребер): {complement_edges}")

plt.figure(figsize=(10, 8))
nx.draw(complement, with_labels=True, node_color='lightgreen', node_size=500, font_weight='bold')
plt.suptitle("Чертеж дополнения графа")
plt.show()

# 8. Три длинных цикла
print("\nТри длинных цикла:")
cycles = nx.cycle_basis(G)
long_cycles = sorted(cycles, key=len, reverse=True)[:3]
for i, cycle in enumerate(long_cycles, 1):
    print(f"Цикл {i}: {cycle}")

# 9. Реберный граф
line_graph = nx.line_graph(G)
plt.figure(figsize=(10, 8))
nx.draw(line_graph, with_labels=True, node_color='lightcoral', node_size=500, font_weight='bold')
plt.suptitle("Чертеж реберного графа")
plt.show()
