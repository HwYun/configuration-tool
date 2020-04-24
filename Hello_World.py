import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import time


class WaH:
    def __init__(self):
        self.width = 0
        self.height = 0


class TopView:
    def __init__(self):
        self.pts = list()
        for i in range(4):
            pt = QPoint()
            self.pts.append(pt)
        self.size = WaH()


class Form(QWidget):

    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.brushcolor = QColor(255, 255, 255, 0)

        self.tL = QPointF()  # topLeft
        self.bR = QPointF()  # bottomRight

        # 탑 뷰
        self.top_view = TopView()

        self.view = CView(self)
        # 전체 레이아웃 박스
        Big_layB = QHBoxLayout()
        self.setLayout(Big_layB)

        # 좌, 중, 우 레이아웃 박스
        leftB = QVBoxLayout()
        middleB = QVBoxLayout()
        rightB = QVBoxLayout()

        #  그룹박스 0 사진 불러오기 버튼
        gb = QGroupBox()
        leftB.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        self.clear_btn = QPushButton('사진 불러오기')
        self.clear_btn.clicked.connect(self.openFileNameDialog)
        hbox.addWidget(self.clear_btn)

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
            self.radiobtns[i].clicked.connect(self.radioClicked)
            box.addWidget(self.radiobtns[i])

        self.radiobtns[0].setChecked(True)
        self.drawType = 0

        # 그룹박스 2
        gb = QGroupBox('펜 설정')
        leftB.addWidget(gb)

        grid = QGridLayout()
        gb.setLayout(grid)
        """
        lb = QLabel('선굵기')
        grid.addWidget(lb, 0, 0)

        self.combo = QComboBox()
        grid.addWidget(self.combo, 0, 1)

        for i in range(1, 51):
            self.combo.addItem(str(i))
        """
        lb = QLabel('선색상')
        grid.addWidget(lb, 1, 0)

        self.pencolor = QColor(0, 255, 0)
        self.penbtn = QPushButton()
        self.penbtn.setStyleSheet('background-color: rgb(0, 0, 0')
        self.penbtn.clicked.connect(self.showColorDlg)
        grid.addWidget(self.penbtn, 1, 1)

        """
        # 그룹박스 3
        gb = QGroupBox('붓 설정')
        leftB.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        lb = QLabel('붓 색상')
        hbox.addWidget(lb)

        
        self.brushbtn = QPushButton()
        self.brushbtn.setStyleSheet('background-color: rgb(255, 255, 255)')
        self.brushbtn.clicked.connect(self.showColorDlg)
        hbox.addWidget(self.brushbtn)
        """

        # 그룹박스 3
        self.TvWidth_input_btn = QPushButton('탑뷰 너비')
        self.TvWidth_input_btn.clicked.connect(self.getTvWidth)
        leftB.addWidget(self.TvWidth_input_btn)

        self.TvHeight_input_btn = QPushButton('탑뷰 높이')
        self.TvHeight_input_btn.clicked.connect(self.getTvHeight)
        leftB.addWidget(self.TvHeight_input_btn)

        #  그룹박스 4
        gb = QGroupBox('지우개')
        leftB.addWidget(gb)

        vbox = QVBoxLayout()
        gb.setLayout(vbox)

        self.Dclear_btn = QPushButton('Reset only Drawing')
        self.Dclear_btn.clicked.connect(self.clear_Clicked_drawing)
        vbox.addWidget(self.Dclear_btn)

        self.clear_btn = QPushButton('All Reset')
        self.clear_btn.clicked.connect(self.clear_Clicked)
        vbox.addWidget(self.clear_btn)

        leftB.addStretch(1)

        # 중앙 레이아웃 박스에 그래픽 뷰 추가

        middleB.addWidget(self.view)

        # 우측 레이아웃 박스 구성

        # 그룹박스 5
        gb = QGroupBox('각종 속성 값')
        rightB.addWidget(gb)

        vbox = QVBoxLayout()
        gb.setLayout(vbox)

        self.coord_text = 'topLeft: ( {0}, {1} )\nbottomRight: ( {2}, {3} )'.format(0.0, 0.0, 0.0, 0.0)
        self.lb5 = QLabel(self.coord_text, self)
        vbox.addWidget(self.lb5)

        self.setMouseTracking(True)

        self.TvSize_text = "TopView_Width: {0}\nTopView_Height: {1}".format(self.top_view.size.width,
                                                                            self.top_view.size.height)
        self.lb6 = QLabel(self.TvSize_text, self)
        vbox.addWidget(self.lb6)
        rightB.addStretch(1)

        # 전체 레이아웃 박스에 좌 중 우 박스 배치
        Big_layB.addLayout(leftB)
        Big_layB.addLayout(middleB)
        Big_layB.addLayout(rightB)

        Big_layB.setStretchFactor(leftB, 0)
        Big_layB.setStretchFactor(middleB, 1)
        Big_layB.setStretchFactor(rightB, 0)

        self.setGeometry(50, 50, 1600, 900)

    def mouseMoveEvent(self, e):
        # x = e.x()
        # y = e.y()
        start_x = self.view.start.x()
        start_y = self.view.start.y()
        end_x = self.view.end.x()
        end_y = self.view.end.y()
        # self.view.mouse_place = e.pos()
        (self.tL.x, self.tL.y), w, h = self.view.coordinateAdj()
        self.bR.x = (self.tL.x + w)
        self.bR.y = (self.tL.y + h)

        # text = 'start_x: {0}, start_y: {1}\nend_x: {2}, end_y : {3}'.format(start_x, start_y, end_x, end_y)
        self.coord_text = 'topLeft: ( {0}, {1} )\nbottomRight: ( {2}, {3} )'.format(self.tL.x, self.tL.y,
                                                                                    self.bR.x, self.bR.y)
        self.lb5.setText(self.coord_text)
        self.lb5.adjustSize()

    def radioClicked(self):
        for i in range(len(self.radiobtns)):
            if self.radiobtns[i].isChecked():
                self.drawType = i
                if i == 0:  # 직선
                    self.pencolor = QColor(0, 255, 0)  # Green
                elif i == 1:  # 곡선
                    self.pencolor = QColor(0, 0, 255)  # Blue
                elif i == 2:  # 직사각형
                    self.pencolor = QColor(255, 0, 0)  # Red
                break

    def checkClicked(self):
        pass

    # 화면에 표시된거 클리어
    def clear_Clicked(self):
        self.view.scene.clear()

    # 진정한 의미로 그린것만 지움. 편법사용 x
    def clear_Clicked_drawing(self):
        for i in self.view.scene.items():
            # print(i)
            # print(type(i))
            if type(i) is not QGraphicsPixmapItem:
                self.view.scene.removeItem(i)
        # self.display_image(self.sid)

    def showColorDlg(self):
        # 색상 대화상자 생성
        color = QColorDialog.getColor()

        sender = self.sender()  # 선 색인지, 붓 색인지 구분하기 위해

        # 색상이 유효한 값이면 참, QFrame에 색 적용
        if sender == self.penbtn and color.isValid():
            self.pencolor = color
            self.penbtn.setStyleSheet('background-color: {}'.format(color.name()))
        else:  # 붓 색은 무조건 투명
            pass
            # self.brushcolor = color
            # self.brushbtn.setStyleSheet('background-color: {}'.format(color.name()))

    def showing_Image(self):
        img = QPixmap('image.png')
        # enhancer = ImageEnhance.Brightness(img)
        for i in range(1, 8):
            # img = enhancer.enhance(i)
            self.display_image(img)
            # QCoreApplication.processEvents()  # let Qt do his work
            # time.sleep(0.5)

    def display_image(self, img):
        self.view.scene.clear()
        print(img.size())
        w, h = img.size().width(), img.size().height()
        # self.imgQ = QImage.ImageQt(img)  # we need to hold reference to imgQ, or it will crash
        # pixMap = QPixmap.fromImage(self.imgQ)
        img.scaled(1280, 720)
        self.view.scene.addPixmap(img)

        # self.view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        # self.view.scene.update()

    def openFileNameDialog(self):
        fileName, f_type = QFileDialog.getOpenFileName(self, "불러올 이미지를 선택하세요", "",
                                                       "All Files(*);;Python Files (*.py)")
        if fileName:
            print(fileName)
            self.sid = QPixmap(fileName)
            self.display_image(self.sid)

    def getTvWidth(self):
        width, ok = QInputDialog.getInt(self, '', "Enter TopView Width")
        if ok:
            self.top_view.size.width = width
            self.lb6.setText("TopView_Width: {0}\nTopView_Height: {1}".format(self.top_view.size.width,
                                                                              self.top_view.size.height))

    def getTvHeight(self):
        height, ok = QInputDialog.getInt(self, '', "Enter TopView Height")
        if ok:
            self.top_view.size.height = height
            self.lb6.setText("TopView_Width: {0}\nTopView_Height: {1}".format(self.top_view.size.width,
                                                                              self.top_view.size.height))


