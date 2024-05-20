import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Параметры для фигуры Лисажу
A = 1  # Амплитуда по x
B = 1  # Амплитуда по y
delta = 0  # Сдвиг фаз

# Создание фигуры и оси
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-A, A)
ax.set_ylim(-B, B)
line, = ax.plot([], [], lw=2)


def init():
    line.set_data([], [])
    return line,


def update(frame):
    t = np.linspace(0, 2 * np.pi, 1000)
    freq_ratio = frame / 100  # Изменение частоты от 0 до 1
    x = A * np.sin(1 * t)
    y = B * np.sin(freq_ratio * t + delta)
    line.set_data(x, y)
    return line,


if __name__ == '__main__':
    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 101), init_func=init, blit=True, interval=100)

    plt.show()

    ani.save('lissajous_animation.gif', writer='pillow')
