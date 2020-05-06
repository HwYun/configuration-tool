import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import xml.etree.ElementTree as ET

import time


class WaH:
    def __init__(self):
        self.width = 0
        self.height = 0


class TopView:
    def __init__(self):
        self.pts = list()
        self.index = 0
        self.size = WaH()


class Form(QWidget):

    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.brushcolor = QColor(255, 255, 255, 0)

        self.camera_id = 0

        self.tL = QPointF()  # topLeft
        self.bR = QPointF()  # bottomRight

        # frame area
        self.frame_area = list()
        self.frame_area_output = tuple()

        # top view
        self.top_view = TopView()
        self.top_view_output = TopView()

        # counting line
        self.counting_line_lst = []
        self.counting_line_lst_calc = []

        # ROI mask
        self.ROI = ""

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

        self.clear_btn = QPushButton('Open Image')
        self.clear_btn.clicked.connect(self.openFileNameDialog)
        hbox.addWidget(self.clear_btn)

        # 그룹박스 1
        gb = QGroupBox('그리기 종류')  # 추후 기능 변경하게되면 이 부분을 버튼으로 처리.
        leftB.addWidget(gb)

        # 그룹박스 1 에서 사용할 레이아웃
        box = QVBoxLayout()
        gb.setLayout(box)

        # 그룹박스 1 라디오 버튼 배치
        text = ['counting_line', 'top_view', "frame_area"]
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

        self.pencolor = QColor(0, 255, 0, 192)
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

        self.ROI_input_btn = QPushButton('ROI')
        self.ROI_input_btn.clicked.connect(self.getROI)
        leftB.addWidget(self.ROI_input_btn)

        self.ID_input_btn = QPushButton('Camera ID')
        self.ID_input_btn.clicked.connect(self.getCameraId)
        leftB.addWidget(self.ID_input_btn)

        #  그룹박스 4
        gb = QGroupBox()
        leftB.addWidget(gb)

        vbox = QVBoxLayout()
        gb.setLayout(vbox)

        self.Dclear_btn = QPushButton('Reset only Drawing')
        self.Dclear_btn.clicked.connect(self.clear_Clicked_drawing)
        vbox.addWidget(self.Dclear_btn)

        self.clear_btn = QPushButton('All Reset')
        self.clear_btn.clicked.connect(self.clear_Clicked)
        vbox.addWidget(self.clear_btn)

        self.scale_up_btn = QPushButton('+')
        self.scale_up_btn.clicked.connect(self.view.scale_up_pixmap)
        vbox.addWidget(self.scale_up_btn)

        self.scale_down_btn = QPushButton('-')
        self.scale_down_btn.clicked.connect(self.view.scale_down_pixmap)
        vbox.addWidget(self.scale_down_btn)

        leftB.addStretch(1)

        # 중앙 레이아웃 박스에 그래픽 뷰 추가

        middleB.addWidget(self.view)

        # 우측 레이아웃 박스 구성

        # 그룹박스 5
        self.gb5 = QGroupBox('속성 값')
        rightB.addWidget(self.gb5)

        self.gb5_vbox = QVBoxLayout()
        self.gb5.setLayout(self.gb5_vbox)

        self.coord_text = 'frame_area: ( {0}, {1} ), ( {2}, {3} )'.format(0.0, 0.0, 0.0, 0.0)
        self.frame_area_lb = QLabel(self.coord_text, self)
        self.gb5_vbox.addWidget(self.frame_area_lb)

        self.setMouseTracking(True)

        self.Tvpoint_text = "top_view_point: [[{0}, {1}], [{2}, {3}], [{4}, {5}], [{6}, {7}]]".format(0, 0, 0, 0, 0, 0,
                                                                                                      0, 0)
        self.Tvpoint_lb = QLabel(self.Tvpoint_text, self)
        self.gb5_vbox.addWidget(self.Tvpoint_lb)

        self.TvSize_text = "top_view_size({0}, {1})".format(self.top_view.size.width, self.top_view.size.height)
        self.TvSize_lb = QLabel(self.TvSize_text, self)
        self.gb5_vbox.addWidget(self.TvSize_lb)

        self.counting_line_text = "counting_line: " + str(self.counting_line_lst)
        self.counting_line_lb = QLabel(self.counting_line_text, self)
        self.gb5_vbox.addWidget(self.counting_line_lb)

        self.roi_path = QLabel("ROI\n", self)
        self.gb5_vbox.addWidget(self.roi_path)

        self.camera_id_lb = QLabel("Camera_ID", self)
        self.gb5_vbox.addWidget(self.camera_id_lb)

        """
        self.tmp_vbox = QVBoxLayout()
        rightB.addWidget(self.tmp_vbox)

        self.tmp_vbox.addStretch(1)
        
        self.save_vbox = QVBoxLayout()
        rightB.addWidget(self.save_vbox)
        """
        self.save_btn = QPushButton('Save')
        self.save_btn.clicked.connect(self.save_data)
        rightB.addWidget(self.save_btn)

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

        if self.drawType == 0:  # counting line
            pass
        elif self.drawType == 1:  # top_view_point
            pass
        elif self.drawType == 2:  # frame_area
            (self.tL.x, self.tL.y), w, h = self.view.coordinateAdj(start_x, start_y, end_x, end_y)
            self.bR.x = (self.tL.x + w)
            self.bR.y = (self.tL.y + h)

            # print(self.view.scale_count)

            if self.view.scale_count != 0:  # scale을 했음.
                if self.view.scale_count > 0:  # 기존보다 확대.
                    for i in range(self.view.scale_count):
                        self.tL.x = 0.90909 * self.tL.x
                        self.tL.y = 0.90909 * self.tL.y
                        self.bR.x = 0.90909 * self.bR.x
                        self.bR.y = 0.90909 * self.bR.y
                        # print(self.tL, self.bR)
                else:  # 기존보다 축소
                    for i in range(self.view.scale_count, 0):
                        self.tL.x = 1.1 * self.tL.x
                        self.tL.y = 1.1 * self.tL.y
                        self.bR.x = 1.1 * self.bR.x
                        self.bR.y = 1.1 * self.bR.y
                        # print(self.tL, self.bR)

            self.coord_text = 'frame_area: ( %4d, %4d ), ( %4d, %4d )' % (self.tL.x, self.tL.y, self.bR.x, self.bR.y)
            self.frame_area_lb.setText(self.coord_text)
            # self.frame_area_lb.adjustSize()

    def radioClicked(self):
        for i in range(len(self.radiobtns)):
            if self.radiobtns[i].isChecked():
                self.drawType = i
                if i == 0:  # counting_line
                    self.pencolor = QColor(0, 255, 0, 192)  # Green
                elif i == 1:  # top_view
                    self.pencolor = QColor(20, 181, 255, 192)  # Blue
                elif i == 2:  # frame_area
                    self.pencolor = QColor(255, 0, 0, 192)  # Red
                break

    def checkClicked(self):
        pass

    # 화면에 표시된거 클리어
    def clear_Clicked(self):
        self.view.scene.clear()
        while len(self.counting_line_lst):
            self.counting_line_lst.pop()
        while len(self.top_view.pts):
            self.top_view.pts.pop()
        while len(self.top_view_output.pts):
            self.top_view_output.pts.pop()
        self.top_view.index = 0
        self.counting_line_lb.setText("counting_line: []")
        self.frame_area_lb.setText('frame_area: ( {0}, {1} ), ( {2}, {3} )'.format(0.0, 0.0, 0.0, 0.0))
        self.Tvpoint_lb.setText("top_view_point: [[{0}, {1}], [{2}, {3}],"
                                " [{4}, {5}], [{6}, {7}]]".format(0, 0, 0, 0, 0, 0, 0, 0))

        self.view.scale_count = 0
        self.view.line_num = 0
        self.view.frame_area_drawing_chk = False

    # 진정한 의미로 그린것만 지움. 편법사용 x
    def clear_Clicked_drawing(self):
        for i in self.view.scene.items():
            # print(i)
            # print(type(i))
            if type(i) is not QGraphicsPixmapItem:
                self.view.scene.removeItem(i)
        while len(self.counting_line_lst):
            self.counting_line_lst.pop()
        while len(self.counting_line_lst_calc):
            self.counting_line_lst_calc.pop()
        while len(self.top_view.pts):
            self.top_view.pts.pop()
        while len(self.top_view_output.pts):
            self.top_view_output.pts.pop()
        self.top_view.index = 0
        self.frame_area = [[0, 0], [0, 0]]
        self.frame_area_output = ((0, 0), (0, 0))
        self.counting_line_lb.setText("counting_line: []")
        self.frame_area_lb.setText('frame_area: ( {0}, {1} ), ( {2}, {3} )'.format(0.0, 0.0, 0.0, 0.0))
        self.Tvpoint_lb.setText("top_view_point: [[{0}, {1}], [{2}, {3}],"
                                " [{4}, {5}], [{6}, {7}]]".format(0, 0, 0, 0, 0, 0, 0, 0))
        # self.display_image(self.sid)
        self.view.line_num = 0
        self.view.frame_area_drawing_chk = False

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

    """
    # 사실 의미없음
    def showing_Image(self):
        img = QPixmap('image.png')
        # enhancer = ImageEnhance.Brightness(img)
        for i in range(1, 8):
            # img = enhancer.enhance(i)
            self.display_image(img)
            # QCoreApplication.processEvents()  # let Qt do his work
            # time.sleep(0.5)
    """

    def openFileNameDialog(self):
        fileName, f_type = QFileDialog.getOpenFileName(self, "불러올 이미지를 선택하세요", "",
                                                       "All Files(*);;Python Files (*.py)")
        if fileName:
            print(fileName)
            self.sid = QPixmap(fileName)
            self.view.scale_count = 0
            self.view.display_image(self.sid)
            self.clear_Clicked_drawing()

    def getROI(self):
        fileName, f_type = QFileDialog.getOpenFileName(self, "Select ROI", "",
                                                       "All Files(*);;Python Files (*.py)")
        if fileName:
            self.ROI = fileName
            self.roi_path.setText("ROI\n" + fileName)

    def getTvWidth(self):
        width, ok = QInputDialog.getInt(self, '', "Enter TopView Width")
        if ok:
            self.top_view.size.width = width
            self.top_view_output.size.width = width
            self.TvSize_lb.setText("top_view_size( %4d, %4d )" % (self.top_view.size.width, self.top_view.size.height))

    def getTvHeight(self):
        height, ok = QInputDialog.getInt(self, '', "Enter TopView Height")
        if ok:
            self.top_view.size.height = height
            self.top_view_output.size.height = height
            self.TvSize_lb.setText("top_view_size( %4d, %4d )" % (self.top_view.size.width, self.top_view.size.height))

    def getCameraId(self):
        tmp_id, ok = QInputDialog.getInt(self, '', "Enter Camera id")
        if ok:
            self.camera_id = tmp_id
            self.camera_id_lb.setText("Camera_ID: %d" % self.camera_id)

    def save_data(self):
        if self.camera_id > 0:
            tree = ET.parse("config_data.xml")
            root = tree.getroot()

            for cctv in root.iter('cctv'):
                if self.camera_id == int(cctv.get('id')):
                    new_frame_area = self.frame_area_output
                    cctv.find('frame_area').text = str(new_frame_area)
                    # cctv.find('frame_area').set('updated', 'yes')

                    new_top_view_point = "["
                    for i in range(len(self.top_view_output.pts)):
                        new_top_view_point = new_top_view_point + str([self.top_view_output.pts[i].x(),
                                                   self.top_view_output.pts[i].y()]) + ", "
                    new_top_view_point = new_top_view_point[:-2] + "]"
                    cctv.find('top_view_point').text = new_top_view_point
                    # cctv.find('top_view_point').set('updated', 'yes')

                    new_top_view_size = (self.top_view_output.size.width, self.top_view_output.size.height)
                    cctv.find('top_view_size').text = str(new_top_view_size)

                    new_counting_line = "["
                    for i in range(len(self.counting_line_lst)):
                        new_counting_line = new_counting_line + "[" + str(self.counting_line_lst[i]) + ", True], "
                    new_counting_line = new_counting_line[:-2] + "]"
                    cctv.find('counting_line').text = str(new_counting_line)

                    new_ROI_mask = self.ROI
                    cctv.find('ROI_mask').text = new_ROI_mask

                    new_HOI_shelf = " "
                    cctv.find('HOI_shelf').text = new_HOI_shelf

            tree.write('output.xml')
        else:
            tmp_id, ok = QInputDialog.getInt(self, '', "Enter Camera id.\nAnd Click Save Button again")
            if ok:
                self.camera_id = tmp_id
                self.camera_id_lb.setText("Camera_ID: %d" % self.camera_id)

