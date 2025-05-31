import tkinter as tk
from tkinter import messagebox
import matplotlib
import numpy as np
from sympy import sympify, E
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tksheet import Sheet

matplotlib.use("TkAgg")

GIVEN_RIGHT_SIDE = "(x - 1) * y / x ** 2"
GIVEN_EXACT_SOLUTION = "x * exp(1 / x)"
# GIVEN_RIGHT_SIDE = "2/x + x/exp(y)"
# GIVEN_EXACT_SOLUTION = "ln(x**2 * (ln(x) + 1))"

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
    x_values, y_values, exact_values, errors = [], [], [], []
    x, y = a, y0

    while x <= b + 1e-10:
        x_values.append(x)
        y_values.append(y)
        exact = float(true_solution_at_point(x).evalf())
        exact_values.append(exact)
        errors.append(abs(float(y) - exact))

        local_error = margin_of_error(x, y, h)
        if local_error > epsilon:
            print(f"[!] Погрешность {local_error:.3e} > ε = {epsilon} на x = {x:.5f}")

        y = runge_kutta_step(x, y, h)
        x = float(x + h)

    return x_values, y_values, exact_values, errors


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.a_entry = self.add_labeled_entry("Начало интервала (a):", "1.0", 0)
        self.b_entry = self.add_labeled_entry("Конец интервала (b):", "2.0", 1)
        self.y0_entry = self.add_labeled_entry("Начальное условие y(a):", "e", 2)
        self.h_entry = self.add_labeled_entry("Шаг (h):", "0.1", 3)
        self.eps_entry = self.add_labeled_entry("Точность (ε):", "0.0001", 4)

        self.exact_solution_entry = self.create_readonly_entry(GIVEN_EXACT_SOLUTION, "Аналитическое решение:", 5)
        self.right_side_entry = self.create_readonly_entry(GIVEN_RIGHT_SIDE, "Правая часть уравнения:", 6)

        tk.Button(self, text="Старт", command=self.start_calculation).grid(row=7, column=0, pady=10)
        tk.Button(self, text="Выход", command=self.master.destroy).grid(row=7, column=1, pady=10)

    def add_labeled_entry(self, label, default, row):
        tk.Label(self, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(self)
        entry.grid(row=row, column=1, padx=10, pady=5)
        entry.insert(0, default)
        return entry

    def create_readonly_entry(self, default_value, label, row):
        tk.Label(self, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(self, state="readonly")
        entry.grid(row=row, column=1, padx=10, pady=5)
        entry.configure(state="normal")
        entry.insert(0, default_value)
        entry.configure(state="readonly")
        return entry

    def parse_numeric_entry(self, entry):
        return float(sympify(entry.get().strip().lower(), locals={'e': E}).evalf())

    def parse_symbolic_entry(self, entry):
        return sympify(entry.get().strip().lower(), locals={'e': E})

    def start_calculation(self):
        try:
            a = self.parse_numeric_entry(self.a_entry)
            b = self.parse_numeric_entry(self.b_entry)
            y0 = self.parse_numeric_entry(self.y0_entry)
            h = self.parse_numeric_entry(self.h_entry)
            epsilon = self.parse_numeric_entry(self.eps_entry)

            global given_func, true_solution
            given_func = self.parse_symbolic_entry(self.right_side_entry)
            true_solution = self.parse_symbolic_entry(self.exact_solution_entry)

            x_vals, y_vals, exact_vals, errors = compute_solution(a, b, y0, h, epsilon)

            self.show_plot_window(x_vals, y_vals)
            self.show_table_window(x_vals, y_vals, exact_vals, errors)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычислений: {str(e)}")

    def show_plot_window(self, x, y):
        x_vals = list(map(float, x))
        y_vals = list(map(float, y))
        x_dense = np.linspace(x_vals[0], x_vals[-1], 1000)
        exact_dense = [float(true_solution_at_point(xi).evalf()) for xi in x_dense]

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x_dense, exact_dense, 'k-', label="Точное")
        ax.plot(x_vals, y_vals, 'ro', label="Численное", markersize=8, markeredgewidth=2)

        ax.set_title("Сравнение решений")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.legend()

        plot_window = tk.Toplevel(self)
        plot_window.title("График решений")
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_table_window(self, x_vals, y_vals, exact_vals, errors):
        table_window = tk.Toplevel(self)
        table_window.title("Таблица значений")
        table_window.geometry("800x500")

        data = [
            [f"{float(x):.5f}",
             f"{float(y):.8f}",
             f"{float(e):.8f}",
             f"{float(err):.2e}"]
            for x, y, e, err in zip(x_vals, y_vals, exact_vals, errors)
        ]
        headers = ["x", "y (приближенное)", "y (аналитическое)", "Погрешность"]

        sheet = Sheet(table_window,
                      data=data,
                      headers=headers,
                      show_x_scrollbar=True,
                      show_y_scrollbar=True)

        sheet.grid(row=0, column=0, sticky="nsew")
        table_window.grid_rowconfigure(0, weight=1)
        table_window.grid_columnconfigure(0, weight=1)

        def resize_columns():
            total_width = sheet.winfo_width()
            col_count = len(headers)
            if col_count > 0 and total_width > 0:
                new_width = max(total_width // col_count, 50)
                sheet.set_all_column_widths(new_width)
            sheet.after(250, resize_columns)

        resize_columns()


def main():
    root = tk.Tk()
    root.title("Метод Рунге-Кутта 4-го порядка")
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
