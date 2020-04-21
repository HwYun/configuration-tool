# 예제 내용
# * 사용자정의 시그널 만들어 사용하기

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Form(QWidget):

    def __init__(self):

        QWidget.__init__(self, flags=Qt.Widget)

        self.setGeometry(30, 30, 600, 400)
        self.begin = QPoint()
        self.end = QPoint()
        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)
        br = QBrush(QColor(100, 10, 10, 40))
        qp.setBrush(br)
        qp.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())