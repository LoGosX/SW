import string

import cv2
import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QDialog, QMessageBox, QPushButton
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from facerecognition.facerecognizer import FaceRecognizer



class VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)
    login = pyqtSignal(str)
    def run(self):
        self.isFree = True
        fr = FaceRecognizer()
        while True:
            fr._update()
            frame = fr.get_frame(mark_faces=True)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(1600, 1200, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            if(self.isFree):
                self.login.emit("xd")
                self.isFree = False


class MainWindow(QMainWindow):

    def __init__(self,parent = None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SW")
        self.disply_width = 1600
        self.display_height = 1200
        self.resize(self.disply_width,self.display_height)

        self.Loginmsg = QMessageBox()
        self.Loginmsg.setStandardButtons(QMessageBox.Ok | QMessageBox.No)
        self.Loginmsg.buttonClicked.connect(self.loginButton_clicked)

        self.label = QLabel(self)
        self.label.resize( self.disply_width, self.display_height)
        video = VideoThread(self)
        video.changePixmap.connect(self.setImage)
        video.login.connect(self.loginUser)
        video.start()


        self.show()

    def openSecond(self):
        myDialof = QDialog(self)
        myDialof.show()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def loginUser(self, user):
        self.Loginmsg.setText("Hi {}!\n Would you like to log in? ".format(user))
        self.Loginmsg.show()

    def loginButton_clicked(self, i):
        if i.text() == "OK":
            print(i.text())
        print(i.text())

def keyPressEvent(self, e):
        if e.key() == Qt.Key_F9:
            self.close()
