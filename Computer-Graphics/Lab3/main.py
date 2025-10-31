import sys

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
)

PICK_RADIUS = 12  # порог захвата точки


class SplinePainter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painter - Составной сплайн Безье (C1)")
        self.setMinimumSize(800, 600)

        self.points = []
        self.drag_index = -1
        self.show_control = True
        self.path = None
        self._last_control_pairs = None

        btn_clear = QPushButton("Очистить")
        btn_clear.clicked.connect(self.clear_points)

        btn_build = QPushButton("Построить сплайн")
        btn_build.clicked.connect(self.rebuild_and_update)

        self.chk_control = QCheckBox("Показать вспомогательные точки")
        self.chk_control.setChecked(True)
        self.chk_control.stateChanged.connect(self.toggle_control)

        instr = QLabel("ЛКМ: добавить/перетащить | ПКМ по точке: удалить")

        hbox = QHBoxLayout()
        hbox.addWidget(btn_clear)
        hbox.addWidget(btn_build)
        hbox.addWidget(self.chk_control)
        hbox.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(hbox)
        layout.addWidget(instr)

    def toggle_control(self, state):
        self.show_control = state == Qt.Checked
        self.update()

    def clear_points(self):
        self.points = []
        self.path = None
        self._last_control_pairs = None
        self.update()

    def rebuild_and_update(self):
        self.path = self.build_composite_bezier(self.points)
        self.update()

    def mousePressEvent(self, event):
        p = event.pos()
        if event.button() == Qt.LeftButton:
            idx = self.find_nearest_point_index(p)
            if idx is not None and (self.points[idx] - p).manhattanLength() < PICK_RADIUS:
                self.drag_index = idx
            else:
                self.points.append(QPointF(p))
                self.path = None  # путь пересобирается только по кнопке
                self._last_control_pairs = None
                self.update()
        elif event.button() == Qt.RightButton:
            idx = self.find_nearest_point_index(p)
            if idx is not None and (self.points[idx] - p).manhattanLength() < PICK_RADIUS:
                del self.points[idx]
                self.path = None
                self._last_control_pairs = None
                self.update()

    def mouseMoveEvent(self, event):
        if self.drag_index != -1:
            self.points[self.drag_index] = QPointF(event.pos())
            self.path = None
            self._last_control_pairs = None
            self.update()

    def mouseReleaseEvent(self, event):
        self.drag_index = -1

    def find_nearest_point_index(self, pos):
        best_i, best_d = None, None
        for i, pt in enumerate(self.points):
            d = (pt - pos).manhattanLength()
            if best_d is None or d < best_d:
                best_d, best_i = d, i
        return best_i

    def build_composite_bezier(self, P):
        # Кубический составной Безье с C1
        n = len(P)
        if n < 2:
            self._last_control_pairs = None
            return None

        T = [QPointF(0, 0) for _ in range(n)]
        if n == 2:
            T[0] = P[1] - P[0]
            T[1] = P[1] - P[0]
        else:
            for i in range(1, n - 1):
                T[i] = (P[i + 1] - P[i - 1]) * 0.5
            T[0] = P[1] - P[0]
            T[n - 1] = P[n - 1] - P[n - 2]

        control_pairs = []
        for i in range(n - 1):
            C1 = P[i] + T[i] * (1.0 / 3.0)
            C2 = P[i + 1] - T[i + 1] * (1.0 / 3.0)
            control_pairs.append((C1, C2))

        path = QPainterPath(P[0])
        for i in range(n - 1):
            C1, C2 = control_pairs[i]
            path.cubicTo(C1, C2, P[i + 1])

        self._last_control_pairs = control_pairs
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        painter.setPen(QPen(Qt.black, 1))
        for pt in self.points:
            painter.drawEllipse(pt, 4, 4)

        if len(self.points) >= 2:
            painter.setPen(QPen(QColor(200, 200, 200), 1, Qt.DashLine))
            for i in range(len(self.points) - 1):
                painter.drawLine(self.points[i], self.points[i + 1])

        if self.path is not None:
            painter.setPen(QPen(QColor(10, 100, 200), 2))
            painter.drawPath(self.path)

        if self._last_control_pairs and self.show_control:
            painter.setPen(QPen(QColor(180, 50, 50), 1, Qt.DashLine))
            for i, (C1, C2) in enumerate(self._last_control_pairs):
                painter.drawLine(self.points[i], C1)
                painter.drawLine(self.points[i + 1], C2)

            painter.setPen(QPen(QColor(220, 120, 120), 1))
            for (C1, C2) in self._last_control_pairs:
                painter.drawEllipse(C1, 3, 3)
                painter.drawEllipse(C2, 3, 3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SplinePainter()


    def load_star():
        w.points = [QPointF(x, y) for x, y in
                    [(200, 150), (250, 220), (320, 240), (260, 290), (280, 360),
                     (200, 320), (120, 360), (140, 290), (80, 240), (150, 220), (200, 150)]]
        w.path = None
        w._last_control_pairs = None
        w.update()


    def load_triangle():
        w.points = [QPointF(x, y) for x, y in
                    [(150, 400), (400, 400), (275, 150), (150, 400)]]
        w.path = None
        w._last_control_pairs = None
        w.update()


    def load_house():
        w.points = [QPointF(x, y) for x, y in
                    [(120, 400), (360, 400), (360, 260), (240, 160), (120, 260), (120, 400)]]
        w.path = None
        w._last_control_pairs = None
        w.update()


    btns_layout = QHBoxLayout()
    btn_star = QPushButton("Загрузить: звезда")
    btn_star.clicked.connect(load_star)
    btn_tri = QPushButton("Загрузить: треугольник")
    btn_tri.clicked.connect(load_triangle)
    btn_house = QPushButton("Загрузить: дом")
    btn_house.clicked.connect(load_house)

    btns_layout.addWidget(btn_star)
    btns_layout.addWidget(btn_tri)
    btns_layout.addWidget(btn_house)
    w.layout().addLayout(btns_layout)

    w.show()
    sys.exit(app.exec_())
