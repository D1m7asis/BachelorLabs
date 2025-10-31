from PyQt6.QtGui import QPainter


class Shape:
    """Базовый класс фигур"""

    def draw(self, painter: QPainter):
        pass

    def transform(self, dx=0, dy=0, angle=0):
        pass
