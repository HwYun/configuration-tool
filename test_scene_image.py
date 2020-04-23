import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import time

class TestWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.button = QPushButton("Do test")

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.button.clicked.connect(self.showing_Image)

    def showing_Image(self):
        img = QPixmap('image.png')
        # enhancer = ImageEnhance.Brightness(img)
        for i in range(1, 8):
            # img = enhancer.enhance(i)
            self.display_image(img)
            QCoreApplication.processEvents()  # let Qt do his work
            time.sleep(0.5)

    def display_image(self, img):
        self.scene.clear()
        print(img.size())
        w, h = img.size().width(), img.size().height()
        # self.imgQ = QImage.ImageQt(img)  # we need to hold reference to imgQ, or it will crash
        # pixMap = QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(img)
        self.view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        self.scene.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TestWidget()
    widget.resize(640, 480)
    widget.show()

    sys.exit(app.exec_())