class CView(QGraphicsView):

    # QGraphicsView의 생성자 함수.
    # QGraphicsScene클래스에 그려진 그래픽 아이템(직선, 곡선, 사각형, 원)들을 화면에 표시하는 역할을 담당.
    def __init__(self, parent):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.scale_count = 0

        self.item_type = -1 # 직전에 그려진 item type

        self.items = []

        self.start = QPointF()
        self.end = QPointF()

        self.line_num = 0
        self.frame_area_drawing_chk = False

        self.tL = QPointF()
        self.bR = QPointF()
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

            # top_view 점찍기.
            tmp_idx = self.parent().top_view.index
            tmp_pts = self.start
            # print(tmp_idx)
            tmp_text = "top_view: \n["
            if self.parent().drawType == 1 and tmp_idx < 4:  # top_view
                # print("!!")
                if self.scale_count > 0:
                    for i in range(self.scale_count):
                        tmp_pts = 0.90909 * tmp_pts
                elif self.scale_count < 0:
                    for i in range(self.scale_count, 0):
                        tmp_pts = 1.1 * tmp_pts

                self.parent().top_view_output.pts.append(tmp_pts)
                self.parent().top_view.pts.append(self.start)

                for i in range(len(self.parent().top_view_output.pts)):
                    tmp_text = tmp_text + str([self.parent().top_view_output.pts[i].x(), self.parent().top_view_output.pts[i].y()]) + ",\n"
                tmp_text = tmp_text[:-2] + "]"
                self.parent().Tvpoint_lb.setText(tmp_text)

                pen = QPen(self.parent().pencolor, 4)

                if tmp_idx > 0:
                    line = QLineF(self.parent().top_view.pts[tmp_idx - 1].x(),
                                  self.parent().top_view.pts[tmp_idx - 1].y(),
                                  self.parent().top_view.pts[tmp_idx].x(),
                                  self.parent().top_view.pts[tmp_idx].y())
                    self.items.append(self.scene.addLine(line, pen))
                    if tmp_idx == 3:
                        line = QLineF(self.parent().top_view.pts[0].x(),
                                      self.parent().top_view.pts[0].y(),
                                      self.parent().top_view.pts[3].x(),
                                      self.parent().top_view.pts[3].y())
                        self.items.append(self.scene.addLine(line, pen))
                else:
                    line = QLineF(self.start.x(), self.start.y(), self.start.x(), self.start.y())
                    self.items.append(self.scene.addLine(line, pen))

                self.parent().top_view.index = self.parent().top_view.index + 1
                self.item_type = 1

            elif self.parent().drawType == 2:  # frame area
                if self.frame_area_drawing_chk:
                    for i in self.scene.items():
                        if type(i) is QGraphicsRectItem:
                            self.scene.removeItem(i)



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
            pen = QPen(self.parent().pencolor, 4)

            # counting_line
            if self.parent().drawType == 0:

                # 장면에 그려진 이전 선을 제거
                if len(self.items) > 0 and self.item_type != 1:
                    self.scene.removeItem(self.items[-1])
                    del (self.items[-1])


                # 현재 선 추가
                line = QLineF(self.start.x(), self.start.y(), self.end.x(), self.end.y())
                self.items.append(self.scene.addLine(line, pen))
                self.item_type = 0

            # top_view
            """
            if self.parent().drawType == 1:
                path = QPainterPath()
                path.moveTo(self.start)
                path.lineTo(self.end)
                self.scene.addPath(path, pen)

                # 시작점을 다시 기존 끝점으로
                # self.start = e.pos()
            """
            # frame_area
            # 일단 이거 좀 고쳐야 할게... 우측에서 좌측으로 안그려짐.
            # 밑에서 위로도 안그려짐.
            # 해결 2020_04_22 15:55
            if self.parent().drawType == 2:
                brush = QBrush(self.parent().brushcolor)

                # pen = QPen(QColor(0, 255, 0), 3)

                if len(self.items) > 0 and self.item_type != 1:
                    self.scene.removeItem(self.items[-1])
                    del (self.items[-1])

                # tL에 topLeft좌표, rect_w에 너비, rect_h에 높이
                (self.tL.x, self.tL.y), self.rect_w, self.rect_h = self.coordinateAdj(self.start.x(), self.start.y(),
                                                                                      self.end.x(), self.end.y())
                self.bR.x = (self.tL.x + self.rect_w)
                self.bR.y = (self.tL.y + self.rect_h)

                self.parent().frame_area = [[int(self.tL.x), int(self.tL.y)],
                                            [int(self.bR.x), int(self.bR.y)]]

                # print(self.view.scale_count)
                # rect = QRectF(self.start, self.end)
                rect = QRectF(self.tL.x, self.tL.y, self.rect_w, self.rect_h)
                self.items.append(self.scene.addRect(rect, pen, brush))

                self.item_type = 2

                if self.scale_count != 0:  # scale을 했음.
                    if self.scale_count > 0:  # 기존보다 확대.
                        for i in range(self.scale_count):
                            self.tL.x = 0.90909 * self.tL.x
                            self.tL.y = 0.90909 * self.tL.y
                            self.bR.x = 0.90909 * self.bR.x
                            self.bR.y = 0.90909 * self.bR.y
                            # print(self.tL, self.bR)
                    else:  # 기존보다 축소
                        for i in range(self.scale_count, 0):
                            self.tL.x = 1.1 * self.tL.x
                            self.tL.y = 1.1 * self.tL.y
                            self.bR.x = 1.1 * self.bR.x
                            self.bR.y = 1.1 * self.bR.y
                            # print(self.tL, self.bR)

                self.parent().frame_area_lb.setText('frame_area: ( %4d, %4d ), ( %4d, %4d )' % (self.tL.x,
                                                                                                self.tL.y,
                                                                                                self.bR.x,
                                                                                                self.bR.y))
                self.parent().frame_area_output = ((int(self.tL.x), int(self.tL.y)),
                                                   (int(self.bR.x), int(self.bR.y)))


            # test
            """
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
            """

    # 직사각형  대각위치의 좌표 2개 입력받으면 topLeft좌표와 width, height 반환 함수.
    def coordinateAdj(self, s_x, s_y, e_x, e_y):
        if s_x < e_x and s_y < e_y:
            return (s_x, s_y), e_x - s_x, e_y - s_y
        elif s_x < e_x and s_y > e_y:
            return (s_x, e_y), e_x - s_x, s_y - e_y
        elif s_x > e_x and s_y < e_y:
            return (e_x, s_y), s_x - e_x, e_y - s_y
        else:
            return (e_x, e_y), s_x - e_x, s_y - e_y

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

            if self.parent().drawType == 0:  # counting_line

                self.items.clear()
                line = QLineF(self.start.x(), self.start.y(), self.end.x(), self.end.y())

                self.parent().counting_line_lst.append([[self.start.x(), self.start.y()], [self.end.x(), self.end.y()]])
                self.parent().counting_line_lst_calc.append([[self.start.x(), self.start.y()],
                                                             [self.end.x(), self.end.y()]])

                if self.scale_count != 0:  # scale을 했음.
                    if self.scale_count > 0:  # 기존보다 확대.
                        for i in range(self.scale_count):
                            self.parent().counting_line_lst[self.line_num][0][0] = 0.90909 *\
                                                                                   self.parent().counting_line_lst[
                                                                                       self.line_num][0][0]
                            self.parent().counting_line_lst[self.line_num][0][1] = 0.90909 * \
                                                                                   self.parent().counting_line_lst[
                                                                                       self.line_num][0][1]
                            self.parent().counting_line_lst[self.line_num][1][0] = 0.90909 * \
                                                                                   self.parent().counting_line_lst[
                                                                                       self.line_num][1][0]
                            self.parent().counting_line_lst[self.line_num][1][1] = 0.90909 * \
                                                                                   self.parent().counting_line_lst[
                                                                                       self.line_num][1][1]
                    else:  # 기존보다 축소
                        for i in range(self.scale_count, 0):
                            self.parent().counting_line_lst[self.line_num][0][0] = 1.1 * \
                                                                                   self.parent().counting_line_lst[
                                                                                       self.line_num][0][0]
                            self.parent().counting_line_lst[self.line_num][0][1] = 1.1 * \
                                                                                   self.parent().counting_line_lst[
                                                                                       self.line_num][0][1]
                            self.parent().counting_line_lst[self.line_num][1][0] = 1.1 * \
                                                                                   self.parent().counting_line_lst[
                                                                                       self.line_num][1][0]
                            self.parent().counting_line_lst[self.line_num][1][1] = 1.1 * \
                                                                                   self.parent().counting_line_lst[
                                                                                       self.line_num][1][1]
                # print(self.parent().counting_line_lst)

                for j in range(len(self.parent().counting_line_lst)):
                    # print(self.parent().counting_line_lst[j])
                    self.parent().counting_line_lst[j][0][0] = int(self.parent().counting_line_lst[j][0][0])
                    self.parent().counting_line_lst[j][0][1] = int(self.parent().counting_line_lst[j][0][1])
                    self.parent().counting_line_lst[j][1][0] = int(self.parent().counting_line_lst[j][1][0])
                    self.parent().counting_line_lst[j][1][1] = int(self.parent().counting_line_lst[j][1][1])

                tmp_text = "counting_line: \n["
                for i in range(len(self.parent().counting_line_lst)):
                    tmp_text = tmp_text + str(self.parent().counting_line_lst[i]) + ",\n"
                tmp_text = tmp_text[:-2] + "]"
                # self.parent().counting_line_text = "counting_line: " + str(self.parent().counting_line_lst)
                self.parent().counting_line_lb.setText(tmp_text)

                self.scene.addLine(line, pen)
                self.line_num = self.line_num + 1

            elif self.parent().drawType == 2:

                brush = QBrush(self.parent().brushcolor)
                # pen = QPen(QColor(0, 255, 0), 3)

                self.items.clear()
                rect = QRectF(self.start, self.end)
                # self.scene.addRect(rect, pen, brush)
                self.items.append(self.scene.addRect(rect, pen, brush))
                self.frame_area_drawing_chk = True
        print(self.scene.items())

    def display_image(self, img):
        self.scene.clear()
        print(img.size())
        w, h = img.size().width(), img.size().height()

        # self.imgQ = QImage.ImageQt(img)  # we need to hold reference to imgQ, or it will crash
        # pixMap = QPixmap.fromImage(self.imgQ)
        # img.scaled(1280, 720)
        # self.view.scene.addPixmap(img)
        self.item = self.scene.addPixmap(img)

        self.item.setTransformOriginPoint(QPointF(0, 0))

        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        chk = max(w/16, h/9)
        chk = int(chk/12)
        if chk > 6:
            for i in range(chk-6):
               self.scale_down_pixmap()
        """
        if w >= 1920 or h >= 1080:
            for i in range(6):
                self.scale_down_pixmap()
        elif w >= 1600 or h >= 900:
            for i in range(5):
                self.scale_down_pixmap()
        elif w >= 1377 or h >= 768:
            for i in range(4):
                self.scale_down_pixmap()
        elif w >= 1280 or h >= 720:
            for i in range(3):
                self.scale_down_pixmap()
        """


        # self.view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        # self.view.scene.update()

    def scale_up_pixmap(self):
        self.scale_count = self.scale_count + 1
        print(self.scale_count)
        self.item.setScale(1.1 * self.item.scale())
        self.scale_item(1.1)

    def scale_down_pixmap(self):
        self.scale_count = self.scale_count - 1
        print(self.scale_count)
        self.item.setScale(0.90909 * self.item.scale())
        self.scale_item(0.90909)

    def scale_item(self, coefficient):
        # Remove All Drawing
        for i in self.scene.items():
            if type(i) is not QGraphicsPixmapItem:
                self.scene.removeItem(i)

        brush = QBrush(self.parent().brushcolor)

        # counting_line
        if len(self.parent().counting_line_lst_calc):
            pen = QPen(QColor(0, 255, 0, 192), 4)
            for i in range(self.line_num):
                self.parent().counting_line_lst_calc[i][0][0] = coefficient * self.parent().counting_line_lst_calc[i][0][0]
                self.parent().counting_line_lst_calc[i][0][1] = coefficient * self.parent().counting_line_lst_calc[i][0][1]
                self.parent().counting_line_lst_calc[i][1][0] = coefficient * self.parent().counting_line_lst_calc[i][1][0]
                self.parent().counting_line_lst_calc[i][1][1] = coefficient * self.parent().counting_line_lst_calc[i][1][1]
                tmp_start_x = self.parent().counting_line_lst_calc[i][0][0]
                tmp_start_y = self.parent().counting_line_lst_calc[i][0][1]
                tmp_end_x = self.parent().counting_line_lst_calc[i][1][0]
                tmp_end_y = self.parent().counting_line_lst_calc[i][1][1]
                line = QLineF(tmp_start_x, tmp_start_y, tmp_end_x, tmp_end_y)
                self.items.append(self.scene.addLine(line, pen))
                self.item_type = 0

        # top view
        pen = QPen(QColor(20, 181, 255, 192), 4)
        tmp_idx = self.parent().top_view.index
        if tmp_idx > 0:
            for j in range(tmp_idx):
                self.parent().top_view.pts[j] = coefficient * self.parent().top_view.pts[j]
            for i in range(tmp_idx):
                if i > 0:
                    line = QLineF(self.parent().top_view.pts[i - 1].x(),
                                  self.parent().top_view.pts[i - 1].y(),
                                  self.parent().top_view.pts[i].x(),
                                  self.parent().top_view.pts[i].y())
                    self.items.append(self.scene.addLine(line, pen))
                if i == 3:
                    line = QLineF(self.parent().top_view.pts[0].x(),
                                  self.parent().top_view.pts[0].y(),
                                  self.parent().top_view.pts[3].x(),
                                  self.parent().top_view.pts[3].y())
                    self.items.append(self.scene.addLine(line, pen))
                else:
                    line = QLineF(self.parent().top_view.pts[i].x(), self.parent().top_view.pts[i].y(),
                                  self.parent().top_view.pts[i].x(), self.parent().top_view.pts[i].y())
                    self.items.append(self.scene.addLine(line, pen))
            self.item_type = 1

        # frame area
        pen = QPen(QColor(255, 0, 0, 192), 4)
        if self.frame_area_drawing_chk:
            self.parent().frame_area[0][0] = coefficient * self.parent().frame_area[0][0]
            self.parent().frame_area[0][1] = coefficient * self.parent().frame_area[0][1]
            self.parent().frame_area[1][0] = coefficient * self.parent().frame_area[1][0]
            self.parent().frame_area[1][1] = coefficient * self.parent().frame_area[1][1]

            tmp_start_x = self.parent().frame_area[0][0]
            tmp_start_y = self.parent().frame_area[0][1]
            tmp_end_x = self.parent().frame_area[1][0]
            tmp_end_y = self.parent().frame_area[1][1]

            (tmp_x, tmp_y), tmp_w, tmp_h = self.coordinateAdj(tmp_start_x, tmp_start_y, tmp_end_x, tmp_end_y)
            rect = QRectF(tmp_x, tmp_y, tmp_w, tmp_h)
            self.items.append(self.scene.addRect(rect, pen, brush))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())
