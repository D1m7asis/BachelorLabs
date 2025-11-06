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
CLOSE_EPS = 4.0


def dist2(a: QPointF, b: QPointF) -> float:
    dx = a.x() - b.x()
    dy = a.y() - b.y()
    return dx * dx + dy * dy


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
        self.drag_index = -1
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
                self.rebuild_and_update()
        elif event.button() == Qt.RightButton:
            idx = self.find_nearest_point_index(p)
            if idx is not None and (self.points[idx] - p).manhattanLength() < PICK_RADIUS:
                del self.points[idx]
                self.rebuild_and_update()

    def mouseMoveEvent(self, event):
        if self.drag_index != -1:
            self.points[self.drag_index] = QPointF(event.pos())
            self.rebuild_and_update()

    def mouseReleaseEvent(self, event):
        self.drag_index = -1

    def find_nearest_point_index(self, pos):
        if not self.points:
            return None
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

        is_closed = False
        pts = P
        if n >= 3 and dist2(P[0], P[-1]) <= CLOSE_EPS * CLOSE_EPS:
            pts = P[:-1]
            n = len(pts)
            if n >= 3:
                is_closed = True
            else:
                is_closed = False

        if n < 2:
            self._last_control_pairs = None
            return None

        T = [QPointF(0, 0) for _ in range(n)]
        if is_closed:
            for i in range(n):
                im1 = (i - 1) % n
                ip1 = (i + 1) % n
                T[i] = (pts[ip1] - pts[im1]) * 0.5
        else:
            if n == 2:
                T[0] = pts[1] - pts[0]
                T[1] = pts[1] - pts[0]
            else:
                for i in range(1, n - 1):
                    T[i] = (pts[i + 1] - pts[i - 1]) * 0.5
                T[0] = pts[1] - pts[0]
                T[n - 1] = pts[n - 1] - pts[n - 2]

        control_pairs = []
        if is_closed:
            for i in range(n):
                ip1 = (i + 1) % n
                C1 = pts[i] + T[i] * (1.0 / 3.0)
                C2 = pts[ip1] - T[ip1] * (1.0 / 3.0)
                control_pairs.append((C1, C2))
        else:
            for i in range(n - 1):
                C1 = pts[i] + T[i] * (1.0 / 3.0)
                C2 = pts[i + 1] - T[i + 1] * (1.0 / 3.0)
                control_pairs.append((C1, C2))

        path = QPainterPath(pts[0])
        if is_closed:
            for i in range(n):
                ip1 = (i + 1) % n
                C1, C2 = control_pairs[i]
                path.cubicTo(C1, C2, pts[ip1])
            path.closeSubpath()
        else:
            for i in range(n - 1):
                C1, C2 = control_pairs[i]
                path.cubicTo(C1, C2, pts[i + 1])

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

        if self._last_control_pairs and self.show_control and len(self.points) >= 2:
            painter.setPen(QPen(QColor(180, 50, 50), 1, Qt.DashLine))
            is_closed_now = False
            if len(self.points) >= 3 and dist2(self.points[0], self.points[-1]) <= CLOSE_EPS * CLOSE_EPS:
                is_closed_now = True

            if self.path is not None and is_closed_now:
                n = len(self.points) - 1
                for i, (C1, C2) in enumerate(self._last_control_pairs):
                    ip1 = (i + 1) % n
                    painter.drawLine(self.points[i], C1)
                    painter.drawLine(self.points[ip1], C2)
            else:
                for i, (C1, C2) in enumerate(self._last_control_pairs):
                    if i + 1 < len(self.points):
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
        w.rebuild_and_update()


    def load_triangle():
        w.points = [QPointF(x, y) for x, y in
                    [(150, 400), (400, 400), (275, 150), (150, 400)]]
        w.rebuild_and_update()


    def load_house():
        w.points = [QPointF(x, y) for x, y in
                    [(120, 400), (360, 400), (360, 260), (240, 160), (120, 260), (120, 400)]]
        w.rebuild_and_update()


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
