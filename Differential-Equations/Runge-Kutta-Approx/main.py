import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import sympify

GIVEN_RIGHT_SIDE = "(x - 1) * y / x ** 2"
GIVEN_EXACT_SOLUTION = "x * exp(1 / x)"

TABLE_WIDTH = 71

global given_func, true_solution


def f(x, y):
    """Вычисление правой части уравнения."""
    return given_func.subs({'x': x, 'y': y})


def true_solution_at_point(x):
    """Вычисление точного решения."""
    return true_solution.subs({'x': x})


def runge_kutta_step(x, y, h):
    """Один шаг метода Рунге-Кутта 4-го порядка."""
    k1 = f(x, y)
    k2 = f(x + h / 2, y + h * k1 / 2)
    k3 = f(x + h / 2, y + h * k2 / 2)
    k4 = f(x + h, y + h * k3)
    return y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


def margin_of_error(x, y, h):
    """Оценка погрешности по правилу Рунге."""
    k1 = f(x, y)
    k2 = f(x + h / 2, y + (h * k1) / 2)
    k3 = f(x + h / 2, y + (h * k2) / 2)
    k4 = f(x + h, y + (h * k3))
    return abs((k3 + k2) - (k4 + k1)) / 15


def compute_solution(a, b, y0, h, epsilon):
    """Решение с автоматическим выбором шага по правилу Рунге."""
    x_values = [a]
    y_values = [y0]
    exact_values = [true_solution_at_point(a)]
    errors = [0]
    h_values = [h]

    x = a
    y = y0
    h_current = h

    while x < b:
        if x + h_current > b:
            h_current = b - x

        error_est = margin_of_error(x, y, h_current)

        if error_est <= epsilon:
            # Принимаем шаг
            y_new = runge_kutta_step(x, y, h_current)
            x += h_current
            y = y_new

            x_values.append(x)
            y_values.append(y)
            exact = true_solution_at_point(x)
            exact_values.append(exact)
            errors.append(abs(y - exact))
            h_values.append(h_current)

            # Адаптация шага
            if error_est < epsilon / 32:
                h_current *= 2
        else:
            # Уменьшаем шаг
            h_current /= 2
            if h_current < 1e-10:
                messagebox.showerror("Ошибка", "Шаг стал слишком маленьким. Увеличьте ε или измените параметры.")
                break

    return x_values, y_values, exact_values, errors, h_values


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # Кнопки и графики
        self.plot_frame = None
        self.quit_btn = None
        self.output = None
        self.start_btn = None
        self.figure = None
        self.canvas = None

        # Поля ввода
        self.a_entry = tk.Entry(self)
        self.b_entry = tk.Entry(self)
        self.y0_entry = tk.Entry(self)
        self.h_entry = tk.Entry(self)
        self.eps_entry = tk.Entry(self)
        self.exact_solution_entry = tk.Entry(self)
        self.right_side_entry = tk.Entry(self)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Начало интервала (a):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.a_entry.grid(row=0, column=1, padx=10, pady=5)
        self.a_entry.insert(0, "1.0")

        tk.Label(self, text="Конец интервала (b):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.b_entry.grid(row=1, column=1, padx=10, pady=5)
        self.b_entry.insert(0, "2.0")

        tk.Label(self, text="Начальное условие y(a):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.y0_entry.grid(row=2, column=1, padx=10, pady=5)
        self.y0_entry.insert(0, "e")

        tk.Label(self, text="Начальный шаг (h):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.h_entry.grid(row=3, column=1, padx=10, pady=5)
        self.h_entry.insert(0, "0.1")

        tk.Label(self, text="Точность (ε):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.eps_entry.grid(row=4, column=1, padx=10, pady=5)
        self.eps_entry.insert(0, "0.0001")

        tk.Label(self, text="Аналитическое решение:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.exact_solution_entry.grid(row=5, column=1, padx=10, pady=5)
        self.exact_solution_entry.insert(0, GIVEN_EXACT_SOLUTION)

        tk.Label(self, text="Правая часть уравнения:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.right_side_entry.grid(row=6, column=1, padx=10, pady=5)
        self.right_side_entry.insert(0, GIVEN_RIGHT_SIDE)

        self.start_btn = tk.Button(self, text="Старт", command=self.start_calculation)
        self.start_btn.grid(row=7, column=0, pady=10)

        self.quit_btn = tk.Button(self, text="Выход", command=self.master.destroy)
        self.quit_btn.grid(row=7, column=1, pady=10)

        self.output = tk.Text(self, height=15, width=TABLE_WIDTH, state=tk.DISABLED)
        self.output.grid(row=8, column=0, columnspan=2, pady=10)

        self.plot_frame = tk.Frame(self)
        self.plot_frame.grid(row=9, column=0, columnspan=2)

    @staticmethod
    def parse_entry(entry):
        """Парсинг введенного значения"""
        from sympy import E
        locals_dict = {'e': E}
        return sympify(entry.get().strip().lower(), locals=locals_dict)

    @staticmethod
    def validate_args(a, b, h, eps):
        if a >= b:
            messagebox.showerror("Ошибка", "Конец интервала должен быть больше начала.")
            return False
        if not h > 0:
            messagebox.showerror("Ошибка", "Начальный шаг должен быть строго больше нуля!")
            return False
        if not eps > 0:
            messagebox.showerror("Ошибка", "Значение точности (эпсилон) должно быть строго больше нуля!")
            return False
        return True

    def start_calculation(self):
        try:
            a = self.parse_entry(self.a_entry)
            b = self.parse_entry(self.b_entry)
            y0 = self.parse_entry(self.y0_entry)
            h = self.parse_entry(self.h_entry)
            eps = self.parse_entry(self.eps_entry)

            global given_func, true_solution
            given_func = sympify(self.right_side_entry.get().strip())
            true_solution = sympify(self.exact_solution_entry.get().strip())

            if not self.validate_args(a, b, h, eps):
                return

            x_vals, y_vals, exact_vals, errors, h_values = compute_solution(a, b, y0, h, eps)

            # Вывод таблицы
            self.output.configure(state='normal')
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"{'x':<10}"
                                       f"{'y (числ.)':<15}"
                                       f"{'y (точн.)':<15}"
                                       f"{'Погрешность':<20}"
                                       f"{'h':<10}\n")
            self.output.insert(tk.END, "=" * TABLE_WIDTH + "\n")

            for x_i, y_i, e_i, err_i, h_i in zip(x_vals, y_vals, exact_vals, errors, h_values):
                self.output.insert(tk.END, f"{float(x_i):<10.5f}"
                                           f"{float(y_i):<15.8f}"
                                           f"{float(e_i):<15.8f}"
                                           f"{'{:.8e}'.format(float(err_i)):<20}"
                                           f"{float(h_i):<10.5f}\n")

            self.output.configure(state='disabled')
            self.show_plot(x_vals, y_vals, errors)

        except ValueError as e:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения.")
            raise e
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычислений: {str(e)}")

    def show_plot(self, x, y, errors):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.figure = plt.Figure(figsize=(10, 4), dpi=100)
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)

        ax1.plot(x, y, label="Численное", color="blue")

        x_vals_float = list(map(float, x))
        x_dense = np.linspace(min(x_vals_float), max(x_vals_float), 1000)
        exact_dense = [float(true_solution_at_point(xi)) for xi in x_dense]

        ax1.plot(x_dense, exact_dense, label="Точное", color="red", linestyle='--', linewidth=2.5)
        ax1.set_title("Сравнение решений")
        ax1.set_xlabel("x")
        ax1.set_ylabel("y")
        ax1.legend()
        ax1.grid(True)

        ax2.plot(x, errors, color="green")
        ax2.set_title("Погрешность на шаге")
        ax2.set_xlabel("x")
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()
        ax2.set_ylabel("Погрешность", labelpad=15)
        ax2.set_yscale("log")
        ax2.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()


def main():
    root = tk.Tk()
    root.title("Метод Рунге-Кутта с графиком и точным решением")
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()