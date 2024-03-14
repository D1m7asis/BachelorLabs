import numpy as np

def check_linear_dependency(matrix):
    det = np.linalg.det(matrix)
    if det == 0:
        return True
    else:
        return False

# Пример матрицы
mat = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 80]
]

# Вывод матрицы
print("Матрица:")
for row in mat:
    print(row)

# Проверка линейной зависимости
if check_linear_dependency(mat):
    print("Столбцы матрицы линейно зависимы.")
else:
    print("Столбцы матрицы не линейно зависимы.")
