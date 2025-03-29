import torch
import torch.nn as nn

"""
Задача №4.

1.     Напишите функцию forward_pass(X, w) (𝑤0 входит в 𝑤) для одного нейрона (с сигмоидой) с помощью PyTorch.
"""


def forward_pass(X, w):
    """
    Прямой проход для одного нейрона с сигмоидной активацией.

    Параметры:
        X (torch.Tensor): Матрица признаков размером (n_samples, n_features).
        w (torch.Tensor): Вектор весов размером (n_features + 1,), включая w0 (смещение).

    Возвращает:
        torch.Tensor: Выход нейрона после сигмоиды (размер: (n_samples,)).
    """
    # Добавляем единичный столбец к X для учёта w0 (bias)
    X_with_bias = torch.cat([torch.ones(X.shape[0], 1), X], dim=1)

    # Линейная комбинация: z = w0*1 + w1*x1 + ... + wn*xn
    z = torch.matmul(X_with_bias, w)

    # Сигмоидная активация
    sigma = nn.Sigmoid()
    output = sigma(z)

    return output


# Пример использования
if __name__ == "__main__":
    # Данные: 3 образца, 2 признака
    X = torch.tensor([[1.0, 2.0],
                      [0.5, -1.0],
                      [-1.0, 0.0]], dtype=torch.float32)

    # Веса: w0 (bias) = -0.5, w1 = 1.0, w2 = 0.5
    w = torch.tensor([-0.5, 1.0, 0.5], dtype=torch.float32)

    # Прямой проход
    y_pred = forward_pass(X, w)
    print("Выход нейрона после сигмоиды:\n", y_pred)
