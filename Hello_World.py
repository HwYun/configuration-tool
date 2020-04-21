# 예제 내용
# * 사용자정의 시그널 만들어 사용하기

import sys

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal


class Form(QWidget):

    def __init__(self):

        QWidget.__init__(self, flags=Qt.Widget)
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("여기를 바꾸면 창 이름이 바뀝니다.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())