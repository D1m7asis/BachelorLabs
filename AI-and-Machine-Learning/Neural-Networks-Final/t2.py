import torch

"""
Задача №2.

1.     Создайте два вещественных тензора: a размером (5, 2) и b размером (1,10)

2.     Создайте тензор c, являющийся тензором b, но размера (5, 2)

3.     Произведите все арифметические операции с тензорами a и c.
"""


# 1. Создаем тензоры a и b
a = torch.randn(5, 2)
b = torch.randn(1, 10)

print("Тензор a:")
print(a)
print("Размер a:", a.shape)
print("\nТензор b:")
print(b)
print("Размер b:", b.shape)

# 2. Меняем форму тензора b на (5, 2)
c = b.view(5, 2)  # или reshape
print("\nТензор c:")
print(c)
print("Размер c:", c.shape)

# 3. Арифметические операции
print("\nСложение a + c:")
print(a + c)

print("\nВычитание a - c:")
print(a - c)

print("\nПоэлементное умножение a * c:")
print(a * c)

print("\nПоэлементное деление a / c:")
print(a / c)

print("\nМатричное умножение a @ c.T:")
print(torch.mm(a, c.T))  # или a @ c.T

print("\nПоэлементное возведение в степень a ** c:")
print(a ** c)