class CView(QGraphicsView):

    # QGraphicsView의 생성자 함수.
    # QGraphicsScene클래스에 그려진 그래픽 아이템(직선, 곡선, 사각형, 원)들을 화면에 표시하는 역할을 담당.
    def __init__(self, parent):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.items = []

        self.start = QPointF()
        self.end = QPointF()

        self.tL = QPointF()
        self.rect_w = 0.0
        self.rect_h = 0.0

        self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.mouse_place = QPointF()

    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0, 0, -2, -2)
        self.scene.setSceneRect(rect)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # 시작점 저장
            self.start = e.pos()
            self.end = e.pos()

    def mouseMoveEvent(self, e):
        # self.mouse_place = e.pos()
        # print(2)
        # e.buttons()는 정수형 값을 리턴, e.button()은 move시 Qt.Nobutton 리턴
        if e.buttons() & Qt.LeftButton:

            self.end = e.pos()

            # 이건 지우개 코드 일단 흰색으로 칠함.
            """
            if self.parent().checkbox.isChecked():
                pen = QPen(QColor(255, 255, 255), 30)  # 색이랑 펜 굵기인듯.
                path = QPainterPath()
                path.moveTo(self.start)
                path.lineTo(self.end)
                self.scene.addPath(path, pen)
                self.start = e.pos()
                return None
            """
            pen = QPen(self.parent().pencolor, 3)

            # drawing Line
            if self.parent().drawType == 0:

                # 장면에 그려진 이전 선을 제거
                if len(self.items) > 0:
                    self.scene.removeItem(self.items[-1])
                    del (self.items[-1])

                # 현재 선 추가
                line = QLineF(self.start.x(), self.start.y(), self.end.x(), self.end.y())
                self.items.append(self.scene.addLine(line, pen))

            # drawing Curve
            if self.parent().drawType == 1:
                path = QPainterPath()
                path.moveTo(self.start)
                path.lineTo(self.end)
                self.scene.addPath(path, pen)

                # 시작점을 다시 기존 끝점으로
                self.start = e.pos()

            # drawing Rectangle
            # 일단 이거 좀 고쳐야 할게... 우측에서 좌측으로 안그려짐.
            # 밑에서 위로도 안그려짐.
            # 해결 2020_04_22 15:55
            if self.parent().drawType == 2:
                brush = QBrush(self.parent().brushcolor)

                # pen = QPen(QColor(0, 255, 0), 3)

                if len(self.items) > 0:
                    self.scene.removeItem(self.items[-1])
                    del (self.items[-1])

                # tL에 topLeft좌표, rect_w에 너비, rect_h에 높이
                (self.tL.x, self.tL.y), self.rect_w, self.rect_h = self.coordinateAdj()

                # rect = QRectF(self.start, self.end)
                rect = QRectF(self.tL.x, self.tL.y, self.rect_w, self.rect_h)
                self.items.append(self.scene.addRect(rect, pen, brush))

            # drawing Ellipse
            if self.parent().drawType == 3:
                brush = QBrush(self.parent().brushcolor)

                if len(self.items) > 0:
                    self.scene.removeItem(self.items[-1])
                    del (self.items[-1])

                # rect = QRectF(self.start, self.end)
                # tL에 topLeft좌표, rect_w에 너비, rect_h에 높이

                (self.tL.x, self.tL.y), self.rect_w, self.rect_h = self.coordinateAdj()

                # rect = QRectF(self.start, self.end)
                rect = QRectF(self.tL.x, self.tL.y, self.rect_w, self.rect_h)
                self.items.append(self.scene.addEllipse(rect, pen, brush))
            # print("!!")
            self.parent().lb5.setText('topLeft: ( {0}, {1} )\nbottomRight: ( {2}, {3} )'.format(self.tL.x,
                                                                                                 self.tL.y,
                                                                                                 self.tL.x + self.rect_w,
                                                                                                 self.tL.y + self.rect_h))
            print('topLeft: ( {0}, {1} )\nbottomRight: ( {2}, {3} )'.format(self.tL.x,
                                                                            self.tL.y,
                                                                            self.tL.x + self.rect_w,
                                                                            self.tL.y + self.rect_h))

    # 직사각형  대각위치의 좌표 2개 입력받으면 topLeft좌표와 width, height 반환 함수.
    def coordinateAdj(self):
        self.s_x = self.start.x()
        self.s_y = self.start.y()
        self.e_x = self.end.x()
        self.e_y = self.end.y()

        if self.s_x < self.e_x and self.s_y < self.e_y:
            return (self.s_x, self.s_y), self.e_x - self.s_x, self.e_y - self.s_y
        elif self.s_x < self.e_x and self.s_y > self.e_y:
            return (self.s_x, self.e_y), self.e_x - self.s_x, self.s_y - self.e_y
        elif self.s_x > self.e_x and self.s_y < self.e_y:
            return (self.e_x, self.s_y), self.s_x - self.e_x, self.e_y - self.s_y
        else:
            return (self.e_x, self.e_y), self.s_x - self.e_x, self.s_y - self.e_y

    # 곡선 제외한 그리기 모드에서 마우스 클릭 해지 시 완성된 그림을 그리는 방식.
    # 직선, 사각형, 원의 경우 클릭 해지 시 기존에 그려진 것들 삭제하고 최종적으로 다시 한번 그리는 방식.
    def mouseReleaseEvent(self, e):

        if e.button() == Qt.LeftButton:

            # 지우개 모드인 경우 바로 리턴함. 다음 그리기 동작 일어나지 않게.
            """
            if self.parent().checkbox.isChecked():
                return None
            """
            pen = QPen(self.parent().pencolor, 3)

            if self.parent().drawType == 0:

                self.items.clear()
                line = QLineF(self.start.x(), self.start.y(), self.end.x(), self.end.y())

                self.scene.addLine(line, pen)

            elif self.parent().drawType == 2:

                brush = QBrush(self.parent().brushcolor)
                # pen = QPen(QColor(0, 255, 0), 3)

                self.items.clear()
                rect = QRectF(self.start, self.end)
                self.scene.addRect(rect, pen, brush)

            elif self.parent().drawType == 3:

                brush = QBrush(self.parent().brushcolor)

                self.items.clear()
                rect = QRectF(self.start, self.end)
                self.scene.addEllipse(rect, pen, brush)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())
