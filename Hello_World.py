import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Form(QWidget):

    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)

        # 전체 레이아웃 박스
        Big_layB = QHBoxLayout()
        self.setLayout(Big_layB)

        # 좌, 중, 우 레이아웃 박스
        leftB = QVBoxLayout()
        middleB = QVBoxLayout()
        rightB = QVBoxLayout()

        # 그룹박스 1
        gb = QGroupBox('그리기 종류')  # 추후 기능 변경하게되면 이 부분을 버튼으로 처리.
        leftB.addWidget(gb)

        # 그룹박스 1 에서 사용할 레이아웃
        box = QVBoxLayout()
        gb.setLayout(box)

        # 그룹박스 1 라디오 버튼 배치
        text = ['Line', 'Curve', "Rectangle", 'Ellipse']
        self.radiobtns = []

        for i in range(len(text)):
            self.radiobtns.append(QRadioButton(text[i], self))
            self.radiobtns[i].clicked.connect(self.radioCLicked)
            box.addWidget(self.radiobtns[i])

        self. radiobtns[0].setChecked(True)
        self.drawType = 0

        # 그룹박스 2
        gb = QGroupBox('펜 설정')
        leftB.addWidget(gb)

        grid = QGridLayout()
        gb.setLayout(grid)

        lb = QLabel('선굵기')
        grid.addWidget(lb, 0, 0)

        self.combo = QComboBox()
        grid.addWidget(self.combo, 0, 1)

        for i in range(1, 51):
            self.combo.addItem(str(i))

        lb = QLabel('선색상')
        grid.addWidget(lb, 1, 0)

        self.pencolor = QColor(0, 0, 0)
        self.penbtn = QPushButton()
        self.penbtn.setStyleSheet('background-color: rgb(0, 0, 0')
        self.penbtn.clicked.connect(self.showColorDlg)
        grid.addWidget(self.penbtn, 1, 1)

        # 그룹박스 3
        gb = QGroupBox('붓 설정')
        leftB.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        lb = QLabel('붓 색상')
        hbox.addWidget(lb)

        self.brushcolor = QColor(255, 255, 255)
        self.brushbtn = QPushButton()
        self.brushbtn.setStyleSheet('background-color: rgb(255, 255, 255)')
        self.brushbtn.clicked.connect(self.showColorDlg)
        hbox.addWidget(self.brushbtn)

        #  그룹박스 4
        gb = QGroupBox('지우개')
        leftB.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        self.checkbox = QCheckBox('지우개 동작')
        self.checkbox.clicked.connect(self.checkClicked)
        hbox.addWidget(self.checkbox)

        leftB.addStretch(1)

        # 중앙 레이아웃 박스에 그래픽 뷰 추가
        self.view = CView(self)
        middleB.addWidget(self.view)

        # 우측 레이아웃 박스 구성

        gb = QGroupBox('테스트')
        rightB.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        rightB.addStretch(1)

        # 전체 레이아웃 박스에 좌 중 우 박스 배치
        Big_layB.addLayout(leftB)
        Big_layB.addLayout(middleB)
        Big_layB.addLayout(rightB)

        Big_layB.setStretchFactor(leftB, 0)
        Big_layB.setStretchFactor(middleB, 5)
        Big_layB.setStretchFactor(rightB, 2)

        self.setGeometry(100, 100, 1600, 900)

    def radioClicked(self):
        for i in range(len(self.radiobtns)):
            if self.radiobtns[i].isChecked():
                self.drawType = i
                break
    def checkClicked(self):
        pass

    def showColorDlg(self):
        # 색상 대화상자 생성
        color = QColorDialog.getColor()

        sender = self.sender() # 선 색인지, 붓 색인지 구분하기 위해

        # 색상이 유효한 값이면 참, QFrame에 색 적용
        if sender == self.penbtn and color.isValid():
            self.pencolor = color
            self.penbtn.setStyleSheet('background-color: {}'.format(color.name()))
        else:
            self.brushcolor = color
            self.brushbtn.setStyleSheet('background-color: {}'.format(color.name()))


class CView(QGraphicsView):

    # QGraphicsView의 생성자 함수.
    # QGraphicsScene클래스에 그려진 그래픽 아이템(직선, 곡선, 사각형, 원)들을 화면에 표시하는 역할을 담당.
    def __init__(self, parent):
        super().__init(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.items = []

        self.start = QPointF()
        self.end = QPointF()

        # self.setRenderHint(QPainter.HighQualityAntialiasing)

    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0, 0, -2, -2)
        self.scene.setSceneRect(rect)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # 시작점 저장
            self.start = e.pos()
            self.end = e.pos()
















if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())