import sys
import ctypes
import cv2
import numpy as np
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import time
start_time = time.time()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.img_size = (300, 300)
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.move(screensize[0] - self.img_size[0], screensize[1] - self.img_size[1] - 50)
        self.resize(self.img_size[0], self.img_size[1])

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(f"pushButton")
        self.pushButton.setGeometry(QRect(0, 0, self.img_size[0], self.img_size[1]))
        # self.pushButton.setAttribute(Qt.WA_NoSystemBackground, True)
        # self.pushButton.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.pushButton.setMinimumSize(QSize(100, 100))
        self.pushButton.setText("")
        self.update_icon()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_icon)
        self.timer.start(100)

    def update_icon(self):
        img = cv2.imread("add.png", cv2.IMREAD_UNCHANGED)
        img = np.roll(img, int(150*(time.time() - start_time) % img.shape[0]), axis = 0)
        TF = img[:, :, 3] > 0
        img[TF, 0] = 7
        img[TF, 1] = 110
        img[TF, 2] = 255
        cvImg = img
        height, width, channel = cvImg.shape
        cvImg = np.ascontiguousarray(cvImg, dtype = np.uint8)
        bytesPerLine = channel * width
        qImg = QImage(cvImg.data, width, height, QImage.Format_RGBA8888)
        QPixmap_img = QPixmap().fromImage(qImg)
        self.pushButton.setIcon(QIcon(QPixmap_img))
        self.pushButton.setIconSize(QSize(self.img_size[0], self.img_size[1]))

app = QApplication(sys.argv)
mywindow = MainWindow()
mywindow.show()
app.exec_()
