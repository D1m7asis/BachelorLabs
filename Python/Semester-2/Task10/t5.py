import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def main():
    X = np.linspace(-5, 5, 100)
    Y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(X, Y)
    Fx = (X ** 2 + Y ** 2) / 2

    fig = plt.figure(figsize=(14, 6))
    # Первый график
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, Fx, cmap='viridis')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('MSE Surface Plot')
    ax1.set_zlabel('MSE')

    # Второй график с логарифмической осью
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(X, Y, Fx, cmap='viridis')
    ax2.set_zscale('log')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('MSE Surface Plot (Log Scale)')
    ax2.set_zlabel('MSE (log scale)')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
