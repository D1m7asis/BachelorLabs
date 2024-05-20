import matplotlib.pyplot as plt
import numpy as np


def execute():
    t = np.linspace(0, 2 * np.pi, 1000)
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for ax, a, b in zip(axs.flat, frec_1, frec_2):
        x = np.sin(a * t)
        y = np.sin(b * t)
        ax.plot(x, y)
        ax.set_title(f'Lissajous Figure (a={a}, b={b})')
        ax.grid(True)


if __name__ == '__main__':
    frec_1 = [3, 3, 5, 5]
    frec_2 = [2, 4, 4, 6]

    execute()

    plt.tight_layout()
    plt.show()
