import sys

from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QComboBox, QSlider
)


def pil_to_qimage(img: Image.Image) -> QImage:
    img = img.convert("RGBA")
    data = img.tobytes("raw", "RGBA")
    qimg = QImage(data, img.width, img.height, QImage.Format_RGBA8888)
    return qimg.copy()


class BMViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMViewer — режимы масштабирования BMP")
        self.resize(900, 700)

        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #ddd; border: 1px solid gray;")
        self.image_label.setMinimumSize(600, 400)

        self.btn_load = QPushButton("Загрузить BMP")
        self.btn_load.clicked.connect(self.load_image)

        self.scale_label = QLabel("100%")
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setRange(10, 300)
        self.scale_slider.setValue(100)
        self.scale_slider.valueChanged.connect(self.on_scale_changed)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "По соседним",
            "Линейная интерполяция",
            "Сплайновая (бикубическая) интерполяция",
        ])
        self.mode_combo.currentIndexChanged.connect(self.update_scaled_image)

        controls = QHBoxLayout()
        controls.addWidget(self.btn_load)
        controls.addWidget(self.mode_combo)
        controls.addWidget(QLabel("Масштаб"))
        controls.addWidget(self.scale_slider)
        controls.addWidget(self.scale_label)

        layout = QVBoxLayout(self)
        layout.addLayout(controls)
        layout.addWidget(self.image_label)

        self.pil_original: Image.Image | None = None

    def load_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Открыть BMP", "", "BMP files (*.bmp)")
        if not fname:
            return
        try:
            self.pil_original = Image.open(fname).convert("RGBA")
        except Exception as e:
            self.image_label.setText(f"Ошибка загрузки BMP: {e}")
            self.pil_original = None
            return
        self.update_scaled_image()

    def on_scale_changed(self, val):
        self.scale_label.setText(f"{val}%")
        self.update_scaled_image()

    def update_scaled_image(self):
        if self.pil_original is None:
            return

        factor = self.scale_slider.value() / 100.0
        w = max(1, int(self.pil_original.width * factor))
        h = max(1, int(self.pil_original.height * factor))

        mode = self.mode_combo.currentText()
        if mode == "По соседним":
            resample = Image.NEAREST
        elif mode == "Линейная интерполяция":
            resample = Image.BILINEAR
        else:
            resample = Image.BICUBIC

        resized = self.pil_original.resize((w, h), resample=resample)
        qimg = pil_to_qimage(resized)
        self.image_label.setPixmap(QPixmap.fromImage(qimg))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = BMViewer()
    viewer.show()
    sys.exit(app.exec_())
